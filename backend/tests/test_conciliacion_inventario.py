import json
from decimal import Decimal

from extensions import db
from models import InventoryMovement, PiezaStock, Supply, SupplyCategory, SupplyPriceHistory


def perfil(stock=400, piezas=()):
    categoria = SupplyCategory(name='Perfiles y Tubos')
    db.session.add(categoria)
    db.session.flush()
    insumo = Supply(categoria_id=categoria.id, name='Tubo', unidad_medida='cm',
                    stock_actual=stock, precio_costo_unitario=1, largo_pieza_cm=400)
    db.session.add(insumo)
    db.session.flush()
    for largo in piezas:
        db.session.add(PiezaStock(id_insumo=insumo.id, longitud_original_cm=400,
                                  longitud_actual_cm=largo, es_retazo=largo != 400))
    db.session.commit()
    return insumo


def test_conciliar_piezas_conserva_ids_y_audita_cambios(client, auth):
    insumo = perfil(400, [400, 400])
    headers = auth('admin')
    url = f'/api/inventory/{insumo.id}/pieces/reconcile'
    estado = client.get(url, headers=headers).get_json()
    piezas = [dict(p) for p in estado['piezas']]
    piezas[1]['longitud_actual_cm'] = '0'
    piezas.append(dict(id=None, longitud_original_cm='400', longitud_actual_cm='120', es_retazo=True))
    response = client.post(url, headers=headers, json={
        'stock_esperado': estado['stock'], 'piezas_esperadas': estado['piezas'],
        'piezas': piezas, 'motivo': 'Conteo físico',
    })
    assert response.status_code == 201, response.get_json()
    assert response.get_json()['cantidad'] == 120
    db.session.expire_all()
    assert db.session.get(Supply, insumo.id).stock_actual == 520
    assert db.session.get(PiezaStock, piezas[1]['id']).longitud_actual_cm == 0
    movimientos = InventoryMovement.query.filter_by(id_insumo=insumo.id).order_by(InventoryMovement.id).all()
    assert [(m.cantidad, m.stock_resultante) for m in movimientos] == [(400, 400), (120, 520)]
    movimiento = movimientos[-1]
    detalle = json.loads(movimiento.notas)
    assert detalle['motivo'] == 'Conteo físico'
    assert len(detalle['antes']) == 2 and len(detalle['despues']) == 3
    assert all(p['id'] for p in detalle['despues'])
    stale = client.post(url, headers=headers, json={
        'stock_esperado': estado['stock'], 'piezas_esperadas': estado['piezas'],
        'piezas': piezas, 'motivo': 'Conteo físico',
    })
    assert stale.status_code == 409
    assert InventoryMovement.query.filter_by(id_insumo=insumo.id).count() == 2


def test_conciliacion_con_saldo_igual_registra_apertura_pieza_y_exige_admin(client, auth):
    insumo = perfil(400)
    url = f'/api/inventory/{insumo.id}/pieces/reconcile'
    estado = client.get(url, headers=auth('admin')).get_json()
    datos = {'stock_esperado': estado['stock'], 'piezas_esperadas': [],
             'piezas': [{'id': None, 'longitud_original_cm': 400,
                         'longitud_actual_cm': 400, 'es_retazo': False}], 'motivo': 'Conteo'}
    assert client.post(url, headers=auth('taller'), json=datos).status_code == 403
    response = client.post(url, headers=auth('admin'), json=datos)
    assert response.status_code == 201 and response.get_json()['cantidad'] == 0
    assert PiezaStock.query.filter_by(id_insumo=insumo.id).count() == 1


