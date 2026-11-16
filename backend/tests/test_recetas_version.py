import importlib
import os
from datetime import datetime, timedelta, timezone

import sqlalchemy as sa
from alembic import command
from alembic.config import Config

from extensions import db
from factory import create_app
from models import PiezaStock, Receta, Supply, SupplyCategory
from tests.helpers import crear_receta

MIGRACIONES = os.path.join(os.path.dirname(os.path.dirname(__file__)), "migrations")


def _insumos():
    cat = SupplyCategory(name="Varios")
    db.session.add(cat)
    db.session.flush()
    tubo = Supply(categoria_id=cat.id, name="Tubo 4 mts", unidad_medida="cm", precio_costo_unitario=50,
                  stock_actual=2000, largo_pieza_cm=400)
    soporte = Supply(categoria_id=cat.id, name="Soporte central", unidad_medida="unidad",
                     precio_costo_unitario=1000, stock_actual=20)
    cadena = Supply(categoria_id=cat.id, name="Cadena", unidad_medida="metro", precio_costo_unitario=200,
                    stock_actual=50)
    db.session.add_all([tubo, soporte, cadena])
    db.session.flush()
    db.session.add_all([PiezaStock(id_insumo=tubo.id, longitud_original_cm=400,
                                  longitud_actual_cm=400, es_retazo=False) for _ in range(5)])
    db.session.commit()
    return tubo, soporte, cadena


def _item(insumo, **extra):
    return {"id_insumo": insumo.id, "nombre": insumo.name, **extra}


# --- Condiciones y fórmulas -----------------------------------------------------------------

def test_componente_condicional_por_ancho(client, auth):
    tubo, soporte, _ = _insumos()
    crear_receta(1, [
        _item(tubo, tipo_calculo="perfil", delta_ancho_cm=-1.5),
        _item(soporte, tipo_calculo="fijo", condicion="ancho > 200"),
    ])
    h = auth("admin")
    angosto = client.get("/api/test-recipe/1?w=150&h=200", headers=h).get_json()
    ancho = client.get("/api/test-recipe/1?w=250&h=200", headers=h).get_json()
    assert [e["componente"] for e in angosto["explosion"]] == ["Tubo 4 mts", "Etiqueta"]
    assert [e["componente"] for e in ancho["explosion"]] == ["Tubo 4 mts", "Soporte central", "Etiqueta"]
    assert ancho["total_materiales"] == angosto["total_materiales"] + 100 * 0 + 1000 + (250 - 150) * 50


def test_variante_por_opcion_sistema(client, auth):
    tubo, _, cadena = _insumos()
    crear_receta(1, [
        _item(tubo, tipo_calculo="perfil"),
        _item(cadena, tipo_calculo="lineal_alto", condicion="sistema == 'cadena'"),
    ])
    h = auth("ventas")
    con = client.get("/api/test-recipe/1?w=150&h=200&sistema=cadena", headers=h).get_json()
    sin = client.get("/api/test-recipe/1?w=150&h=200&sistema=motor", headers=h).get_json()
    sin_opcion = client.get("/api/test-recipe/1?w=150&h=200", headers=h).get_json()
    assert len(con["explosion"]) == 3 and len(sin["explosion"]) == 2 and len(sin_opcion["explosion"]) == 2


def test_formulas_de_medida_y_cantidad(client, auth):
    tubo, soporte, _ = _insumos()
    crear_receta(1, [
        _item(tubo, tipo_calculo="perfil", formula_ancho="ancho - 3"),
        _item(soporte, tipo_calculo="fijo", formula_cantidad="ceil(ancho / 100)"),
    ])
    data = client.get("/api/test-recipe/1?w=250&h=200", headers=auth("admin")).get_json()
    tubo_r, soporte_r, etiqueta_r = data["explosion"]
    assert etiqueta_r["costo_parcial"] == 200
    assert tubo_r["consumo_m_o_m2"] == 247
    assert soporte_r["consumo_m_o_m2"] == 3 and soporte_r["costo_parcial"] == 3000


def test_formula_rota_en_la_base_da_422_claro(client, auth):
    _, soporte, _ = _insumos()
    crear_receta(1, [_item(soporte, tipo_calculo="fijo", formula_cantidad="ancho / 0")])
    r = client.get("/api/test-recipe/1?w=150&h=200", headers=auth("ventas"))
    assert r.status_code == 422 and "División por cero" in r.get_json()["message"]


