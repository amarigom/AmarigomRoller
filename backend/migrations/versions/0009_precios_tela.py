"""Clasificación de telas y precio separado por metro cuadrado.

Revision ID: 0009_precios_tela
Revises: 0008_etiqueta_desgaste
"""
from alembic import op
import sqlalchemy as sa

revision = '0009_precios_tela'
down_revision = '0008_etiqueta_desgaste'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('insumos', sa.Column('es_tela', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('insumos', sa.Column('precio_m2', sa.Numeric(12, 4)))
    op.add_column('insumos', sa.Column('unidad_compra', sa.String(20)))
    op.add_column('insumos', sa.Column('factor_conversion', sa.Numeric(12, 4)))
    op.add_column('historial_precios_insumos', sa.Column('precio_m2', sa.Numeric(12, 4)))


def downgrade():
    op.drop_column('historial_precios_insumos', 'precio_m2')
    op.drop_column('insumos', 'factor_conversion')
    op.drop_column('insumos', 'unidad_compra')
    op.drop_column('insumos', 'precio_m2')
    op.drop_column('insumos', 'es_tela')