def test_script_conciliacion_simula_y_es_atomico(client, auth, app, tmp_path):
    insumo = perfil(400)
    estado = client.get(f'/api/inventory/{insumo.id}/pieces/reconcile', headers=auth('admin')).get_json()
    datos = {'id_insumo': insumo.id, 'stock_esperado': estado['stock'], 'piezas_esperadas': [],
             'piezas': [{'id': None, 'longitud_original_cm': 400, 'longitud_actual_cm': 400,
                         'es_retazo': False}], 'motivo': 'Conteo'}
    archivo = tmp_path / 'conteo.json'
    archivo.write_text(json.dumps([datos]), encoding='utf-8')
    runner = app.test_cli_runner()
    result = runner.invoke(args=['conciliar-piezas', str(archivo)])
    assert result.exit_code == 0, result.output
    assert PiezaStock.query.filter_by(id_insumo=insumo.id).count() == 0
    result = runner.invoke(args=['conciliar-piezas', str(archivo), '--apply'])
    assert result.exit_code == 0, result.output
    assert PiezaStock.query.filter_by(id_insumo=insumo.id).count() == 1
    assert runner.invoke(args=['conciliar-piezas', str(archivo), '--apply']).exit_code != 0


def _telas_y_etiqueta():
    cat = SupplyCategory(name='Telas')
    db.session.add(cat)
    db.session.flush()
    tela = Supply(categoria_id=cat.id, name='Blackout ancho 2.20', unidad_medida='cm',
                  precio_costo_unitario=Decimal('122.5'), stock_actual=1000, stock_minimo=100)
    db.session.add(tela)
    etiqueta = Supply.query.filter_by(codigo_sku='ROLLER-ETIQUETA').one()
    etiqueta.stock_actual = 100
    db.session.flush()
    db.session.add_all([
        InventoryMovement(id_insumo=tela.id, tipo='apertura', cantidad=1000, stock_resultante=1000),
        SupplyPriceHistory(id_insumo=tela.id, precio=Decimal('122.5')),
        InventoryMovement(id_insumo=etiqueta.id, tipo='apertura', cantidad=0, stock_resultante=0),
    ])
    db.session.commit()
    return tela, etiqueta


def test_normalizacion_simulacion_conversion_historial_e_idempotencia(app):
    tela, etiqueta = _telas_y_etiqueta()
    runner = app.test_cli_runner()
    result = runner.invoke(args=['normalizar-inventario-inicial'])
    assert result.exit_code == 0, result.output
    db.session.expire_all()
    assert tela.unidad_medida == 'cm' and etiqueta.stock_actual == 100
    assert InventoryMovement.query.filter_by(id_insumo=etiqueta.id).count() == 1
    result = runner.invoke(args=['normalizar-inventario-inicial', '--apply'])
    assert result.exit_code == 0, result.output
    db.session.expire_all()
    assert (tela.ancho_cm, tela.stock_actual, tela.stock_minimo, tela.precio_costo_unitario) == (220, 10, 1, 12250)
    assert tela.es_tela and tela.unidad_medida == 'metro' and tela.precio_m2 is None
    movimientos = InventoryMovement.query.filter_by(id_insumo=tela.id).order_by(InventoryMovement.id).all()
    assert [(m.cantidad, m.unidad) for m in movimientos] == [(1000, 'cm'), (0, 'metro')]
    precios = SupplyPriceHistory.query.filter_by(id_insumo=tela.id).order_by(SupplyPriceHistory.id).all()
    assert [(p.precio, p.unidad) for p in precios] == [(Decimal('122.5'), 'cm'), (12250, 'metro')]
    assert sum(m.cantidad for m in InventoryMovement.query.filter_by(id_insumo=etiqueta.id)) == 100
    assert etiqueta.stock_actual == 100
    assert runner.invoke(args=['normalizar-inventario-inicial', '--apply']).exit_code == 0
    assert InventoryMovement.query.filter_by(id_insumo=etiqueta.id).count() == 2


def test_normalizacion_ambigua_no_aplica_cambios(app):
    tela, etiqueta = _telas_y_etiqueta()
    db.session.add(Supply(categoria_id=tela.categoria_id, name='Tela ancho 2', unidad_medida='cm',
                         precio_costo_unitario=5, stock_actual=200))
    db.session.commit()
    result = app.test_cli_runner().invoke(args=['normalizar-inventario-inicial', '--apply'])
    assert result.exit_code != 0
    db.session.expire_all()
    assert tela.unidad_medida == 'cm' and tela.ancho_cm is None
    assert InventoryMovement.query.filter_by(id_insumo=etiqueta.id).count() == 1


