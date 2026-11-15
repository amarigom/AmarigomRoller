"""Conserva la unidad original de los movimientos y precios históricos.

Revision ID: 0010_unidades_historial
Revises: 0009_precios_tela
"""
from alembic import op
import sqlalchemy as sa

revision = '0010_unidades_historial'
down_revision = '0009_precios_tela'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('inventario_movimientos', sa.Column('unidad', sa.String(20)))
    op.add_column('historial_precios_insumos', sa.Column('unidad', sa.String(20)))


def downgrade():
    op.drop_column('historial_precios_insumos', 'unidad')
    op.drop_column('inventario_movimientos', 'unidad')
