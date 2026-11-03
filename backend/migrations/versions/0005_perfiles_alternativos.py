"""perfiles alternativos por componente de receta

Revision ID: 0005_perfiles_alternativos
Revises: 0004_recetas_versionadas
"""
import sqlalchemy as sa
from alembic import op

revision = '0005_perfiles_alternativos'
down_revision = '0004_recetas_versionadas'
branch_labels = None
depends_on = None


def upgrade():
    cols = {c['name'] for c in sa.inspect(op.get_bind()).get_columns('receta_items')}
    if 'insumos_alternativos' not in cols:
        op.add_column('receta_items', sa.Column('insumos_alternativos', sa.JSON()))


def downgrade():
    op.drop_column('receta_items', 'insumos_alternativos')