def test_extraccion_de_anchos_existentes_y_ambiguedades():
    import pytest
    from exceptions import ValidationFailed
    from services.normalizacion_inicial import ancho_del_nombre

    assert ancho_del_nombre('Black Out TAPAR Blanco - ancho 2.20') == 220
    assert ancho_del_nombre('SCREEN OLO 9 (Gris) - ancho 2.50') == 250
    assert ancho_del_nombre('Tela ancho 250 cm') == 250
    assert ancho_del_nombre('Tela ancho 2,50 metros') == 250
    for nombre in ('Tela ancho 2', 'Tela sin medida', 'Tela ancho 2.20 ancho 2.50'):
        with pytest.raises(ValidationFailed):
            ancho_del_nombre(nombre)


def test_conciliacion_general_corrige_historial_y_conteo(client, auth):
    categoria = SupplyCategory.query.first()
    insumo = Supply(categoria_id=categoria.id, name='Accesorio', unidad_medida='unidad',
                    stock_actual=100, precio_costo_unitario=200)
    db.session.add(insumo)
    db.session.commit()
    url = f'/api/inventory/{insumo.id}/reconcile'
    headers = auth('admin')
    snapshot = client.get(url, headers=headers).get_json()
    assert (snapshot['stock'], snapshot['historial'], snapshot['diferencia']) == ('100.0000', '0', '100.0000')
    datos = {'stock_esperado': snapshot['stock'], 'historial_esperado': snapshot['historial'],
             'stock_contado': 95, 'motivo': 'Conteo físico'}
    assert client.post(url, headers=auth('taller'), json=datos).status_code == 403
    response = client.post(url, headers=headers, json=datos)
    assert response.status_code == 200, response.get_json()
    db.session.expire_all()
    assert db.session.get(Supply, insumo.id).stock_actual == 95
    movimientos = InventoryMovement.query.filter_by(id_insumo=insumo.id).order_by(InventoryMovement.id).all()
    assert [(m.cantidad, m.stock_resultante) for m in movimientos] == [(100, 100), (-5, 95)]
    assert client.post(url, headers=headers, json=datos).status_code == 409


def test_conciliacion_convierte_historial_de_tela(client, auth):
    tela, _ = _telas_y_etiqueta()
    assert app_runner(client).invoke(args=['normalizar-inventario-inicial', '--apply']).exit_code == 0
    data = client.get(f'/api/inventory/{tela.id}/reconcile', headers=auth('admin')).get_json()
    assert Decimal(data['historial']) == Decimal('10')
    assert Decimal(data['diferencia']) == 0


def test_conciliacion_bloquea_historial_ambiguo(client, auth):
    tela, _ = _telas_y_etiqueta()
    assert app_runner(client).invoke(args=['normalizar-inventario-inicial', '--apply']).exit_code == 0
    db.session.add(InventoryMovement(id_insumo=tela.id, tipo='ajuste', cantidad=1, stock_resultante=11))
    db.session.commit()
    response = client.get(f'/api/inventory/{tela.id}/reconcile', headers=auth('admin'))
    assert response.status_code == 409
    assert 'sin unidad' in response.get_json()['message']


def app_runner(client):
    return client.application.test_cli_runner()


def test_preparar_telas_lineales_versiona_y_simula(app):
    from models import Receta
    from tests.helpers import crear_receta
    tela, _ = _telas_y_etiqueta()
    crear_receta(1, [{'id_insumo': tela.id, 'nombre': 'Tela', 'tipo_calculo': 'superficie', 'merma_pct': 5}])
    runner = app.test_cli_runner()
    result = runner.invoke(args=['preparar-telas-lineales'])
    assert result.exit_code == 0, result.output
    db.session.expire_all()
    assert tela.unidad_medida == 'cm' and Receta.query.count() == 1
    result = runner.invoke(args=['preparar-telas-lineales', '--apply'])
    assert result.exit_code == 0, result.output
    db.session.expire_all()
    versiones = Receta.query.order_by(Receta.version).all()
    assert [r.items[0].tipo_calculo for r in versiones] == ['superficie', 'lineal_alto']
    assert versiones[0].vigente_hasta is not None and versiones[1].vigente_hasta is None
    assert tela.unidad_medida == 'metro'
    assert runner.invoke(args=['preparar-telas-lineales', '--apply']).exit_code == 0
    assert Receta.query.count() == 2


