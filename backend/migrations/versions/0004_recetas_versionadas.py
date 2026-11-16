"""recetas versionadas: tablas recetas y receta_items

Separa el producto (tabla productos) de su receta. Cada receta tiene versiones con vigencia
(vigente_desde / vigente_hasta) y sus ítems admiten fórmulas y condiciones.
Copia lo que hay en recetas_bom como versión 1 de cada producto (id_padre = producto_id).
recetas_bom no se borra: queda como respaldo de solo lectura.

Revision ID: 0004_recetas_versionadas
Revises: 0003_unidades_perfiles
Create Date: 2026-11-03
"""
from alembic import op
import sqlalchemy as sa

revision = '0004_recetas_versionadas'
down_revision = '0003_unidades_perfiles'
branch_labels = None
depends_on = None

VIGENTE_DESDE = '2000-01-01 00:00:00'


def upgrade():
    bind = op.get_bind()
    tablas = set(sa.inspect(bind).get_table_names())

    if 'recetas' not in tablas:
        op.create_table(
            'recetas',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('producto_id', sa.Integer(), sa.ForeignKey('productos.id'), nullable=False),
            sa.Column('version', sa.Integer(), nullable=False),
            sa.Column('vigente_desde', sa.DateTime(), nullable=False),
            sa.Column('vigente_hasta', sa.DateTime()),
            sa.Column('nota', sa.String(255)),
            sa.Column('creado_en', sa.DateTime(), server_default=sa.func.current_timestamp()),
            sa.UniqueConstraint('producto_id', 'version', name='uq_recetas_producto_version'),
        )
        op.create_index('ix_recetas_producto_vigencia', 'recetas', ['producto_id', 'vigente_desde'])
    if 'receta_items' not in tablas:
        op.create_table(
            'receta_items',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('receta_id', sa.Integer(), sa.ForeignKey('recetas.id'), nullable=False),
            sa.Column('orden', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('id_insumo', sa.Integer(), sa.ForeignKey('insumos.id')),
            sa.Column('nombre', sa.String(100), nullable=False),
            sa.Column('tipo_calculo', sa.String(30), nullable=False),
            sa.Column('descripcion', sa.Text()),
            sa.Column('delta_ancho_cm', sa.Numeric(12, 2), server_default='0'),
            sa.Column('delta_alto_cm', sa.Numeric(12, 2), server_default='0'),
            sa.Column('cantidad_base', sa.Numeric(12, 4), server_default='1'),
            sa.Column('merma_pct', sa.Numeric(5, 2), server_default='0'),
            sa.Column('minutos_mano_obra', sa.Numeric(8, 2), server_default='0'),
            sa.Column('formula_ancho', sa.String(200)),
            sa.Column('formula_alto', sa.String(200)),
            sa.Column('formula_cantidad', sa.String(200)),
            sa.Column('condicion', sa.String(200)),
        )
        op.create_index('ix_receta_items_receta', 'receta_items', ['receta_id'])

    if 'recetas_bom' in tablas:
        _copiar_recetas_existentes(bind)


def _copiar_recetas_existentes(bind):
    ya_migrados = {r[0] for r in bind.execute(sa.text("SELECT producto_id FROM recetas"))}
    padres = [r[0] for r in bind.execute(sa.text(
        "SELECT DISTINCT id_padre FROM recetas_bom WHERE id_padre IS NOT NULL ORDER BY id_padre"))]
    for producto_id in padres:
        if producto_id in ya_migrados:
            continue
        existe = bind.execute(sa.text("SELECT 1 FROM productos WHERE id = :i"), {'i': producto_id}).first()
        if not existe:
            nombre = bind.execute(
                sa.text("SELECT nombre_producto FROM recetas_bom WHERE id = :i"), {'i': producto_id}).scalar()
            bind.execute(
                sa.text("INSERT INTO productos (id, nombre, activo) VALUES (:i, :n, :a)"),
                {'i': producto_id, 'n': nombre or f"Producto {producto_id}", 'a': True})
        bind.execute(
            sa.text("INSERT INTO recetas (producto_id, version, vigente_desde, nota) "
                    "VALUES (:p, 1, :d, 'Migrada desde recetas_bom')"),
            {'p': producto_id, 'd': VIGENTE_DESDE})
        receta_id = bind.execute(
            sa.text("SELECT id FROM recetas WHERE producto_id = :p AND version = 1"), {'p': producto_id}).scalar()
        bind.execute(sa.text(
            "INSERT INTO receta_items (receta_id, orden, id_insumo, nombre, tipo_calculo, descripcion, "
            "delta_ancho_cm, delta_alto_cm, cantidad_base, merma_pct, minutos_mano_obra) "
            "SELECT :r, id, id_insumo, COALESCE(nombre_producto, 'Componente'), tipo_calculo, descripcion, "
            "COALESCE(delta_ancho_cm, 0), COALESCE(delta_alto_cm, 0), COALESCE(cantidad_base, 1), "
            "COALESCE(merma_pct, 0), COALESCE(minutos_mano_obra, 0) "
            "FROM recetas_bom WHERE id_padre = :p ORDER BY id"),
            {'r': receta_id, 'p': producto_id})


def downgrade():
    op.drop_index('ix_receta_items_receta', table_name='receta_items')
    op.drop_table('receta_items')
    op.drop_index('ix_recetas_producto_vigencia', table_name='recetas')
    op.drop_table('recetas')
