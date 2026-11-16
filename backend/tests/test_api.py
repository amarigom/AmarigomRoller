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
    r = client.get("/api/test-recipe/1?w=150&h=200", headers=auth("admin"))
    assert r.status_code == 200
    data = r.get_json()
    assert data["total_materiales"] == 30200.0
    assert data["explosion"][0]["consumo_m_o_m2"] == 2.0


def test_explosion_alias_canonico(client, auth):
    _seed_receta()
    r = client.get("/api/recipes/1/explosion?w=150&h=200", headers=auth("taller"))
    assert r.get_json()["explosion"][0]["consumo_m_o_m2"] == 2.0
    assert "total_materiales" not in r.get_json()


def test_cotizacion_incluye_costos_y_colocacion_separada(client, auth, app):
    tela = _seed_receta()
    receta = crear_receta(2, [dict(id_insumo=tela.id, nombre="Tela", tipo_calculo="lineal_alto",
                                   minutos_mano_obra=5)])
    app.config.update(COSTO_MINUTO_MANO_OBRA=1000, TARIFA_BASE_COLOCACION='8000', COSTO_POR_KM='450')
    r = client.post("/api/quotes/calculate", json={
        "receta_id": receta.id, "ancho": 150, "alto": 100, "km_obra": 15,
    }, headers=auth("admin"))
    assert r.status_code == 200
    body = r.get_json()
    assert body["receta_id"] == receta.id
    data = body["resultado"]
    assert data["desglose_fabricacion"] == {
        "costo_materiales": 15200, "costo_operaciones": 5000, "costo_desgaste": 2000,
        "costo_total_fabricacion": 22200,
    }
    assert data["precio_producto"] == {
        "markup_pct": 100, "ganancia_markup": 22200, "margen_sobre_ventas_pct": 50,
        "precio_venta_final": 44400,
    }
    assert data["servicio_colocacion"] == {
        "tarifa_base": 8000, "km_ida": 15, "km_totales": 30, "costo_traslado": 13500,
        "total_colocacion": 21500,
    }
    assert data["total_presupuesto"] == 65900
    assert float(tela.stock_actual) == 50


@pytest.mark.parametrize("km", [-1, "nan", "inf", "abc", "1.234", ""])
def test_cotizacion_rechaza_distancia_invalida(client, auth, km):
    _seed_receta()
    r = client.post("/api/quotes/calculate", json={
        "receta_id": 1, "ancho": 150, "alto": 200, "km_obra": km,
    }, headers=auth("ventas"))
    assert r.status_code == 400


def test_cotizacion_con_retazo_y_permiso(client, auth):
    tela = _seed_receta()
    db.session.add(RetazoTela(id_insumo_base=tela.id, ancho_cm=160, largo_cm=210))
    db.session.commit()
    assert client.post("/api/quotes/calculate", json={"receta_id": 1, "ancho": 150, "alto": 200}).status_code == 401
    data = client.get("/api/recipes/1/quote?w=150&h=200", headers=auth("admin")).get_json()
    assert data["total"] == 2200
    assert data["precio_producto"]["precio_venta_final"] == 4400
    assert data["precio_producto"]["margen_sobre_ventas_pct"] == 50
    assert data["servicio_colocacion"]["costo_traslado"] == 0
    assert data["total_presupuesto"] == 4400 + data["servicio_colocacion"]["tarifa_base"]


def test_etiqueta_actualiza_precio_y_no_puede_archivarse(client, auth):
    _seed_receta()
    etiqueta = Supply.query.filter_by(codigo_sku='ROLLER-ETIQUETA').one()
    h = auth("admin")
    assert client.delete(f"/api/inventory/{etiqueta.id}", headers=h).status_code == 409
    response = client.post("/api/inventory/prices", headers=h, json={
        "items": [{"id_insumo": etiqueta.id, "precio": 300}],
    })
    assert response.status_code == 200
    data = client.get("/api/recipes/1/quote?w=150&h=100", headers=h).get_json()
    assert data["total_materiales"] == 15300
    assert data["precio_producto"]["precio_venta_final"] == 34600


def test_receta_rechaza_etiqueta_explicita_para_evitar_duplicados(client, auth):
    _seed_receta()
    etiqueta = Supply.query.filter_by(codigo_sku='ROLLER-ETIQUETA').one()
    response = client.post("/api/recipes/1/versions", headers=auth("admin"), json={
        "items": [{"id_insumo": etiqueta.id, "nombre": "Etiqueta", "tipo_calculo": "fijo"}],
    })
    assert response.status_code == 400
    assert "automáticamente" in str(response.get_json())


def test_cotizacion_redondea_centavos(client, auth):
    tela = _seed_receta()
    tela.precio_costo_unitario = 100.01
    db.session.commit()
    data = client.get("/api/recipes/1/quote?w=150&h=100", headers=auth("admin")).get_json()
    assert (data["total"], data["precio_producto"]["precio_venta_final"],
            data["precio_producto"]["ganancia_markup"]) == (2300.01, 4600.02, 2300.01)


