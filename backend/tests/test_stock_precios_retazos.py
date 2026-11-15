from extensions import db
from models import InventoryMovement, RetazoTela, Supply, SupplyCategory, SupplyPriceHistory
from tests.helpers import crear_receta


def _insumo(name='Blackout', stock=10, minimo=0, precio=100, ancho=300):
    cat = SupplyCategory.query.first()
    if cat is None:
        cat = SupplyCategory(name='Telas')
        db.session.add(cat)
        db.session.flush()
    insumo = Supply(
        categoria_id=cat.id, name=name, unidad_medida='metro',
        precio_costo_unitario=precio, stock_actual=stock, stock_minimo=minimo, ancho_cm=ancho, es_tela=True,
    )
    db.session.add(insumo)
    db.session.commit()
    db.session.add(InventoryMovement(
        id_insumo=insumo.id, tipo='apertura', cantidad=stock, stock_resultante=stock,
        referencia='Test', notas='Stock inicial',
    ))
    db.session.add(SupplyPriceHistory(
        id_insumo=insumo.id, precio=precio, motivo='Precio inicial',
    ))
    db.session.commit()
    return insumo


def test_alta_de_insumo_crea_movimiento_inicial_e_historial_de_precio(client, auth):
    h = auth('admin')
    cat = SupplyCategory(name='Telas')
    db.session.add(cat)
    db.session.commit()
    r = client.post('/api/inventory', headers=h, json={
        'name': 'Blackout', 'categoria_id': cat.id, 'stock_actual': 12,
        'stock_minimo': 3, 'precio_costo_unitario': 250,
    })
    assert r.status_code == 201, r.get_json()
    supply_id = r.get_json()['id']
    movement = InventoryMovement.query.filter_by(id_insumo=supply_id).one()
    price = SupplyPriceHistory.query.filter_by(id_insumo=supply_id).one()
    assert movement.tipo == 'apertura' and float(movement.cantidad) == 12
    assert float(price.precio) == 250
    assert r.get_json()['stock_minimo'] == 3


def test_entrada_y_ajuste_generan_movimientos_auditables(client, auth):
    insumo = _insumo(stock=10)
    h = auth('taller')
    entrada = client.post(f'/api/inventory/{insumo.id}/movements', headers=h, json={
        'tipo': 'entrada', 'cantidad': 5, 'referencia': 'Compra 123',
    })
    assert entrada.status_code == 201, entrada.get_json()
    ajuste = client.post(f'/api/inventory/{insumo.id}/movements', headers=h, json={
        'tipo': 'ajuste', 'cantidad': -2, 'notas': 'Conteo físico',
    })
    assert ajuste.status_code == 201
    db.session.refresh(insumo)
    assert float(insumo.stock_actual) == 13
    movimientos = client.get(f'/api/inventory/{insumo.id}/movements', headers=h).get_json()
    assert len(movimientos) == 3
    assert {m['tipo'] for m in movimientos} == {'apertura', 'entrada', 'ajuste'}
    assert any(m['referencia'] == 'Compra 123' and m['stock_resultante'] == 15 for m in movimientos)


def test_movimiento_no_permite_stock_negativo(client, auth):
    insumo = _insumo(stock=2)
    r = client.post(f'/api/inventory/{insumo.id}/movements', headers=auth('taller'), json={
        'tipo': 'ajuste', 'cantidad': -3,
    })
    assert r.status_code == 409
    db.session.refresh(insumo)
    assert float(insumo.stock_actual) == 2
    assert InventoryMovement.query.filter_by(id_insumo=insumo.id).count() == 1


def test_movimientos_rechazan_cantidad_invalida_y_respeta_permisos(client, auth):
    insumo = _insumo()
    assert client.post(f'/api/inventory/{insumo.id}/movements',
                       headers=auth('taller'), json={'tipo': 'entrada', 'cantidad': 0}).status_code == 400
    assert client.post(f'/api/inventory/{insumo.id}/movements',
                       headers=auth('ventas'), json={'tipo': 'entrada', 'cantidad': 1}).status_code == 403
    assert client.get('/api/inventory/999/movements', headers=auth('admin')).status_code == 404


