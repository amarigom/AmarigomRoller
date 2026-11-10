"""movimientos de stock, historial de precios, stock minimo y referencia de retazos

Revision ID: 0006_stock_precios_retazos
Revises: 0005_perfiles_alternativos
"""
from alembic import op
import sqlalchemy as sa

revision = '0006_stock_precios_retazos'
down_revision = '0005_perfiles_alternativos'
branch_labels = None
depends_on = None


def _columnas(tabla):
    return {c['name'] for c in sa.inspect(op.get_bind()).get_columns(tabla)}


def upgrade():
    bind = op.get_bind()
    if 'stock_minimo' not in _columnas('insumos'):
        op.add_column('insumos', sa.Column(
            'stock_minimo', sa.Numeric(12, 4), nullable=False, server_default='0'))
    if 'activo' not in _columnas('insumos'):
        op.add_column('insumos', sa.Column(
            'activo', sa.Boolean(), nullable=False, server_default=sa.true()))
    if 'retazos_telas' not in sa.inspect(bind).get_table_names():
        op.create_table(
            'retazos_telas',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('id_insumo_base', sa.Integer(), sa.ForeignKey('insumos.id'), nullable=False),
            sa.Column('ancho_cm', sa.Numeric(10, 2), nullable=False),
            sa.Column('largo_cm', sa.Numeric(10, 2), nullable=False),
            sa.Column('fecha_generado', sa.DateTime(), server_default=sa.func.current_timestamp()),
            sa.Column('estado', sa.String(20), server_default='disponible'),
            sa.Column('notas', sa.Text()),
        )
        op.create_index('ix_retazos_telas_insumo_estado', 'retazos_telas', ['id_insumo_base', 'estado'])
    if 'referencia' not in _columnas('retazos_telas'):
        op.add_column('retazos_telas', sa.Column('referencia', sa.String(255)))

    tablas = set(sa.inspect(bind).get_table_names())
    if 'inventario_movimientos' not in tablas:
        op.create_table(
            'inventario_movimientos',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('id_insumo', sa.Integer(), sa.ForeignKey('insumos.id'), nullable=False),
            sa.Column('tipo', sa.String(20), nullable=False),
            sa.Column('cantidad', sa.Numeric(14, 4), nullable=False),
            sa.Column('stock_resultante', sa.Numeric(14, 4), nullable=False),
            sa.Column('referencia', sa.String(255)),
            sa.Column('notas', sa.Text()),
            sa.Column('usuario_id', sa.Integer(), sa.ForeignKey('usuarios.id')),
            sa.Column('creado_en', sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp()),
        )
    op.execute(
        'CREATE INDEX IF NOT EXISTS ix_inventario_movimientos_insumo_fecha '
        'ON inventario_movimientos (id_insumo, creado_en)')

    if 'historial_precios_insumos' not in tablas:
        op.create_table(
            'historial_precios_insumos',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('id_insumo', sa.Integer(), sa.ForeignKey('insumos.id'), nullable=False),
            sa.Column('precio', sa.Numeric(12, 4), nullable=False),
            sa.Column('vigente_desde', sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp()),
            sa.Column('motivo', sa.String(255)),
            sa.Column('usuario_id', sa.Integer(), sa.ForeignKey('usuarios.id')),
        )
    op.execute(
        'CREATE INDEX IF NOT EXISTS ix_historial_precios_insumo_fecha '
        'ON historial_precios_insumos (id_insumo, vigente_desde)')

    # Conserva el saldo existente como movimiento inicial, sin modificarlo.
    columnas = _columnas('insumos')
    if 'stock_actual' in columnas:
        bind.execute(sa.text(
            "INSERT INTO inventario_movimientos "
            "(id_insumo, tipo, cantidad, stock_resultante, referencia, notas) "
            "SELECT i.id, 'apertura', i.stock_actual, i.stock_actual, 'Migración 0006', "
            "'Saldo inicial migrado desde insumos.stock_actual' "
            "FROM insumos i WHERE COALESCE(i.stock_actual, 0) <> 0 "
            "AND NOT EXISTS (SELECT 1 FROM inventario_movimientos m "
            "WHERE m.id_insumo = i.id AND m.tipo = 'apertura' AND m.referencia = 'Migración 0006')"))
    if 'precio_costo_unitario' in columnas:
        bind.execute(sa.text(
            "INSERT INTO historial_precios_insumos (id_insumo, precio, motivo) "
            "SELECT i.id, COALESCE(i.precio_costo_unitario, 0), 'Precio inicial migrado' "
            "FROM insumos i WHERE NOT EXISTS "
            "(SELECT 1 FROM historial_precios_insumos h WHERE h.id_insumo = i.id)"))


def downgrade():
    op.drop_index('ix_historial_precios_insumo_fecha', table_name='historial_precios_insumos')
    op.drop_table('historial_precios_insumos')
    op.drop_index('ix_inventario_movimientos_insumo_fecha', table_name='inventario_movimientos')
    op.drop_table('inventario_movimientos')
    op.drop_column('retazos_telas', 'referencia')
    op.drop_column('insumos', 'activo')
    op.drop_column('insumos', 'stock_minimo')
