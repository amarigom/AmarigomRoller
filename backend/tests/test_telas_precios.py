from extensions import db
from models import RetazoTela, Supply, SupplyCategory
from tests.helpers import crear_receta


def _tela():
    categoria = SupplyCategory(name='Telas de prueba')
    db.session.add(categoria)
    db.session.flush()
    tela = Supply(categoria_id=categoria.id, name='Tela', unidad_medida='metro',
                  precio_costo_unitario=3000, precio_m2=1200, ancho_cm=300,
                  largo_pieza_cm=3000, es_tela=True, stock_actual=30,
                  unidad_compra='rollo', factor_conversion=30)
    db.session.add(tela)
    db.session.commit()
    return tela


def test_roller_cobra_superficie_con_merma_y_descontara_largo_sin_merma(client, auth):
    tela = _tela()
    crear_receta(1, [{'id_insumo': tela.id, 'nombre': 'Tela', 'tipo_calculo': 'superficie', 'merma_pct': 5}])
    headers = auth('taller')
    admin = auth('admin')
    quote = client.get('/api/recipes/1/quote?w=150&h=200', headers=admin).get_json()
    item = quote['explosion'][0]
    assert (item['consumo_m_o_m2'], item['unidad'], item['cantidad_costo'], item['unidad_costo']) == (2, 'metro', 3.15, 'm2')
    assert item['costo_parcial'] == 3780
    r = client.post('/api/recipes/1/produce', headers=headers, json={'w': 150, 'h': 200})
    assert r.status_code == 200, r.get_json()
    db.session.refresh(tela)
    assert float(tela.stock_actual) == 28
    retazo = RetazoTela.query.one()
    assert (float(retazo.ancho_cm), float(retazo.largo_cm)) == (150, 200)
    segundo = client.get('/api/recipes/1/quote?w=100&h=150', headers=admin).get_json()['explosion'][0]
    assert (segundo['metodo'], segundo['consumo_m_o_m2'], segundo['cantidad_costo'], segundo['costo_parcial']) == ('RETAZO', 0, 0, 0)


def test_tradicional_usa_precio_metro_lineal(client, auth):
    tela = _tela()
    crear_receta(1, [{'id_insumo': tela.id, 'nombre': 'Tela', 'tipo_calculo': 'lineal_alto', 'merma_pct': 5}])
    item = client.get('/api/recipes/1/explosion?w=150&h=200', headers=auth('admin')).get_json()['explosion'][0]
    assert (item['consumo_m_o_m2'], item['cantidad_costo'], item['unidad_costo'], item['costo_parcial']) == (2, 2.1, 'metro', 6300)


def test_tela_lineal_cobra_retazo_sin_descontar_rollo(client, auth):
    tela = _tela()
    tela.precio_m2 = None
    db.session.add(RetazoTela(id_insumo_base=tela.id, ancho_cm=180, largo_cm=220, estado='disponible'))
    db.session.commit()
    crear_receta(1, [{'id_insumo': tela.id, 'nombre': 'Tela', 'tipo_calculo': 'lineal_alto', 'merma_pct': 5}])
    headers = auth('taller')
    admin = auth('admin')
    resultado = client.get('/api/recipes/1/quote?w=150&h=200', headers=admin)
    datos = resultado.get_json()
    item = datos['explosion'][0]
    assert (item['metodo'], item['consumo_m_o_m2'], item['cantidad_costo'], item['costo_parcial']) == ('RETAZO', 0, 0, 0)
    assert (item['cantidad_reposicion'], item['costo_reposicion']) == (2.1, 6300)
    assert datos['desglose_fabricacion']['costo_total_fabricacion'] == 2200
    assert datos['precio_producto']['precio_venta_final'] == 17000
    assert datos['precio_producto']['ganancia_markup'] == 14800
    retazo = RetazoTela.query.one()
    retazo.estado = 'reservado'
    db.session.commit()
    con_rollo = client.get('/api/recipes/1/quote?w=150&h=200', headers=admin).get_json()
    assert con_rollo['precio_producto']['precio_venta_final'] == datos['precio_producto']['precio_venta_final']
    retazo.estado = 'disponible'
    db.session.commit()
    producido = client.post('/api/recipes/1/produce', headers=headers, json={'w': 150, 'h': 200})
    assert producido.status_code == 200, producido.get_json()
    db.session.refresh(tela)
    assert tela.stock_actual == 30
    db.session.refresh(retazo)
    assert retazo.estado == 'usado'