def test_movimiento_rechaza_cantidad_no_finita(client, auth):
    insumo = _insumo()
    r = client.post(f'/api/inventory/{insumo.id}/movements', headers=auth('taller'),
                    json={'tipo': 'entrada', 'cantidad': float('nan')})
    assert r.status_code == 400


def test_produccion_registra_consumo_en_movimientos(client, auth):
    tela = _insumo(stock=10, ancho=300)
    crear_receta(1, [{'id_insumo': tela.id, 'nombre': 'Tela', 'tipo_calculo': 'lineal_alto'}])
    r = client.post('/api/recipes/1/produce', headers=auth('taller'), json={'w': 100, 'h': 120})
    assert r.status_code == 200, r.get_json()
    consumos = InventoryMovement.query.filter_by(id_insumo=tela.id, tipo='consumo').all()
    assert len(consumos) == 1
    assert float(consumos[0].cantidad) == -1.2
    assert float(consumos[0].stock_resultante) == 8.8
    assert 'Producto 1' in consumos[0].referencia


def test_produccion_guarda_historial_completo_y_enlaza_movimientos(client, auth):
    tela = _insumo(stock=10, ancho=300)
    crear_receta(1, [{'id_insumo': tela.id, 'nombre': 'Tela', 'tipo_calculo': 'lineal_alto'}])
    h = auth('taller')
    r = client.post('/api/recipes/1/produce', headers=h, json={
        'w': 100, 'h': 120, 'referencia': 'PED-100', 'opciones': {'sistema': 'cadena'},
    })
    assert r.status_code == 200, r.get_json()
    production_id = r.get_json()['produccion_id']
    historial = client.get('/api/recipes/productions?referencia=PED-100', headers=auth('admin'))
    assert historial.status_code == 200
    registro = historial.get_json()[0]
    assert registro['id'] == production_id
    assert registro['producto_nombre'] == 'Producto 1'
    assert registro['receta_version'] == 1
    assert (registro['ancho_cm'], registro['alto_cm']) == (100, 120)
    assert registro['opciones'] == {'sistema': 'cadena'}
    assert registro['referencia'] == 'PED-100'
    assert registro['usuario'] == 'Taller'
    assert registro['total'] == 2320
    assert registro['total_desgaste'] == 2000
    assert registro['detalle'][0]['componente'] == 'Blackout'
    movimiento = InventoryMovement.query.filter_by(tipo='consumo', id_insumo=tela.id).one()
    assert movimiento.produccion_id == production_id
    etiqueta = Supply.query.filter_by(codigo_sku='ROLLER-ETIQUETA').one()
    consumo = InventoryMovement.query.filter_by(tipo='consumo', id_insumo=etiqueta.id).one()
    assert (float(consumo.cantidad), consumo.produccion_id, float(etiqueta.stock_actual)) == (-1, production_id, 9999)


def test_sin_etiquetas_la_produccion_no_descontara_otros_insumos(client, auth):
    tela = _insumo(stock=10, ancho=300)
    etiqueta = Supply.query.filter_by(codigo_sku='ROLLER-ETIQUETA').one()
    etiqueta.stock_actual = 0
    db.session.commit()
    crear_receta(1, [{'id_insumo': tela.id, 'nombre': 'Tela', 'tipo_calculo': 'lineal_alto'}])
    respuesta = client.post('/api/recipes/1/produce', headers=auth('taller'), json={'w': 100, 'h': 120})
    assert respuesta.status_code == 409
    assert 'Etiqueta' in str(respuesta.get_json())
    db.session.refresh(tela)
    assert float(tela.stock_actual) == 10
    assert InventoryMovement.query.filter_by(tipo='consumo').count() == 0
    assert client.get('/api/recipes/productions', headers=auth('taller')).get_json() == []


def test_produccion_fallida_no_crea_registro_de_historial(client, auth):
    tela = _insumo(stock=1, ancho=300)
    crear_receta(1, [{'id_insumo': tela.id, 'nombre': 'Tela', 'tipo_calculo': 'lineal_alto'}])
    respuesta = client.post('/api/recipes/1/produce', headers=auth('taller'), json={
        'w': 100, 'h': 120,
    })
    assert respuesta.status_code == 409
    assert client.get('/api/recipes/productions', headers=auth('taller')).get_json() == []


