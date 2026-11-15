"""historial de producciones y enlace con movimientos de stock

Revision ID: 0007_historial_producciones
Revises: 0006_stock_precios_retazos
"""
from alembic import op
import sqlalchemy as sa

revision = '0007_historial_producciones'
down_revision = '0006_stock_precios_retazos'
branch_labels = None
depends_on = None


def upgrade():
    tablas = set(sa.inspect(op.get_bind()).get_table_names())
    if 'producciones' not in tablas:
        op.create_table(
            'producciones',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('producto_id', sa.Integer(), sa.ForeignKey('productos.id'), nullable=False),
            sa.Column('producto_nombre', sa.String(255), nullable=False),
            sa.Column('receta_id', sa.Integer(), sa.ForeignKey('recetas.id'), nullable=False),
            sa.Column('receta_version', sa.Integer(), nullable=False),
            sa.Column('ancho_cm', sa.Numeric(10, 2), nullable=False),
            sa.Column('alto_cm', sa.Numeric(10, 2), nullable=False),
            sa.Column('opciones', sa.JSON(), nullable=False),
            sa.Column('referencia', sa.String(255)),
            sa.Column('total_materiales', sa.Numeric(14, 2), nullable=False),
            sa.Column('total_minutos', sa.Numeric(10, 2), nullable=False),
            sa.Column('total_mano_obra', sa.Numeric(14, 2), nullable=False),
            sa.Column('total', sa.Numeric(14, 2), nullable=False),
            sa.Column('detalle', sa.JSON(), nullable=False),
            sa.Column('usuario_id', sa.Integer(), sa.ForeignKey('usuarios.id')),
            sa.Column('usuario_nombre', sa.String(100)),
            sa.Column('creado_en', sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp()),
        )
    op.execute('CREATE INDEX IF NOT EXISTS ix_producciones_fecha ON producciones (creado_en)')
    op.execute(
        'CREATE INDEX IF NOT EXISTS ix_producciones_producto_fecha '
        'ON producciones (producto_id, creado_en)')

    columnas = {c['name'] for c in sa.inspect(op.get_bind()).get_columns('inventario_movimientos')}
    if 'produccion_id' not in columnas:
        with op.batch_alter_table('inventario_movimientos') as batch_op:
            batch_op.add_column(sa.Column('produccion_id', sa.Integer()))
            batch_op.create_foreign_key(
                'fk_inventario_movimientos_produccion_id',
                'producciones',
                ['produccion_id'],
                ['id'],
            )


def downgrade():
    with op.batch_alter_table('inventario_movimientos') as batch_op:
        batch_op.drop_constraint(
            'fk_inventario_movimientos_produccion_id',
            type_='foreignkey',
        )
        batch_op.drop_column('produccion_id')
    op.drop_index('ix_producciones_producto_fecha', table_name='producciones')
    op.drop_index('ix_producciones_fecha', table_name='producciones')
    op.drop_table('producciones')