def test_csv_lineal_no_borra_precio_historico_m2(client, auth):
    tela = _tela()
    csv = f'id_insumo;precio_metro\n{tela.id};3500,50\n'
    h = auth('admin')
    assert client.post('/api/inventory/prices/fabrics/import', headers=h, json={'csv': csv}).status_code == 200
    assert client.post('/api/inventory/prices/fabrics/import', headers=h, json={'csv': csv, 'aplicar': True}).status_code == 200
    db.session.refresh(tela)
    assert (float(tela.precio_costo_unitario), float(tela.precio_m2)) == (3500.5, 1200)


def test_configuracion_de_tela_conserva_precio_historico_si_no_se_envia(client, auth):
    tela = _tela()
    response = client.patch(f'/api/inventory/{tela.id}/fabric', headers=auth('admin'), json={'ancho_cm': 300})
    assert response.status_code == 200
    db.session.refresh(tela)
    assert float(tela.precio_m2) == 1200


def test_tela_lineal_rechaza_ancho_mayor_que_rollo(client, auth):
    tela = _tela()
    crear_receta(1, [{'id_insumo': tela.id, 'nombre': 'Tela', 'tipo_calculo': 'lineal_alto'}])
    response = client.get('/api/recipes/1/quote?w=301&h=200', headers=auth('ventas'))
    assert response.status_code == 422
    assert 'ancho' in response.get_json()['message']


def test_superficie_exige_precio_y_ancho_suficiente(client, auth):
    tela = _tela()
    crear_receta(1, [{'id_insumo': tela.id, 'nombre': 'Tela', 'tipo_calculo': 'superficie'}])
    h = auth('ventas')
    assert client.get('/api/recipes/1/explosion?w=301&h=200', headers=h).status_code == 422
    tela.precio_m2 = None
    db.session.commit()
    assert client.get('/api/recipes/1/explosion?w=150&h=200', headers=h).status_code == 422


def test_importacion_csv_precios_tela_es_atomica(client, auth):
    tela = _tela()
    h = auth('admin')
    csv = f'id_insumo;precio_metro;precio_m2\n{tela.id};3500,50;1400,25\n'
    preview = client.post('/api/inventory/prices/fabrics/import', headers=h, json={'csv': csv})
    assert preview.status_code == 200 and not preview.get_json()['aplicado']
    db.session.refresh(tela)
    assert float(tela.precio_m2) == 1200
    bad = client.post('/api/inventory/prices/fabrics/import', headers=h, json={
        'csv': csv + '999;20;10\n', 'aplicar': True,
    })
    assert bad.status_code == 400
    db.session.refresh(tela)
    assert float(tela.precio_m2) == 1200
    applied = client.post('/api/inventory/prices/fabrics/import', headers=h, json={'csv': csv, 'aplicar': True})
    assert applied.status_code == 200 and applied.get_json()['actualizados'] == 1
    db.session.refresh(tela)
    assert (float(tela.precio_costo_unitario), float(tela.precio_m2)) == (3500.5, 1400.25)


def test_compra_de_rollos_convierte_a_metros_sin_permitir_fracciones(client, auth):
    tela = _tela()
    h = auth('taller')
    url = f'/api/inventory/{tela.id}/purchases'
    assert client.post(url, headers=h, json={'cantidad': 0.5}).status_code == 400
    r = client.post(url, headers=h, json={'cantidad': 2, 'referencia': 'Compra demo'})
    assert r.status_code == 201
    assert (r.get_json()['cantidad'], r.get_json()['stock_resultante']) == (60, 90)
    db.session.refresh(tela)
    assert float(tela.stock_actual) == 90