def test_historial_produccion_filtra_por_producto_y_restringe_permisos(client, auth):
    tela = _insumo(stock=10, ancho=300)
    crear_receta(1, [{'id_insumo': tela.id, 'nombre': 'Tela', 'tipo_calculo': 'lineal_alto'}])
    h = auth('taller')
    client.post('/api/recipes/1/produce', headers=h, json={'w': 100, 'h': 120})
    assert len(client.get('/api/recipes/productions?producto_id=1', headers=h).get_json()) == 1
    assert client.get('/api/recipes/productions?producto_id=99', headers=h).status_code == 404
    assert client.get('/api/recipes/productions', headers=auth('ventas')).status_code == 200


def test_alertas_de_stock_minimo_y_ajuste_restringido_a_admin(client, auth):
    insumo = _insumo(stock=2, minimo=5)
    alertas = client.get('/api/inventory/alerts', headers=auth('ventas')).get_json()
    alerta = next(a for a in alertas if a['id_insumo'] == insumo.id)
    assert alerta['faltante'] == 3
    assert client.patch(f'/api/inventory/{insumo.id}/minimum',
                        headers=auth('taller'), json={'stock_minimo': 8}).status_code == 403
    r = client.patch(f'/api/inventory/{insumo.id}/minimum',
                     headers=auth('admin'), json={'stock_minimo': 8})
    assert r.status_code == 200 and r.get_json()['stock_minimo'] == 8


def test_actualizacion_masiva_de_precios_crea_historial(client, auth):
    a = _insumo(name='Tela A', precio=100)
    b = _insumo(name='Tela B', precio=200)
    h = auth('admin')
    r = client.post('/api/inventory/prices', headers=h, json={
        'porcentaje': 10, 'motivo': 'Lista noviembre',
    })
    assert r.status_code == 200, r.get_json()
    assert r.get_json()['actualizados'] == 3
    db.session.refresh(a)
    db.session.refresh(b)
    assert float(a.precio_costo_unitario) == 110 and float(b.precio_costo_unitario) == 220
    assert len(client.get(f'/api/inventory/{a.id}/prices', headers=h).get_json()) == 2


def test_lista_de_precios_por_proveedor_es_atomica(client, auth):
    a = _insumo(name='Tela A', precio=100)
    h = auth('admin')
    r = client.post('/api/inventory/prices', headers=h, json={
        'items': [{'id_insumo': a.id, 'precio': 125}, {'id_insumo': 999, 'precio': 5}],
    })
    assert r.status_code == 404
    db.session.refresh(a)
    assert float(a.precio_costo_unitario) == 100
    assert SupplyPriceHistory.query.filter_by(id_insumo=a.id).count() == 1


def test_precio_no_admin_y_validacion_de_operacion_excluyente(client, auth):
    insumo = _insumo()
    assert client.post('/api/inventory/prices', headers=auth('taller'),
                       json={'porcentaje': 10}).status_code == 403
    assert client.post('/api/inventory/prices', headers=auth('admin'),
                       json={'porcentaje': 5, 'items': [{'id_insumo': insumo.id, 'precio': 3}]}).status_code == 400


def test_produccion_crea_retazo_de_tela_solo_si_supera_80_por_80(client, auth):
    tela = _insumo(stock=10, ancho=300)
    crear_receta(1, [{'id_insumo': tela.id, 'nombre': 'Tela', 'tipo_calculo': 'lineal_alto'}])
    respuesta = client.post('/api/recipes/1/produce', headers=auth('taller'), json={'w': 150, 'h': 120})
    assert respuesta.status_code == 200, respuesta.get_json()
    assert respuesta.get_json()['retazos_tela_generados'] == 1
    retazo = RetazoTela.query.one()
    assert float(retazo.ancho_cm) == 150 and float(retazo.largo_cm) == 120
    assert retazo.estado == 'disponible' and 'Producto 1' in retazo.referencia
    siguiente = client.get('/api/recipes/1/explosion?w=100&h=120', headers=auth('ventas')).get_json()
    assert siguiente['explosion'][0]['metodo'] == 'RETAZO'


