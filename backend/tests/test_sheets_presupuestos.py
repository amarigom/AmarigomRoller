from datetime import timedelta
from decimal import Decimal

import pytest

from extensions import db
from exceptions import ExternalServiceError, ValidationFailed
from models import PriceSyncState, Supply, SupplyCategory, SupplyPriceHistory
from services import google_sheets_prices
from tests.helpers import crear_receta
from utils.clock import utcnow


@pytest.fixture
def precios(app):
    cat = SupplyCategory(name='Proveedor')
    db.session.add(cat)
    db.session.flush()
    perfil = Supply(categoria_id=cat.id, codigo_sku='TRO01072', name='Perfil 4 m',
                    unidad_medida='cm', largo_pieza_cm=400, precio_costo_unitario=10, stock_actual=400)
    tela = Supply(categoria_id=cat.id, codigo_sku='LBK3503', name='Tela',
                  unidad_medida='metro', es_tela=True, ancho_cm=250, precio_costo_unitario=20, stock_actual=30)
    db.session.add_all([perfil, tela, PriceSyncState(id=1)])
    db.session.commit()
    return perfil, tela


def _filas():
    return [
        ['15/11/2026', 'SISTEMAS Y ACCESORIOS CORTINAS ROLLER - ZEBRA'],
        ['Articulo', 'Descripción', 'Unidad Medida', 'Precio Final'],
        ['TRO01072', 'Perfil 4 mts', 'Unidad', 26289.59],
        ['LBK3503', 'Tela', 'Mt.Lineal', 23498.44],
        ['AJENO', 'Otro', 'Unidad', 100],
    ]


def test_sincronizacion_convierte_y_registra_solo_cambios(client, auth, precios, monkeypatch):
    perfil, tela = precios
    monkeypatch.setattr(google_sheets_prices, '_leer_hoja', _filas)
    headers = auth('admin')
    response = client.post('/api/inventory/prices/sheets', headers=headers)
    assert response.status_code == 200, response.get_json()
    assert response.get_json() == {'actualizados': 2, 'omitidos': 1}
    db.session.expire_all()
    assert db.session.get(Supply, perfil.id).precio_costo_unitario == Decimal('65.7240')
    assert db.session.get(Supply, tela.id).precio_costo_unitario == Decimal('23498.4400')
    historial = SupplyPriceHistory.query.filter_by(motivo='Sincronización Google Sheets').all()
    assert len(historial) == 2 and all(h.usuario_id for h in historial)
    assert client.post('/api/inventory/prices/sheets', headers=headers).get_json()['actualizados'] == 0
    assert SupplyPriceHistory.query.filter_by(motivo='Sincronización Google Sheets').count() == 2
    assert client.post('/api/inventory/prices/sheets', headers=auth('ventas')).status_code == 403


@pytest.mark.parametrize('cambio', ['duplicado', 'unidad', 'precio', 'precio_extremo'])
def test_sincronizacion_invalida_es_atomica_y_avisa(client, auth, precios, monkeypatch, cambio):
    filas = _filas()
    if cambio == 'duplicado':
        filas.append([*filas[2][:3], 500])
    elif cambio == 'unidad':
        filas[3][2] = 'Caja'
    elif cambio == 'precio_extremo':
        filas[3][3] = '1e100000'
    else:
        filas[3][3] = 0
    monkeypatch.setattr(google_sheets_prices, '_leer_hoja', lambda: filas)
    response = client.post('/api/inventory/prices/sheets', headers=auth('admin'))
    assert response.status_code == 400
    db.session.expire_all()
    assert db.session.get(Supply, precios[0].id).precio_costo_unitario == Decimal('10')
    assert db.session.get(Supply, precios[1].id).precio_costo_unitario == Decimal('20')
    assert SupplyPriceHistory.query.count() == 0
    estado = db.session.get(PriceSyncState, 1)
    assert estado.ultima_exitosa is None and estado.error and estado.ultimo_intento


def test_estado_advertencia_por_fallo_y_atraso(client, auth, precios, app):
    app.config.update(GOOGLE_SHEETS_ID='ejemplo', GOOGLE_SHEETS_CREDENTIALS_JSON='ejemplo')
    estado = db.session.get(PriceSyncState, 1)
    estado.ultima_exitosa = utcnow() - timedelta(hours=19)
    db.session.commit()
    data = client.get('/api/inventory/prices/sheets', headers=auth('ventas')).get_json()
    assert data['configurado'] and data['advertencia']
    estado.ultima_exitosa = utcnow()
    estado.error = 'Falló la conexión'
    db.session.commit()
    assert client.get('/api/inventory/prices/sheets', headers=auth('ventas')).get_json()['advertencia']


def test_error_externo_conserva_ultima_sincronizacion(client, auth, precios, monkeypatch):
    estado = db.session.get(PriceSyncState, 1)
    anterior = utcnow() - timedelta(hours=2)
    estado.ultima_exitosa = anterior
    db.session.commit()
    def falla():
        raise ExternalServiceError('No se pudo leer la hoja')
    monkeypatch.setattr(google_sheets_prices, '_leer_hoja', falla)
    response = client.post('/api/inventory/prices/sheets', headers=auth('admin'))
    assert response.status_code == 502
    estado = db.session.get(PriceSyncState, 1)
    assert estado.ultima_exitosa == anterior
    assert estado.error == 'No se pudo leer la hoja'
    assert estado.ultimo_intento > anterior