def test_cotizacion_por_id_respeta_version_y_tarifas_configurables(client, auth, app):
    tela = _seed_receta()
    primera = crear_receta(2, [dict(id_insumo=tela.id, nombre="Tela", tipo_calculo="lineal_alto")])
    segunda = crear_receta(2, [dict(id_insumo=tela.id, nombre="Tela", tipo_calculo="lineal_alto",
                                    delta_alto_cm=100)], version=2)
    app.config.update(TARIFA_BASE_COLOCACION='100', COSTO_POR_KM='2.5')
    headers = auth("admin")
    resultados = []
    for receta in (primera, segunda):
        response = client.post("/api/quotes/calculate", headers=headers, json={
            "receta_id": receta.id, "ancho": 150, "alto": 100, "km_obra": 1.5,
        })
        assert response.status_code == 200
        resultados.append(response.get_json()["resultado"])
    assert [r["version"] for r in resultados] == [1, 2]
    assert [r["total"] for r in resultados] == [17200, 32200]
    assert resultados[0]["servicio_colocacion"]["total_colocacion"] == 107.5
    assert client.post("/api/quotes/calculate", headers=headers, json={
        "receta_id": 999, "ancho": 150, "alto": 100,
    }).status_code == 404
    assert client.post("/api/quotes/calculate", headers=headers, json={
        "receta_id": primera.id, "ancho": 150, "alto": 100, "markup_pct": 0,
    }).status_code == 400


def test_cotizacion_valida_medidas_y_opciones(client, auth):
    tela = _seed_receta()
    receta = crear_receta(2, [dict(
        id_insumo=tela.id, nombre="Tela", tipo_calculo="lineal_alto", condicion="sistema == 'motor'",
    )])
    headers = auth("ventas")
    for datos in (
        {"receta_id": receta.id, "alto": 100},
        {"receta_id": receta.id, "ancho": 0, "alto": 100},
        {"receta_id": receta.id, "ancho": 100, "alto": "nan"},
        {"receta_id": 0, "ancho": 100, "alto": 100},
    ):
        assert client.post("/api/quotes/calculate", headers=headers, json=datos).status_code == 400
    response = client.post("/api/quotes/calculate", headers=headers, json={
        "receta_id": receta.id, "ancho": 100, "alto": 100, "opciones": {"sistema": "motor"},
    })
    assert response.status_code == 200
    assert response.get_json()["resultado"]["precio_producto"]["precio_venta_final"] == 34400
    response = client.get("/api/recipes/2/quote?w=100&h=100&sistema=motor&km_obra=2", headers=headers)
    assert response.status_code == 200
    assert response.get_json()["precio_producto"]["precio_venta_final"] == 34400
    assert client.get("/api/recipes/2/quote?w=100&h=100&markup_pct=0", headers=headers).status_code == 400


def test_receta_usa_retazo(client, auth):
    tela = _seed_receta()
    db.session.add(RetazoTela(id_insumo_base=tela.id, ancho_cm=160, largo_cm=210))
    db.session.commit()
    data = client.get("/api/test-recipe/1?w=150&h=200", headers=auth("admin")).get_json()
    assert data["explosion"][0]["metodo"] == "RETAZO"
    assert data["total_materiales"] == 200.0


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
    assert len(client.get("/api/inventory", headers=h).get_json()) == 4
    assert len(client.get("/api/inventory?limit=2", headers=h).get_json()) == 2


def test_eliminar_insumo(client, auth):
    h = auth("admin")
    assert client.delete("/api/inventory/999", headers=h).status_code == 404
    cat = SupplyCategory(name="Telas")
    db.session.add(cat)
    db.session.commit()
    nuevo = client.post("/api/inventory", json={"name": "T", "categoria_id": cat.id}, headers=h).get_json()
    assert client.delete(f"/api/inventory/{nuevo['id']}", headers=h).status_code == 200
    assert [s["name"] for s in client.get("/api/inventory", headers=h).get_json()] == ["Etiqueta"]
    assert client.get(f"/api/inventory/{nuevo['id']}/movements", headers=h).get_json()


def test_archivar_insumo_con_stock_es_rechazado(client, auth):
    h = auth("admin")
    cat = SupplyCategory(name="Telas")
    db.session.add(cat)
    db.session.commit()
    nuevo = client.post("/api/inventory", json={
        "name": "T", "categoria_id": cat.id, "stock_actual": 5,
    }, headers=h).get_json()
    assert client.delete(f"/api/inventory/{nuevo['id']}", headers=h).status_code == 409
    assert len(client.get("/api/inventory", headers=h).get_json()) == 2


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
