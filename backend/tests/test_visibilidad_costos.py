import base64
import time

import pytest
from itsdangerous import URLSafeTimedSerializer

from extensions import db
from models import PriceSyncState, ProductionRecord, Supply, User
from services.saved_quotes import _cipher
from tests.helpers import crear_receta


@pytest.fixture
def receta():
    tela = Supply(categoria_id=1, name='Tela', unidad_medida='metro',
                  precio_costo_unitario=12345, stock_actual=30, es_tela=True, ancho_cm=300)
    db.session.add(tela)
    db.session.flush()
    receta = crear_receta(1, [{'id_insumo': tela.id, 'nombre': 'Tela', 'tipo_calculo': 'lineal_alto'}])
    return tela, receta


def _sin_costos(objeto):
    prohibidos = {
        'price', 'precio_m2', 'precio_unitario', 'costo_parcial', 'costo_reposicion',
        'cantidad_costo', 'unidad_costo', 'cantidad_reposicion', 'total_materiales',
        'total_mano_obra', 'total_desgaste', 'total', 'desglose_fabricacion',
        'markup_pct', 'ganancia_markup', 'margen_sobre_ventas_pct', 'tarifa_base', 'costo_traslado',
        'costo_inesperado',
    }
    if isinstance(objeto, dict):
        assert not prohibidos.intersection(objeto)
        for valor in objeto.values():
            _sin_costos(valor)
    elif isinstance(objeto, list):
        for valor in objeto:
            _sin_costos(valor)


def test_inventario_y_cotizaciones_por_rol(client, auth, receta):
    tela, version = receta
    admin, ventas, taller = (auth(rol) for rol in ('admin', 'ventas', 'taller'))
    assert client.get('/api/inventory', headers=admin).get_json()[-1]['price'] == 12345
    for headers in (ventas, taller):
        _sin_costos(client.get('/api/inventory', headers=headers).get_json())
        assert client.get(f'/api/inventory/{tela.id}/prices', headers=headers).status_code == 403
        assert client.post('/api/inventory', headers=headers, json={}).status_code == 403
        explosion = client.get('/api/recipes/1/explosion?w=100&h=120', headers=headers).get_json()
        _sin_costos(explosion)
        assert explosion['explosion'][0]['medida_corte']

    cotizacion = client.get('/api/recipes/1/quote?w=100&h=120', headers=ventas).get_json()
    _sin_costos(cotizacion)
    assert cotizacion['precio_producto']['precio_venta_final'] > 0
    calculo = client.post('/api/quotes/calculate', headers=ventas, json={
        'receta_id': version.id, 'ancho': 100, 'alto': 120,
    })
    assert calculo.status_code == 200
    _sin_costos(calculo.get_json())
    assert client.get('/api/recipes/1/quote?w=100&h=120', headers=taller).status_code == 403
    assert client.post('/api/quotes/calculate', headers=taller, json={}).status_code == 403
    assert client.get('/api/quotes/saved', headers=taller).status_code == 403
    assert client.post('/api/quotes/saved', headers=taller, json={}).status_code == 403


def test_produccion_taller_oculta_costos_y_conserva_historial(client, auth, receta):
    taller = auth('taller')
    respuesta = client.post('/api/recipes/1/produce', headers=taller, json={'w': 100, 'h': 120})
    assert respuesta.status_code == 200, respuesta.get_json()
    _sin_costos(respuesta.get_json())
    assert respuesta.get_json()['descontado']
    registro = db.session.get(ProductionRecord, respuesta.get_json()['produccion_id'])
    detalle = list(registro.detalle)
    detalle[0] = {**detalle[0], 'costo_inesperado': 12345, 'cortes': [
        {'corte': 120, 'origen': 'pieza_nueva', 'costo_inesperado': 12345}
    ]}
    registro.detalle = detalle
    db.session.commit()
    for rol in ('ventas', 'taller'):
        historial = client.get('/api/recipes/productions', headers=auth(rol)).get_json()
        _sin_costos(historial)
        assert historial[0]['detalle'][0]['cortes'][0]['corte'] == 120
    admin = client.get('/api/recipes/productions', headers=auth('admin')).get_json()
    assert admin[0]['detalle'][0]['costo_parcial'] > 0


def test_token_cifrado_valida_integridad_usuario_y_vencimiento(client, auth, receta, app):
    ventas = auth('ventas')
    cotizacion = client.get('/api/recipes/1/quote?w=100&h=120', headers=ventas).get_json()
    token = cotizacion['guardado_token']
    assert b'precio_unitario' not in base64.urlsafe_b64decode(token)
    guardado = client.post('/api/quotes/saved', headers=ventas, json={'token': token})
    assert guardado.status_code == 201
    _sin_costos(guardado.get_json())
    _sin_costos(client.get('/api/quotes/saved', headers=ventas).get_json())
    assert client.get('/api/quotes/saved', headers=auth('admin')).get_json()[0]['resultado']['total'] > 0
    assert client.post('/api/quotes/saved', headers=auth('admin'), json={'token': token}).status_code == 400
    contenido = _cipher().decrypt(token.encode())
    vencido = _cipher().encrypt_at_time(contenido, int(time.time()) - 3601).decode()
    firmado_anterior = URLSafeTimedSerializer(app.config['SECRET_KEY'], salt='presupuesto-congelado-v1').dumps({'resultado': {}})
    alterado = token[:30] + ('A' if token[30] != 'A' else 'B') + token[31:]
    for invalido in (vencido, firmado_anterior, alterado):
        assert client.post('/api/quotes/saved', headers=ventas, json={'token': invalido}).status_code == 400


def test_cambio_de_rol_aplica_a_la_api_con_token_existente(client, auth, receta):
    headers = auth('ventas')
    usuario = User.query.filter_by(email='ventas@example.com').one()
    usuario.rol = 'admin'
    db.session.commit()
    assert 'price' in client.get('/api/inventory', headers=headers).get_json()[0]
    usuario.rol = 'ventas'
    db.session.commit()
    _sin_costos(client.get('/api/inventory', headers=headers).get_json())


def test_estado_de_sincronizacion_no_expone_error_a_ventas(client, auth):
    db.session.add(PriceSyncState(id=1, error='Detalle sensible'))
    db.session.commit()
    ventas = client.get('/api/inventory/prices/sheets', headers=auth('ventas')).get_json()
    assert ventas['advertencia'] and ventas['error'] is None
    assert client.get('/api/inventory/prices/sheets', headers=auth('admin')).get_json()['error'] == 'Detalle sensible'
    assert client.get('/api/inventory/prices/sheets', headers=auth('taller')).status_code == 403
