"""Estado de sincronización de precios y presupuestos congelados.

Revision ID: 0012_sheets_presupuestos
Revises: 0011_compatibilidad_legacy
"""
from alembic import op
import sqlalchemy as sa

revision = '0012_sheets_presupuestos'
down_revision = '0011_compatibilidad_legacy'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sincronizacion_precios',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('ultimo_intento', sa.DateTime()),
        sa.Column('ultima_exitosa', sa.DateTime()),
        sa.Column('error', sa.Text()),
        sa.Column('actualizados', sa.Integer()),
        sa.Column('omitidos', sa.Integer()),
    )
    op.execute('INSERT INTO sincronizacion_precios (id) VALUES (1)')
    op.create_table(
        'presupuestos_guardados',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('producto_id', sa.Integer(), sa.ForeignKey('productos.id'), nullable=False),
        sa.Column('producto_nombre', sa.String(255), nullable=False),
        sa.Column('receta_id', sa.Integer(), sa.ForeignKey('recetas.id'), nullable=False),
        sa.Column('receta_version', sa.Integer(), nullable=False),
        sa.Column('ancho_cm', sa.Float(), nullable=False),
        sa.Column('alto_cm', sa.Float(), nullable=False),
        sa.Column('referencia', sa.String(255)),
        sa.Column('opciones', sa.JSON(), nullable=False),
        sa.Column('resultado', sa.JSON(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), sa.ForeignKey('usuarios.id')),
        sa.Column('usuario_nombre', sa.String(100)),
        sa.Column('creado_en', sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp()),
    )
    op.create_index('ix_presupuestos_guardados_fecha', 'presupuestos_guardados', ['creado_en'])


def downgrade():
    op.drop_index('ix_presupuestos_guardados_fecha', table_name='presupuestos_guardados')
    op.drop_table('presupuestos_guardados')
    op.drop_table('sincronizacion_precios')
