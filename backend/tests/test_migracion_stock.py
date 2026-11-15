import os

import sqlalchemy as sa
from alembic import command
from alembic.config import Config

from factory import create_app

MIGRACIONES = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'migrations')


def test_migracion_stock_conserva_saldos_y_registra_precios_iniciales(tmp_path):
    uri = 'sqlite:///' + str(tmp_path / 'stock_legacy.db')
    engine = sa.create_engine(uri)
    with engine.begin() as conn:
        conn.execute(sa.text(
            'CREATE TABLE insumos (id INTEGER PRIMARY KEY, name TEXT, '
            'stock_actual NUMERIC, precio_costo_unitario NUMERIC)'))
        conn.execute(sa.text("CREATE TABLE usuarios (id INTEGER PRIMARY KEY)"))
        conn.execute(sa.text(
            "INSERT INTO insumos VALUES (1, 'Tela', 12.5, 800), (2, 'Soporte', 0, 25)"))

    app = create_app({
        'SQLALCHEMY_DATABASE_URI': uri, 'SECRET_KEY': 'x' * 40, 'TESTING': True,
    })
    cfg = Config(os.path.join(MIGRACIONES, 'alembic.ini'))
    cfg.set_main_option('script_location', MIGRACIONES)
    with app.app_context():
        command.stamp(cfg, '0005_perfiles_alternativos')
        command.upgrade(cfg, '0006_stock_precios_retazos')
        command.upgrade(cfg, '0006_stock_precios_retazos')

    with engine.connect() as conn:
        saldo = conn.execute(sa.text(
            'SELECT stock_actual, stock_minimo FROM insumos WHERE id=1')).one()
        movimientos = conn.execute(sa.text(
            "SELECT tipo, cantidad, stock_resultante FROM inventario_movimientos "
            "WHERE id_insumo=1")).all()
        precios = conn.execute(sa.text(
            "SELECT precio FROM historial_precios_insumos WHERE id_insumo=2")).all()
        tablas = set(sa.inspect(conn).get_table_names())
    assert tuple(map(float, saldo)) == (12.5, 0)
    assert [(m[0], float(m[1]), float(m[2])) for m in movimientos] == [('apertura', 12.5, 12.5)]
    assert [float(p[0]) for p in precios] == [25]
    assert 'retazos_telas' in tablas


def test_migracion_crea_historial_y_enlace_de_movimientos(tmp_path):
    uri = 'sqlite:///' + str(tmp_path / 'production_legacy.db')
    engine = sa.create_engine(uri)
    with engine.begin() as conn:
        conn.execute(sa.text('CREATE TABLE productos (id INTEGER PRIMARY KEY)'))
        conn.execute(sa.text('CREATE TABLE recetas (id INTEGER PRIMARY KEY)'))
        conn.execute(sa.text('CREATE TABLE usuarios (id INTEGER PRIMARY KEY)'))
        conn.execute(sa.text(
            'CREATE TABLE inventario_movimientos (id INTEGER PRIMARY KEY, id_insumo INTEGER)'))

    app = create_app({
        'SQLALCHEMY_DATABASE_URI': uri, 'SECRET_KEY': 'x' * 40, 'TESTING': True,
    })
    cfg = Config(os.path.join(MIGRACIONES, 'alembic.ini'))
    cfg.set_main_option('script_location', MIGRACIONES)
    with app.app_context():
        command.stamp(cfg, '0006_stock_precios_retazos')
        command.upgrade(cfg, '0007_historial_producciones')

    with engine.connect() as conn:
        tablas = set(sa.inspect(conn).get_table_names())
        columnas = {c['name'] for c in sa.inspect(conn).get_columns('inventario_movimientos')}
        claves_foraneas = sa.inspect(conn).get_foreign_keys('inventario_movimientos')
    assert 'producciones' in tablas
    assert 'produccion_id' in columnas
    assert any(
        fk['name'] == 'fk_inventario_movimientos_produccion_id'
        and fk['referred_table'] == 'producciones'
        for fk in claves_foraneas
    )

    with app.app_context():
        command.downgrade(cfg, '0006_stock_precios_retazos')

    with engine.connect() as conn:
        tablas = set(sa.inspect(conn).get_table_names())
        columnas = {c['name'] for c in sa.inspect(conn).get_columns('inventario_movimientos')}
    assert 'producciones' not in tablas
    assert 'produccion_id' not in columnas