def test_retazo_de_80_cm_no_se_guarda_y_el_retazo_disponible_se_lista(client, auth):
    tela = _insumo(stock=10, ancho=230)
    crear_receta(1, [{'id_insumo': tela.id, 'nombre': 'Tela', 'tipo_calculo': 'lineal_alto'}])
    respuesta = client.post('/api/recipes/1/produce', headers=auth('taller'), json={'w': 150, 'h': 120})
    assert respuesta.status_code == 200
    assert respuesta.get_json()['retazos_tela_generados'] == 0
    assert RetazoTela.query.count() == 0

    retazo = RetazoTela(id_insumo_base=tela.id, ancho_cm=90, largo_cm=100, estado='disponible')
    db.session.add(retazo)
    db.session.commit()
    listado = client.get('/api/inventory/scraps', headers=auth('ventas')).get_json()
    assert len(listado) == 1 and listado[0]['insumo'] == 'Blackout'


def test_reservar_retazo_lo_aparta_de_otros_presupuestos(client, auth):
    tela = _insumo(stock=10, ancho=300)
    retazo = RetazoTela(id_insumo_base=tela.id, ancho_cm=150, largo_cm=130, estado='disponible')
    db.session.add(retazo)
    db.session.commit()
    crear_receta(1, [{'id_insumo': tela.id, 'nombre': 'Tela', 'tipo_calculo': 'lineal_alto'}])
    h = auth('taller')
    reservado = client.post(f'/api/inventory/scraps/{retazo.id}/reserve', headers=h,
                            json={'referencia': 'PED-100'})
    assert reservado.status_code == 200 and reservado.get_json()['estado'] == 'reservado'
    sin_ref = client.get('/api/recipes/1/explosion?w=100&h=120', headers=h).get_json()
    con_ref = client.get('/api/recipes/1/explosion?w=100&h=120&referencia=PED-100', headers=h).get_json()
    assert sin_ref['explosion'][0]['metodo'] == 'ROLLO'
    assert con_ref['explosion'][0]['metodo'] == 'RETAZO'
    assert client.post(f'/api/inventory/scraps/{retazo.id}/reserve', headers=h,
                       json={'referencia': 'PED-200'}).status_code == 409


def test_produccion_con_referencia_usa_y_cierra_su_reserva(client, auth):
    tela = _insumo(stock=10, ancho=300)
    retazo = RetazoTela(id_insumo_base=tela.id, ancho_cm=150, largo_cm=130, estado='disponible')
    db.session.add(retazo)
    db.session.commit()
    crear_receta(1, [{'id_insumo': tela.id, 'nombre': 'Tela', 'tipo_calculo': 'lineal_alto'}])
    h = auth('taller')
    assert client.post(f'/api/inventory/scraps/{retazo.id}/reserve', headers=h,
                       json={'referencia': 'PED-100'}).status_code == 200
    r = client.post('/api/recipes/1/produce', headers=h, json={
        'w': 100, 'h': 120, 'referencia': 'PED-100',
    })
    assert r.status_code == 200, r.get_json()
    assert r.get_json()['retazos_usados'] == [retazo.id]
    assert db.session.get(RetazoTela, retazo.id).estado == 'usado'
    db.session.refresh(tela)
    assert float(tela.stock_actual) == 10


def test_liberar_reserva_retorna_el_retazo_a_disponible(client, auth):
    tela = _insumo()
    retazo = RetazoTela(id_insumo_base=tela.id, ancho_cm=100, largo_cm=100, estado='disponible')
    db.session.add(retazo)
    db.session.commit()
    h = auth('admin')
    assert client.post(f'/api/inventory/scraps/{retazo.id}/reserve', headers=h,
                       json={'referencia': 'PED-1'}).status_code == 200
    liberado = client.post(f'/api/inventory/scraps/{retazo.id}/release', headers=h)
    assert liberado.status_code == 200
    assert liberado.get_json()['estado'] == 'disponible'
    assert liberado.get_json()['referencia'] is None


def test_no_reserva_referencia_vacia(client, auth):
    tela = _insumo()
    retazo = RetazoTela(id_insumo_base=tela.id, ancho_cm=100, largo_cm=100, estado='disponible')
    db.session.add(retazo)
    db.session.commit()
    r = client.post(f'/api/inventory/scraps/{retazo.id}/reserve', headers=auth('admin'),
                    json={'referencia': '   '})
    assert r.status_code == 400