def test_normalizacion_preserva_detalle_y_unidades_de_produccion(client, auth, app):
    from models import ProductionRecord
    from tests.helpers import crear_receta
    tela, _ = _telas_y_etiqueta()
    receta = crear_receta(1, [{'id_insumo': tela.id, 'nombre': 'Tela', 'tipo_calculo': 'superficie'}])
    detalle = [{'componente': 'Tela histórica', 'unidad': 'cm', 'consumo_m_o_m2': 175,
                'costo_parcial': 100, 'metodo': 'ROLLO'}]
    db.session.add(ProductionRecord(producto_id=1, producto_nombre='Producto 1', receta_id=receta.id,
                                   receta_version=1, ancho_cm=150, alto_cm=175, opciones={},
                                   total_materiales=100, total_minutos=0, total_mano_obra=0,
                                   total_desgaste=0, total=100, detalle=detalle))
    db.session.commit()
    h = auth('admin')
    antes = client.get('/api/recipes/productions', headers=h).get_json()[0]
    result = app.test_cli_runner().invoke(args=['preparar-telas-lineales', '--apply'])
    assert result.exit_code == 0, result.output
    despues = client.get('/api/recipes/productions', headers=h).get_json()[0]
    assert despues == antes
    assert despues['detalle'] == detalle


def test_preparar_no_confirma_si_cambia_el_plan(app):
    import pytest
    from exceptions import ConflictError
    from services.telas_lineales import preparar_telas_lineales
    tela, _ = _telas_y_etiqueta()
    plan = preparar_telas_lineales()
    tela.stock_actual = 1200
    db.session.commit()
    with pytest.raises(ConflictError):
        preparar_telas_lineales(aplicar=True, plan_esperado=plan)
    db.session.rollback()
    db.session.refresh(tela)
    assert tela.stock_actual == 1200 and tela.unidad_medida == 'cm'


def test_preparar_puede_verificarse_antes_de_confirmar(app):
    from services.telas_lineales import preparar_telas_lineales
    tela, _ = _telas_y_etiqueta()
    plan = preparar_telas_lineales()
    preparar_telas_lineales(aplicar=True, plan_esperado=plan, commit=False)
    assert tela.unidad_medida == 'metro'
    db.session.rollback()
    db.session.refresh(tela)
    assert tela.unidad_medida == 'cm'


def test_preparar_telas_lineales_revierte_si_receta_no_es_valida(app):
    from models import Receta
    from tests.helpers import crear_receta
    tela, etiqueta = _telas_y_etiqueta()
    crear_receta(1, [{'id_insumo': tela.id, 'nombre': 'Tela', 'tipo_calculo': 'superficie'},
                     {'id_insumo': etiqueta.id, 'nombre': 'Etiqueta', 'tipo_calculo': 'fijo'}])
    result = app.test_cli_runner().invoke(args=['preparar-telas-lineales', '--apply'])
    assert result.exit_code != 0 and 'etiqueta' in result.output.lower()
    db.session.expire_all()
    assert tela.unidad_medida == 'cm'
    assert Receta.query.count() == 1
    assert InventoryMovement.query.filter_by(id_insumo=etiqueta.id).count() == 1


def test_preparar_telas_no_omite_superficie_sin_tela(app):
    from tests.helpers import crear_receta
    tela, etiqueta = _telas_y_etiqueta()
    crear_receta(1, [{'id_insumo': etiqueta.id, 'nombre': 'Antiguo', 'tipo_calculo': 'superficie'}])
    result = app.test_cli_runner().invoke(args=['preparar-telas-lineales', '--apply'])
    assert result.exit_code != 0 and 'no tiene una tela normalizada' in result.output
    db.session.expire_all()
    assert tela.unidad_medida == 'cm'
    assert InventoryMovement.query.filter_by(id_insumo=etiqueta.id).count() == 1
