from models import InventoryMovement, PiezaStock, Product, Supply


def test_demo_es_explicito_y_no_duplica(app, client, auth):
    runner = app.test_cli_runner()
    simulacion = runner.invoke(args=['seed-demo-fabricacion'])
    assert simulacion.exit_code == 0
    assert Supply.query.filter_by(codigo_sku='DEMO-TELA-300').first() is None
    resultado = runner.invoke(args=['seed-demo-fabricacion', '--apply'])
    assert resultado.exit_code == 0, resultado.output
    tela = Supply.query.filter_by(codigo_sku='DEMO-TELA-300').one()
    perfil = Supply.query.filter_by(codigo_sku='DEMO-PERFIL-400').one()
    assert (float(tela.stock_actual), tela.precio_m2, float(tela.ancho_cm)) == (30, None, 300)
    assert PiezaStock.query.filter_by(id_insumo=perfil.id, es_retazo=False).count() == 3
    assert InventoryMovement.query.filter_by(id_insumo=perfil.id).count() == 1
    roller = Product.query.filter_by(nombre='DEMO Roller').one()
    response = client.post(f'/api/recipes/{roller.id}/produce', headers=auth('taller'),
                           json={'w': 150, 'h': 200})
    assert response.status_code == 200, response.get_json()
    assert runner.invoke(args=['seed-demo-fabricacion', '--apply']).exit_code != 0
    assert Supply.query.filter_by(codigo_sku='DEMO-TELA-300').count() == 1
