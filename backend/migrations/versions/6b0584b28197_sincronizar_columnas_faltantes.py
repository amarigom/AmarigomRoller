"""Compatibiliza nombres y columnas de inventario preexistentes.

Revision ID: 6b0584b28197
Revises: 0010_unidades_historial
"""
from alembic import op
import sqlalchemy as sa

revision = '6b0584b28197'
down_revision = '0010_unidades_historial'
branch_labels = None
depends_on = None


def _columnas(bind, tabla):
    return {col['name'] for col in sa.inspect(bind).get_columns(tabla)}


def _renombrar(bind, tabla, anterior, nuevo):
    columnas = _columnas(bind, tabla)
    if anterior in columnas and nuevo in columnas:
        raise RuntimeError(f'{tabla}: existen {anterior} y {nuevo}; conciliá los datos antes de migrar')
    if anterior in columnas:
        with op.batch_alter_table(tabla) as batch:
            batch.alter_column(anterior, new_column_name=nuevo)
    elif nuevo not in columnas:
        raise RuntimeError(f'{tabla}: faltan {anterior} y {nuevo}')


def upgrade():
    bind = op.get_bind()
    _renombrar(bind, 'categorias_insumos', 'nombre', 'name')
    _renombrar(bind, 'insumos', 'nombre', 'name')
    _renombrar(bind, 'insumos', 'stock_actual_total', 'stock_actual')

    columnas = _columnas(bind, 'insumos')
    definiciones = [
        sa.Column('stock_minimo', sa.Numeric(12, 4), server_default='0', nullable=False),
        sa.Column('activo', sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column('ancho_cm', sa.Numeric(10, 2)),
        sa.Column('largo_pieza_cm', sa.Numeric(10, 2)),
        sa.Column('es_tela', sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column('precio_m2', sa.Numeric(12, 4)),
        sa.Column('unidad_compra', sa.String(20)),
        sa.Column('factor_conversion', sa.Numeric(12, 4)),
    ]
    for columna in definiciones:
        if columna.name not in columnas:
            op.add_column('insumos', columna)
    indices = {index['name'] for index in sa.inspect(bind).get_indexes('insumos')}
    if 'ix_insumos_categoria_id' not in indices:
        op.create_index('ix_insumos_categoria_id', 'insumos', ['categoria_id'])

    if 'stock_piezas_detalle' in sa.inspect(bind).get_table_names():
        indices = {index['name'] for index in sa.inspect(bind).get_indexes('stock_piezas_detalle')}
        if 'ix_stock_piezas_insumo_retazo' not in indices:
            op.create_index('ix_stock_piezas_insumo_retazo', 'stock_piezas_detalle', ['id_insumo', 'es_retazo'])


def downgrade():
    # La revisión adapta esquemas heterogéneos: no es seguro deshacer nombres o borrar columnas existentes.
    pass
