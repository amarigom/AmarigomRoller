"""indices de rendimiento sobre el esquema existente

Revision ID: 0001_indices
Revises:
Create Date: 2026-11-02
"""
from alembic import op

revision = '0001_indices'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # El esquema base ya existe en Neon: esta migracion solo agrega indices.
    op.execute("CREATE INDEX IF NOT EXISTS ix_recetas_bom_id_padre ON recetas_bom (id_padre)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_retazos_telas_insumo_estado ON retazos_telas (id_insumo_base, estado)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_insumos_categoria_id ON insumos (categoria_id)")


def downgrade():
    op.execute("DROP INDEX IF EXISTS ix_insumos_categoria_id")
    op.execute("DROP INDEX IF EXISTS ix_retazos_telas_insumo_estado")
    op.execute("DROP INDEX IF EXISTS ix_recetas_bom_id_padre")
