"""Repara columnas y restricciones antiguas ausentes en algunas ramas.

Revision ID: 0011_compatibilidad_legacy
Revises: 6b0584b28197
"""
from alembic import op
import sqlalchemy as sa

revision = '0011_compatibilidad_legacy'
down_revision = '6b0584b28197'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())
    if 'insumos' in tables:
        columns = {c['name'] for c in inspector.get_columns('insumos')}
        if 'ultima_actualizacion' not in columns:
            op.add_column('insumos', sa.Column('ultima_actualizacion', sa.DateTime()))
    if 'recetas_bom' in tables:
        columns = {c['name'] for c in inspector.get_columns('recetas_bom')}
        for column in (
            sa.Column('id_padre', sa.Integer()),
            sa.Column('cantidad_base', sa.Numeric(12, 4), server_default='1'),
            sa.Column('merma_pct', sa.Numeric(5, 2), server_default='0'),
            sa.Column('minutos_mano_obra', sa.Numeric(8, 2), server_default='0'),
        ):
            if column.name not in columns:
                op.add_column('recetas_bom', column)
        foreign_keys = sa.inspect(bind).get_foreign_keys('recetas_bom')
        if not any(fk['constrained_columns'] == ['id_padre'] and fk['referred_table'] == 'recetas_bom'
                   for fk in foreign_keys):
            with op.batch_alter_table('recetas_bom') as batch:
                batch.create_foreign_key('fk_recetas_bom_id_padre', 'recetas_bom', ['id_padre'], ['id'])
    if bind.dialect.name == 'postgresql':
        for table, constraint, column, values in (
            ('insumos', 'insumos_unidad_medida_check', 'unidad_medida',
             ('unidad', 'cm', 'metro', 'm2', 'rollo')),
            ('recetas_bom', 'recetas_bom_tipo_calculo_check', 'tipo_calculo',
             ('lineal_ancho', 'lineal_alto', 'fijo', 'superficie', 'perfil', 'mano_obra')),
        ):
            if table not in tables:
                continue
            checks = {c['name'] for c in sa.inspect(bind).get_check_constraints(table)}
            if constraint in checks:
                op.drop_constraint(constraint, table, type_='check')
            op.create_check_constraint(constraint, table, f"{column} IN ({', '.join(repr(v) for v in values)})")


def downgrade():
    # Las columnas y restricciones pueden contener datos preexistentes.
    pass
