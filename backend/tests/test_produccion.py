from extensions import db
from models import RetazoTela, Supply, SupplyCategory
from tests.helpers import crear_receta


def _seed(stock=50):
    cat = SupplyCategory(name="Telas")
    db.session.add(cat)
    db.session.flush()
    tela = Supply(categoria_id=cat.id, name="Blackout", unidad_medida="metro",
                  precio_costo_unitario=15000, stock_actual=stock, ancho_cm=210)
    cadena = Supply(categoria_id=cat.id, name="Cadena", unidad_medida="unidad",
                    precio_costo_unitario=500, stock_actual=10)
    db.session.add_all([tela, cadena])
    db.session.flush()
    crear_receta(1, [
        dict(id_insumo=tela.id, nombre="Tela", tipo_calculo="lineal_alto"),
        dict(id_insumo=cadena.id, nombre="Cadena", tipo_calculo="fijo", cantidad_base=2),
    ])
    return tela, cadena


def test_producir_descuenta_stock(client, auth):
    tela, cadena = _seed()
    r = client.post("/api/recipes/1/produce", json={"w": 150, "h": 200}, headers=auth("taller"))
    assert r.status_code == 200, r.get_json()
    db.session.expire_all()
    assert float(db.session.get(Supply, tela.id).stock_actual) == 48.0
    assert float(db.session.get(Supply, cadena.id).stock_actual) == 8.0


def test_producir_con_retazo_no_toca_rollo_y_lo_marca_usado(client, auth):
    tela, cadena = _seed()
    retazo = RetazoTela(id_insumo_base=tela.id, ancho_cm=160, largo_cm=210)
    db.session.add(retazo)
    db.session.commit()
    r = client.post("/api/recipes/1/produce", json={"w": 150, "h": 200}, headers=auth("admin"))
    assert r.status_code == 200
    db.session.expire_all()
    assert float(db.session.get(Supply, tela.id).stock_actual) == 50.0
    assert db.session.get(RetazoTela, retazo.id).estado == "usado"
    # el retazo ya no está disponible: la segunda producción usa rollo
    again = client.post("/api/recipes/1/produce", json={"w": 150, "h": 200}, headers=auth("admin"))
    assert again.status_code == 200
    db.session.expire_all()
    assert float(db.session.get(Supply, tela.id).stock_actual) == 48.0


def test_producir_sin_stock_no_descuenta_nada(client, auth):
    tela, cadena = _seed(stock=1)
    r = client.post("/api/recipes/1/produce", json={"w": 150, "h": 200}, headers=auth("taller"))
    assert r.status_code == 409
    assert r.get_json()["detalles"]
    db.session.expire_all()
    assert float(db.session.get(Supply, cadena.id).stock_actual) == 10.0
    assert float(db.session.get(Supply, tela.id).stock_actual) == 1.0


def test_producir_permisos_y_validacion(client, auth):
    _seed()
    assert client.post("/api/recipes/1/produce", json={"w": 150, "h": 200}, headers=auth("ventas")).status_code == 403
    assert client.post("/api/recipes/1/produce", json={"w": 150, "h": 200}).status_code == 401
    h = auth("taller")
    assert client.post("/api/recipes/1/produce", json={}, headers=h).status_code == 400
    assert client.post("/api/recipes/1/produce", json={"w": -1, "h": 5}, headers=h).status_code == 400
    assert client.post("/api/recipes/99/produce", json={"w": 10, "h": 10}, headers=h).status_code == 404