def test_lectura_usa_api_privada_y_valores_numericos(app, monkeypatch):
    class Credenciales:
        token = 'token-ficticio'

        def refresh(self, request):
            pass

    class Respuesta:
        def raise_for_status(self):
            pass

        def json(self):
            return {'values': _filas()}

    peticiones = []
    def get(url, **kwargs):
        peticiones.append((url, kwargs))
        return Respuesta()

    app.config.update(GOOGLE_SHEETS_ID='id-ficticio', GOOGLE_SHEETS_TAB='PRODUCTOS_INVENTARIO',
                      GOOGLE_SHEETS_CREDENTIALS_JSON='{}')
    monkeypatch.setattr(google_sheets_prices.service_account.Credentials, 'from_service_account_info',
                        lambda info, scopes: Credenciales())
    monkeypatch.setattr(google_sheets_prices.requests, 'get', get)
    assert google_sheets_prices._leer_hoja() == _filas()
    url, options = peticiones[0]
    assert 'id-ficticio' in url and 'PRODUCTOS_INVENTARIO' in url
    assert options['params'] == {'valueRenderOption': 'UNFORMATTED_VALUE'}
    assert options['headers']['Authorization'] == 'Bearer token-ficticio'


def test_precio_de_rollo_solo_se_acepta_para_stock_en_rollos(precios):
    perfil, _ = precios
    perfil.unidad_medida = 'rollo'
    assert google_sheets_prices._precio_por_unidad(perfil, 'Rollo', 1250) == Decimal('1250')
    perfil.unidad_medida = 'metro'
    with pytest.raises(ValidationFailed, match='unidad de compra incompatible'):
        google_sheets_prices._precio_por_unidad(perfil, 'Rollo', 1250)


def test_precios_por_presentacion_y_filas_duplicadas_identicas(client, auth, precios, monkeypatch):
    perfil, _ = precios
    perfil.unidad_medida = 'unidad'
    perfil.unidad_compra = 'juego'
    perfil.factor_conversion = 2
    db.session.commit()
    filas = _filas()
    filas[2][2] = 'Juego'
    filas.append(list(filas[2]))
    monkeypatch.setattr(google_sheets_prices, '_leer_hoja', lambda: filas)
    response = client.post('/api/inventory/prices/sheets', headers=auth('admin'))
    assert response.status_code == 200, response.get_json()
    assert response.get_json()['actualizados'] == 2
    assert db.session.get(Supply, perfil.id).precio_costo_unitario == Decimal('13144.7950')


def test_lectura_admite_archivo_de_cuenta_de_servicio(app, monkeypatch, tmp_path):
    class Credenciales:
        token = 'token-ficticio'

        def refresh(self, request):
            pass

    class Respuesta:
        def raise_for_status(self):
            pass

        def json(self):
            return {'values': _filas()}

    ruta = str(tmp_path / 'cuenta.json')
    llamadas = []
    def credenciales(path, scopes):
        llamadas.append((path, scopes))
        return Credenciales()

    app.config.update(GOOGLE_SHEETS_ID='id-ficticio', GOOGLE_SHEETS_CREDENTIALS_JSON=None,
                      GOOGLE_APPLICATION_CREDENTIALS=ruta)
    monkeypatch.setattr(google_sheets_prices.service_account.Credentials, 'from_service_account_file', credenciales)
    monkeypatch.setattr(google_sheets_prices.requests, 'get', lambda *args, **kwargs: Respuesta())
    assert google_sheets_prices._leer_hoja() == _filas()
    assert llamadas == [(ruta, [google_sheets_prices.SCOPE])]


def test_comando_programado_sin_usuario(client, precios, app, monkeypatch):
    monkeypatch.setattr(google_sheets_prices, '_leer_hoja', _filas)
    result = app.test_cli_runner().invoke(args=['sincronizar-precios-sheets'])
    assert result.exit_code == 0, result.output
    assert 'Precios actualizados: 2' in result.output
    assert all(p.usuario_id is None for p in SupplyPriceHistory.query.all())


def test_presupuesto_guardado_congela_calculo_y_valida_token(client, auth, precios, monkeypatch):
    _, tela = precios
    crear_receta(1, [{'id_insumo': tela.id, 'nombre': 'Tela', 'tipo_calculo': 'lineal_alto'}])
    headers = auth('ventas')
    respuesta = client.get('/api/recipes/1/quote?w=150&h=200&km_obra=5&referencia=ABC', headers=headers)
    assert respuesta.status_code == 200, respuesta.get_json()
    cotizacion = respuesta.get_json()
    monkeypatch.setattr(google_sheets_prices, '_leer_hoja', _filas)
    assert client.post('/api/inventory/prices/sheets', headers=auth('admin')).status_code == 200
    guardado = client.post('/api/quotes/saved', headers=headers, json={'token': cotizacion['guardado_token']})
    assert guardado.status_code == 201, guardado.get_json()
    assert guardado.get_json()['resultado']['total_presupuesto'] == cotizacion['total_presupuesto']
    nuevo = client.get('/api/recipes/1/quote?w=150&h=200&km_obra=5', headers=headers).get_json()
    assert nuevo['total_presupuesto'] != cotizacion['total_presupuesto']
    historial = client.get('/api/quotes/saved', headers=headers).get_json()
    assert 'precio_unitario' not in historial[0]['resultado']['explosion'][0]
    admin = client.get('/api/quotes/saved', headers=auth('admin')).get_json()
    assert admin[0]['resultado']['explosion'][0]['precio_unitario'] == 20
    assert historial[0]['referencia'] == 'ABC'
    assert client.post('/api/quotes/saved', headers=headers, json={'token': 'falso'}).status_code == 400
    assert client.post('/api/quotes/saved', headers=auth('admin'),
                       json={'token': cotizacion['guardado_token']}).status_code == 400
