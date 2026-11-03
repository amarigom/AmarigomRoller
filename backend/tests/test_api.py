import pytest

from extensions import db
from models import RetazoTela, Supply, SupplyCategory
from tests.helpers import crear_receta


def _seed_receta():
    cat = SupplyCategory(name="Telas")
    db.session.add(cat)
    db.session.flush()
    tela = Supply(categoria_id=cat.id, name="Blackout", unidad_medida="metro",
                  precio_costo_unitario=15000, stock_actual=50, ancho_cm=210)
    db.session.add(tela)
    db.session.flush()
    crear_receta(1, [dict(id_insumo=tela.id, nombre="Tela", tipo_calculo="lineal_alto")])
    return tela


def test_receta_calcula_costo_en_metros(client, auth):
    _seed_receta()
    r = client.get("/api/test-recipe/1?w=150&h=200", headers=auth("ventas"))
    assert r.status_code == 200
    data = r.get_json()
    assert data["total_materiales"] == 30000.0
    assert data["explosion"][0]["consumo_m_o_m2"] == 2.0


def test_explosion_alias_canonico(client, auth):
    _seed_receta()
    r = client.get("/api/recipes/1/explosion?w=150&h=200", headers=auth("taller"))
    assert r.get_json()["total_materiales"] == 30000.0


def test_receta_usa_retazo(client, auth):
    tela = _seed_receta()
    db.session.add(RetazoTela(id_insumo_base=tela.id, ancho_cm=160, largo_cm=210))
    db.session.commit()
    data = client.get("/api/test-recipe/1?w=150&h=200", headers=auth("admin")).get_json()
    assert data["explosion"][0]["metodo"] == "RETAZO"
    assert data["total_materiales"] == 0.0


def test_receta_tipo_de_calculo_desconocido(client, auth):
    tela = _seed_receta()
    crear_receta(2, [dict(id_insumo=tela.id, nombre="X", tipo_calculo="inventado")])
    assert client.get("/api/test-recipe/2", headers=auth("admin")).status_code == 422


def test_receta_medidas_invalidas_y_sin_receta(client, auth):
    h = auth("admin")
    assert client.get("/api/test-recipe/1?w=abc", headers=h).status_code == 400
    assert client.get("/api/test-recipe/1?w=-5", headers=h).status_code == 400
    assert client.get("/api/test-recipe/99", headers=h).status_code == 404


def test_inventario_valida_y_pagina(client, auth):
    h = auth("admin")
    cat = SupplyCategory(name="Telas")
    db.session.add(cat)
    db.session.commit()

    malo = client.post("/api/inventory", json={"name": "X", "categoria_id": cat.id, "stock_actual": -1}, headers=h)
    assert malo.status_code == 400
    assert client.post("/api/inventory", json={"name": "X", "categoria_id": 999}, headers=h).status_code == 404

    for i in range(3):
        ok = client.post("/api/inventory", json={"name": f"T{i}", "codigo_sku": f"S{i}",
                                                 "categoria_id": cat.id, "stock_actual": 10}, headers=h)
        assert ok.status_code == 201
        assert ok.get_json()["category"] == "Telas"

    dup = client.post("/api/inventory", json={"name": "T", "codigo_sku": "S0", "categoria_id": cat.id}, headers=h)
    assert dup.status_code == 409
    assert len(client.get("/api/inventory", headers=h).get_json()) == 3
    assert len(client.get("/api/inventory?limit=2", headers=h).get_json()) == 2


def test_eliminar_insumo(client, auth):
    h = auth("admin")
    assert client.delete("/api/inventory/999", headers=h).status_code == 404
    cat = SupplyCategory(name="Telas")
    db.session.add(cat)
    db.session.commit()
    nuevo = client.post("/api/inventory", json={"name": "T", "categoria_id": cat.id}, headers=h).get_json()
    assert client.delete(f"/api/inventory/{nuevo['id']}", headers=h).status_code == 200


def test_clientes_validacion(client, auth):
    h = auth("ventas")
    assert client.post("/api/clients", json={"nombre": "A", "apellido": "B", "email": "no-es-mail"}, headers=h).status_code == 400
    ok = {"nombre": "Ana", "apellido": "Gomez", "email": "ana@example.com"}
    assert client.post("/api/clients", json=ok, headers=h).status_code == 201
    assert client.post("/api/clients", json=ok, headers=h).status_code == 409


def test_presupuesto_publico_escapa_html(client, app):
    r = client.post("/api/presupuesto", json={
        "email": "cli@example.com", "width": 100, "height": 120,
        "observations": "<script>alert(1)</script>"})
    assert r.status_code == 200
    asunto, html, destino = app.extensions["notifier"].sent[0]
    assert destino == "taller@example.com"
    assert "<script>" not in html and "&lt;script&gt;" in html


def test_presupuesto_invalido(client):
    assert client.post("/api/presupuesto", json={"email": "x", "width": 0, "height": 5}).status_code == 400


def test_presupuesto_falla_proveedor_devuelve_502(client, app):
    from exceptions import ExternalServiceError

    class Roto:
        def send(self, *a):
            raise ExternalServiceError()

    app.extensions["notifier"] = Roto()
    r = client.post("/api/presupuesto", json={"email": "c@example.com", "width": 10, "height": 10})
    assert r.status_code == 502
