import os

import pytest
import sqlalchemy as sa
from alembic import command
from alembic.config import Config

from factory import create_app


def _base(tmp_path, existente=False):
    uri = 'sqlite:///' + str(tmp_path / 'etiqueta.db')
    engine = sa.create_engine(uri)
    with engine.begin() as conn:
        conn.execute(sa.text('CREATE TABLE categorias_insumos (id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL)'))
        conn.execute(sa.text(
            'CREATE TABLE insumos (id INTEGER PRIMARY KEY, categoria_id INTEGER, codigo_sku TEXT UNIQUE, '
            'name TEXT NOT NULL, unidad_medida TEXT, precio_costo_unitario NUMERIC, stock_actual NUMERIC, '
            'stock_minimo NUMERIC NOT NULL DEFAULT 0, activo BOOLEAN NOT NULL DEFAULT 1)'))
        conn.execute(sa.text('CREATE TABLE producciones (id INTEGER PRIMARY KEY, total NUMERIC)'))
        conn.execute(sa.text(
            'CREATE TABLE historial_precios_insumos (id INTEGER PRIMARY KEY, id_insumo INTEGER, precio NUMERIC, motivo TEXT)'))
        conn.execute(sa.text(
            'CREATE TABLE inventario_movimientos (id INTEGER PRIMARY KEY, id_insumo INTEGER, tipo TEXT, '
            'cantidad NUMERIC, stock_resultante NUMERIC, referencia TEXT)'))
        conn.execute(sa.text('INSERT INTO producciones VALUES (1, 123)'))
        if existente:
            conn.execute(sa.text("INSERT INTO insumos (name, codigo_sku) VALUES ('Etiqueta', 'EXISTENTE')"))
    app = create_app({'SQLALCHEMY_DATABASE_URI': uri, 'SECRET_KEY': 'x' * 40, 'TESTING': True})
    migraciones = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'migrations')
    cfg = Config(os.path.join(migraciones, 'alembic.ini'))
    cfg.set_main_option('script_location', migraciones)
    return app, cfg, engine


def test_migracion_crea_etiqueta_y_preserva_historial(tmp_path):
    app, cfg, engine = _base(tmp_path)
    with app.app_context():
        command.stamp(cfg, '0007_historial_producciones')
        command.upgrade(cfg, 'head')
    with engine.connect() as conn:
        assert tuple(conn.execute(sa.text(
            "SELECT name, unidad_medida, precio_costo_unitario, stock_actual FROM insumos "
            "WHERE codigo_sku='ROLLER-ETIQUETA'")).one()) == ('Etiqueta', 'unidad', 200, 0)
        assert tuple(conn.execute(sa.text("SELECT total, total_desgaste FROM producciones")).one()) == (123, 0)
        assert conn.execute(sa.text("SELECT count(*) FROM historial_precios_insumos")).scalar() == 1
        assert conn.execute(sa.text("SELECT count(*) FROM inventario_movimientos")).scalar() == 1
        columnas = {c['name'] for c in sa.inspect(conn).get_columns('insumos')}
        assert {'es_tela', 'precio_m2'} <= columnas
    with app.app_context():
        command.downgrade(cfg, '0007_historial_producciones')
        command.upgrade(cfg, 'head')
    with engine.connect() as conn:
        assert conn.execute(sa.text("SELECT count(*) FROM insumos")).scalar() == 1
        assert conn.execute(sa.text("SELECT count(*) FROM historial_precios_insumos")).scalar() == 1


def test_migracion_rechaza_etiqueta_ya_existente_sin_modificarla(tmp_path):
    app, cfg, engine = _base(tmp_path, existente=True)
    with app.app_context():
        command.stamp(cfg, '0007_historial_producciones')
        with pytest.raises(RuntimeError, match='Ya existe un insumo Etiqueta'):
            command.upgrade(cfg, 'head')
    with engine.connect() as conn:
        assert conn.execute(sa.text("SELECT codigo_sku FROM insumos")).scalar() == 'EXISTENTE'
