import os

import pytest
import sqlalchemy as sa
from alembic import command
from alembic.config import Config

from factory import create_app


def _base(tmp_path, categorias, insumos):
    uri = 'sqlite:///' + str(tmp_path / 'compatibilidad.db')
    engine = sa.create_engine(uri)
    with engine.begin() as conn:
        conn.execute(sa.text(f'CREATE TABLE categorias_insumos (id INTEGER PRIMARY KEY, {categorias})'))
        conn.execute(sa.text(f'CREATE TABLE insumos (id INTEGER PRIMARY KEY, categoria_id INTEGER, {insumos})'))
    app = create_app({'SQLALCHEMY_DATABASE_URI': uri, 'SECRET_KEY': 'x' * 40, 'TESTING': True})
    migraciones = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'migrations')
    cfg = Config(os.path.join(migraciones, 'alembic.ini'))
    cfg.set_main_option('script_location', migraciones)
    return app, cfg, engine


def test_compatibilidad_preserva_y_renombra_esquema_anterior(tmp_path):
    app, cfg, engine = _base(
        tmp_path, 'nombre TEXT', 'nombre TEXT, stock_actual_total NUMERIC')
    with engine.begin() as conn:
        conn.execute(sa.text("INSERT INTO categorias_insumos VALUES (1, 'Perfiles')"))
        conn.execute(sa.text("INSERT INTO insumos VALUES (1, 1, 'Tubo', 500)"))
    with app.app_context():
        command.stamp(cfg, '0010_unidades_historial')
        command.upgrade(cfg, 'head')
    with engine.connect() as conn:
        assert conn.execute(sa.text('SELECT name FROM categorias_insumos')).scalar() == 'Perfiles'
        assert tuple(conn.execute(sa.text(
            'SELECT name, stock_actual, activo, es_tela FROM insumos')).one()) == ('Tubo', 500, 1, 0)
        assert {'precio_m2', 'factor_conversion'} <= {
            c['name'] for c in sa.inspect(conn).get_columns('insumos')}


def test_compatibilidad_rechaza_nombres_duplicados(tmp_path):
    app, cfg, engine = _base(
        tmp_path, 'nombre TEXT, name TEXT', 'name TEXT, stock_actual NUMERIC')
    with app.app_context():
        command.stamp(cfg, '0010_unidades_historial')
        with pytest.raises(RuntimeError, match='existen nombre y name'):
            command.upgrade(cfg, 'head')
    with engine.connect() as conn:
        assert {'nombre', 'name'} <= {c['name'] for c in sa.inspect(conn).get_columns('categorias_insumos')}


def test_legacy_repara_columnas_sin_alterar_filas_existentes(tmp_path):
    app, cfg, engine = _base(
        tmp_path, 'name TEXT', 'name TEXT, stock_actual NUMERIC')
    with engine.begin() as conn:
        conn.execute(sa.text('CREATE TABLE recetas_bom (id INTEGER PRIMARY KEY, nombre_producto TEXT NOT NULL)'))
        conn.execute(sa.text("INSERT INTO recetas_bom VALUES (4, 'Ejemplo')"))
    with app.app_context():
        command.stamp(cfg, '6b0584b28197')
        command.upgrade(cfg, 'head')
    with engine.connect() as conn:
        assert tuple(conn.execute(sa.text(
            'SELECT id, nombre_producto, id_padre, cantidad_base FROM recetas_bom')).one()) == (4, 'Ejemplo', None, 1)
        assert {'merma_pct', 'minutos_mano_obra'} <= {
            c['name'] for c in sa.inspect(conn).get_columns('recetas_bom')}
        assert 'ultima_actualizacion' in {c['name'] for c in sa.inspect(conn).get_columns('insumos')}