def test_producir_ignora_los_componentes_condicionales_que_no_aplican(client, auth):
    tubo, soporte, _ = _insumos()
    crear_receta(1, [
        _item(tubo, tipo_calculo="perfil"),
        _item(soporte, tipo_calculo="fijo", condicion="ancho > 200"),
    ])
    r = client.post("/api/recipes/1/produce", json={"w": 150, "h": 200}, headers=auth("taller"))
    assert r.status_code == 200, r.get_json()
    db.session.expire_all()
    assert float(db.session.get(Supply, soporte.id).stock_actual) == 20


# --- Versionado -----------------------------------------------------------------------------

def test_publicar_version_cierra_la_anterior_y_no_cambia_el_pasado(client, auth):
    tubo, soporte, _ = _insumos()
    crear_receta(1, [_item(soporte, tipo_calculo="fijo", cantidad_base=1)],
                 desde=datetime(2025, 1, 1))
    hoy = datetime.now(timezone.utc).date()

    nueva = client.post("/api/recipes/1/versions", headers=auth("admin"), json={
        "nota": "Ahora lleva 2 soportes",
        "items": [{"id_insumo": soporte.id, "nombre": "Soporte", "tipo_calculo": "fijo", "cantidad_base": 2}],
    })
    assert nueva.status_code == 201, nueva.get_json()
    assert nueva.get_json()["version"] == 2

    h = auth("admin")
    vigente = client.get("/api/test-recipe/1?w=150&h=200", headers=h).get_json()
    assert vigente["version"] == 2 and vigente["total_materiales"] == 2200
    # un presupuesto de una fecha anterior sigue dando el mismo resultado
    viejo = client.get("/api/test-recipe/1?w=150&h=200&fecha=2025-06-01", headers=h).get_json()
    assert viejo["version"] == 1 and viejo["total_materiales"] == 1200
    por_version = client.get("/api/test-recipe/1?w=150&h=200&version=1", headers=h).get_json()
    assert por_version["total_materiales"] == 1200

    versiones = client.get("/api/recipes/1/versions", headers=h).get_json()
    assert [v["version"] for v in versiones] == [2, 1]
    assert versiones[1]["vigente_hasta"] is not None and versiones[0]["vigente_hasta"] is None
    assert hoy  # la fecha de hoy resuelve a la versión 2
    assert client.get(f"/api/test-recipe/1?w=150&h=200&fecha={hoy}", headers=h).get_json()["version"] == 2


def test_fecha_anterior_a_toda_version_da_404(client, auth):
    _, soporte, _ = _insumos()
    crear_receta(1, [_item(soporte, tipo_calculo="fijo")], desde=datetime(2025, 1, 1))
    r = client.get("/api/test-recipe/1?w=150&h=200&fecha=2024-01-01", headers=auth("admin"))
    assert r.status_code == 404


def test_publicar_requiere_permiso_de_admin(client, auth):
    _, soporte, _ = _insumos()
    crear_receta(1, [_item(soporte, tipo_calculo="fijo")])
    cuerpo = {"items": [{"id_insumo": soporte.id, "nombre": "S", "tipo_calculo": "fijo"}]}
    assert client.post("/api/recipes/1/versions", json=cuerpo).status_code == 401
    assert client.post("/api/recipes/1/versions", json=cuerpo, headers=auth("taller")).status_code == 403
    assert client.post("/api/recipes/1/versions", json=cuerpo, headers=auth("ventas")).status_code == 403


def test_publicar_valida_los_items(client, auth):
    tubo, soporte, _ = _insumos()
    sin_largo = Supply(categoria_id=tubo.categoria_id, name="Perfil sin largo", unidad_medida="cm",
                       precio_costo_unitario=1, stock_actual=1)
    db.session.add(sin_largo)
    db.session.commit()
    crear_receta(1, [_item(soporte, tipo_calculo="fijo")])
    h = auth("admin")

    def publicar(item):
        return client.post("/api/recipes/1/versions", json={"items": [item]}, headers=h)

    casos = {
        "tipo inexistente": {"id_insumo": soporte.id, "nombre": "X", "tipo_calculo": "magico"},
        "insumo inexistente": {"id_insumo": 9999, "nombre": "X", "tipo_calculo": "fijo"},
        "falta el insumo": {"nombre": "X", "tipo_calculo": "fijo"},
        "perfil sin largo": {"id_insumo": sin_largo.id, "nombre": "X", "tipo_calculo": "perfil"},
        "formula peligrosa": {"id_insumo": soporte.id, "nombre": "X", "tipo_calculo": "fijo",
                              "formula_cantidad": "__import__('os')"},
        "condicion invalida": {"id_insumo": soporte.id, "nombre": "X", "tipo_calculo": "fijo", "condicion": "ancho >"},
        "formula con division por cero": {"id_insumo": soporte.id, "nombre": "X", "tipo_calculo": "fijo",
                                          "formula_cantidad": "ancho / 0"},
        "merma negativa": {"id_insumo": soporte.id, "nombre": "X", "tipo_calculo": "fijo", "merma_pct": -1},
    }
    for nombre, item in casos.items():
        r = publicar(item)
        assert r.status_code == 400, (nombre, r.get_json())
    assert Receta.query.filter_by(producto_id=1).count() == 1  # nada se guardó

    ok = publicar({"id_insumo": soporte.id, "nombre": "X", "tipo_calculo": "fijo",
                   "formula_cantidad": "ceil(ancho / 100)", "condicion": "sistema == 'motor'"})
    assert ok.status_code == 201
    assert publicar({"nombre": "Armado", "tipo_calculo": "mano_obra", "minutos_mano_obra": 20}).status_code == 201


