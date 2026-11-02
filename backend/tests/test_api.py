import os
import sys
import tempfile

import pytest

os.environ["DATABASE_URL"] = "sqlite:///" + os.path.join(tempfile.mkdtemp(), "test.db")
os.environ["SECRET_KEY"] = "test"
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app as flask_app  # noqa: E402
from models import db, SupplyCategory, Supply, RecipeBOM, RetazoTela  # noqa: E402


@pytest.fixture()
def client():
    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        yield flask_app.test_client()
        db.session.remove()


def _seed_receta():
    cat = SupplyCategory(name="Telas")
    db.session.add(cat)
    db.session.flush()
    tela = Supply(categoria_id=cat.id, name="Blackout", unidad_medida="metro",
                  precio_costo_unitario=15000, stock_actual=50, ancho_cm=210)
    db.session.add(tela)
    db.session.flush()
    db.session.add(RecipeBOM(id_padre=1, id_insumo=tela.id, nombre_producto="Tela",
                             tipo_calculo="lineal_alto"))
    db.session.commit()
    return tela


def test_receta_calcula_costo_en_metros(client):
    _seed_receta()
    r = client.get("/api/test-recipe/1?w=150&h=200")
    assert r.status_code == 200
    data = r.get_json()
    assert data["total_materiales"] == 30000.0
    assert data["explosion"][0]["consumo_m_o_m2"] == 2.0


def test_receta_usa_retazo(client):
    tela = _seed_receta()
    db.session.add(RetazoTela(id_insumo_base=tela.id, ancho_cm=160, largo_cm=210))
    db.session.commit()
    data = client.get("/api/test-recipe/1?w=150&h=200").get_json()
    assert data["explosion"][0]["metodo"] == "RETAZO"
    assert data["total_materiales"] == 0.0


def test_receta_medidas_invalidas_y_sin_receta(client):
    assert client.get("/api/test-recipe/1?w=abc").status_code == 400
    assert client.get("/api/test-recipe/1?w=-5").status_code == 400
    assert client.get("/api/test-recipe/99").status_code == 404


def test_inventario_valida_y_pagina(client):
    cat = SupplyCategory(name="Telas")
    db.session.add(cat)
    db.session.commit()

    malo = client.post("/api/inventory", json={"name": "X", "categoria_id": cat.id, "stock_actual": -1})
    assert malo.status_code == 400

    for i in range(3):
        ok = client.post("/api/inventory", json={"name": f"T{i}", "codigo_sku": f"S{i}",
                                                 "categoria_id": cat.id, "stock_actual": 10})
        assert ok.status_code == 201

    dup = client.post("/api/inventory", json={"name": "T", "codigo_sku": "S0", "categoria_id": cat.id})
    assert dup.status_code == 409
    assert len(client.get("/api/inventory").get_json()) == 3
    assert len(client.get("/api/inventory?limit=2").get_json()) == 2


def test_eliminar_insumo_inexistente(client):
    assert client.delete("/api/inventory/999").status_code == 404


def test_clientes_validacion(client):
    assert client.post("/api/clients", json={"nombre": "A", "apellido": "B", "email": "no-es-mail"}).status_code == 400
    ok = {"nombre": "Ana", "apellido": "Gomez", "email": "ana@example.com"}
    assert client.post("/api/clients", json=ok).status_code == 201
    assert client.post("/api/clients", json=ok).status_code == 409
