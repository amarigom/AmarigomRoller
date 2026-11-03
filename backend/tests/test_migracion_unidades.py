import importlib.util
import os
import sys

import sqlalchemy as sa
from alembic import command
from alembic.config import Config

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from factory import create_app

MIGRACIONES = os.path.join(os.path.dirname(os.path.dirname(__file__)), "migrations")


def _modulo_0003():
    ruta = os.path.join(MIGRACIONES, "versions", "0003_unidades_perfiles.py")
    spec = importlib.util.spec_from_file_location("m0003", ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_largo_de_pieza_segun_el_nombre():
    f = _modulo_0003().largo_pieza_cm
    assert f("Tubo aluminio 32 mm x 4 mts") == 400
    assert f("Tubo aluminio 58 mm x 6 mts") == 600
    assert f("Tubo aluminio 32 mm x 2 mts") == 200
    assert f("Tubo Aluminio 25 mm x 1 mt") == 100
    assert f("Cinta doble faz 19mm (50 mts)") == 5000
    assert f("Espagueti traba tela/perfil (Rollo 200m)") == 20000
    assert f("Sistema 25 mm - MINI") is None


def test_migracion_sobre_esquema_viejo_corrige_datos(tmp_path):
    uri = "sqlite:///" + str(tmp_path / "legacy.db")
    engine = sa.create_engine(uri)
    with engine.begin() as c:
        c.execute(sa.text("CREATE TABLE insumos (id INTEGER PRIMARY KEY, name TEXT, unidad_medida TEXT, "
                          "precio_costo_unitario NUMERIC, stock_actual NUMERIC)"))
        c.execute(sa.text("CREATE TABLE recetas_bom (id INTEGER PRIMARY KEY, id_padre INTEGER, id_insumo INTEGER, "
                          "tipo_calculo TEXT, cantidad_base NUMERIC)"))
        c.execute(sa.text("INSERT INTO insumos VALUES (7,'Tubo aluminio 32 mm x 4 mts','cm',54.94,1200),"
                          "(23,'Espagueti traba tela/perfil (Rollo 200m)','cm',70,200),"
                          "(24,'Cinta doble faz 19mm (50 mts)','cm',3.6179,200),"
                          "(17,'Black Out TAPAR Blanco - ancho 2.20','cm',122.5,1000)"))
        c.execute(sa.text("INSERT INTO recetas_bom VALUES (1,5,17,'superficie',1.05),(2,5,7,'lineal_ancho',1),"
                          "(3,5,24,'lineal_ancho',0.2),(4,5,23,'lineal_ancho',0.005)"))

    app = create_app({"SQLALCHEMY_DATABASE_URI": uri, "SECRET_KEY": "x" * 40, "TESTING": True})
    cfg = Config(os.path.join(MIGRACIONES, "alembic.ini"))
    cfg.set_main_option("script_location", MIGRACIONES)
    with app.app_context():
        command.stamp(cfg, "0002_usuarios")
        command.upgrade(cfg, "head")

    with engine.connect() as c:
        insumos = {r[0]: r for r in c.execute(sa.text("SELECT id, unidad_medida, largo_pieza_cm FROM insumos"))}
        recetas = {r[0]: r for r in c.execute(sa.text(
            "SELECT id, tipo_calculo, cantidad_base, merma_pct FROM recetas_bom"))}
    assert insumos[7][1:] == ("cm", 400)
    assert insumos[23][1:] == ("metro", 20000)
    assert insumos[24][1:] == ("rollo", 5000)
    assert insumos[17][2] is None
    assert recetas[1][1:] == ("superficie", 1, 5)
    assert recetas[2][1] == "perfil"
    assert recetas[3][1] == "lineal_ancho" and recetas[4][1] == "lineal_ancho"
    assert "stock_piezas_detalle" in sa.inspect(engine).get_table_names()