def test_publicar_en_producto_inexistente_da_404(client, auth):
    _, soporte, _ = _insumos()
    r = client.post("/api/recipes/999/versions", headers=auth("admin"),
                    json={"items": [{"id_insumo": soporte.id, "nombre": "X", "tipo_calculo": "fijo"}]})
    assert r.status_code == 404


def test_catalogo_de_tipos_de_calculo(client, auth):
    tipos = client.get("/api/recipes/calculation-types", headers=auth("ventas")).get_json()
    assert {t["tipo"] for t in tipos} >= {"lineal_alto", "superficie", "lineal_ancho", "perfil", "fijo", "mano_obra"}


# --- Migración 0004 -------------------------------------------------------------------------

def test_migracion_copia_recetas_bom_como_version_1(tmp_path):
    uri = "sqlite:///" + str(tmp_path / "legacy.db")
    engine = sa.create_engine(uri)
    with engine.begin() as c:
        c.execute(sa.text("CREATE TABLE productos (id INTEGER PRIMARY KEY, nombre TEXT, descripcion TEXT, "
                          "categoria TEXT, activo BOOLEAN)"))
        c.execute(sa.text("CREATE TABLE usuarios (id INTEGER PRIMARY KEY)"))
        c.execute(sa.text("CREATE TABLE insumos (id INTEGER PRIMARY KEY, name TEXT)"))
        c.execute(sa.text(
            "CREATE TABLE recetas_bom (id INTEGER PRIMARY KEY, nombre_producto TEXT, id_insumo INTEGER, "
            "delta_ancho_cm NUMERIC, delta_alto_cm NUMERIC, tipo_calculo TEXT, descripcion TEXT, "
            "id_padre INTEGER, cantidad_base NUMERIC, merma_pct NUMERIC, minutos_mano_obra NUMERIC)"))
        c.execute(sa.text("INSERT INTO productos VALUES (5,'Roller Blackout',NULL,'Sistemas',1)"))
        c.execute(sa.text(
            "INSERT INTO recetas_bom VALUES "
            "(5,'Cortina Roller Blackout',NULL,0,0,'fijo',NULL,NULL,1,0,0),"
            "(17,'Tela',17,-2,30,'superficie',NULL,5,1,5,0),"
            "(18,'Tubo',7,-1.5,0,'perfil',NULL,5,1,0,10),"
            "(30,'Suelto',7,0,0,'fijo',NULL,9,2,0,0)"))
    app = create_app({"SQLALCHEMY_DATABASE_URI": uri, "SECRET_KEY": "x" * 40, "TESTING": True})
    cfg = Config(os.path.join(MIGRACIONES, "alembic.ini"))
    cfg.set_main_option("script_location", MIGRACIONES)
    with app.app_context():
        command.stamp(cfg, "0003_unidades_perfiles")
        command.upgrade(cfg, "0006_stock_precios_retazos")
        command.upgrade(cfg, "0006_stock_precios_retazos")  # idempotente

    with engine.connect() as c:
        recetas = [tuple(r) for r in c.execute(sa.text("SELECT producto_id, version FROM recetas ORDER BY producto_id"))]
        items = [tuple(r) for r in c.execute(sa.text(
            "SELECT r.producto_id, i.nombre, i.tipo_calculo, i.merma_pct, i.minutos_mano_obra "
            "FROM receta_items i JOIN recetas r ON r.id = i.receta_id ORDER BY i.orden"))]
        productos = [tuple(r) for r in c.execute(sa.text("SELECT id, nombre FROM productos ORDER BY id"))]
    assert recetas == [(5, 1), (9, 1)]
    assert items == [(5, "Tela", "superficie", 5, 0), (5, "Tubo", "perfil", 0, 10), (9, "Suelto", "fijo", 0, 0)]
    assert (9, "Producto 9") in productos
