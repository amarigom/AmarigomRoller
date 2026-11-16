"""unidades, perfiles por pieza, merma y mano de obra

- insumos.largo_pieza_cm: largo de la pieza que se compra (perfil de 2/4/6 m, rollo de cinta)
- recetas_bom.merma_pct y minutos_mano_obra
- stock_piezas_detalle: sobrantes de perfil (se crea solo si no existe)
- corrige datos existentes: espagueti por metro, cintas por rollo de 50 m, perfiles con tipo 'perfil'
  y el 5% de tela que estaba en cantidad_base pasa a merma_pct

Revision ID: 0003_unidades_perfiles
Revises: 0002_usuarios
Create Date: 2026-11-03
"""
import re

from alembic import op
import sqlalchemy as sa

revision = '0003_unidades_perfiles'
down_revision = '0002_usuarios'
branch_labels = None
depends_on = None

_PIEZA_METROS = re.compile(r'x\s*(\d+(?:[.,]\d+)?)\s*mts?\b', re.IGNORECASE)
_ROLLO_METROS = re.compile(r'(?:\(|rollo\s+)(\d+(?:[.,]\d+)?)\s*(?:mts?|m)\b', re.IGNORECASE)
_ES_PERFIL = re.compile(r'^\s*(tubo|perfil)', re.IGNORECASE)
_ES_CINTA = re.compile(r'^\s*cinta', re.IGNORECASE)
_ES_ESPAGUETI = re.compile(r'^\s*espagueti', re.IGNORECASE)


def largo_pieza_cm(nombre):
    """Largo de la pieza comprada según el nombre del insumo ('x 4 mts', '(50 mts)', 'Rollo 200m')."""
    for patron in (_PIEZA_METROS, _ROLLO_METROS):
        m = patron.search(nombre or '')
        if m:
            return round(float(m.group(1).replace(',', '.')) * 100, 2)
    return None


def _add_column(bind, table, column):
    cols = {c['name'] for c in sa.inspect(bind).get_columns(table)}
    if column.name not in cols:
        op.add_column(table, column)


def _ampliar_check(bind, table, nombre, columna, valores):
    """Reemplaza un CHECK de lista de valores por una lista ampliada (solo PostgreSQL)."""
    if bind.dialect.name != 'postgresql':
        return
    existentes = {c['name'] for c in sa.inspect(bind).get_check_constraints(table)}
    if nombre in existentes:
        op.drop_constraint(nombre, table, type_='check')
    lista = ", ".join(f"'{v}'" for v in valores)
    op.create_check_constraint(nombre, table, f"{columna} IN ({lista})")


def upgrade():
    bind = op.get_bind()
    _ampliar_check(bind, 'insumos', 'insumos_unidad_medida_check', 'unidad_medida',
                   ['unidad', 'cm', 'metro', 'm2', 'rollo'])
    _ampliar_check(bind, 'recetas_bom', 'recetas_bom_tipo_calculo_check', 'tipo_calculo',
                   ['lineal_ancho', 'lineal_alto', 'fijo', 'superficie', 'perfil', 'mano_obra'])
    _add_column(bind, 'insumos', sa.Column('largo_pieza_cm', sa.Numeric(10, 2)))
    _add_column(bind, 'recetas_bom', sa.Column('merma_pct', sa.Numeric(5, 2), server_default='0'))
    _add_column(bind, 'recetas_bom', sa.Column('minutos_mano_obra', sa.Numeric(8, 2), server_default='0'))

    if 'stock_piezas_detalle' not in sa.inspect(bind).get_table_names():
        op.create_table(
            'stock_piezas_detalle',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('id_insumo', sa.Integer(), sa.ForeignKey('insumos.id'), nullable=False),
            sa.Column('longitud_original_cm', sa.Numeric(10, 2), nullable=False),
            sa.Column('longitud_actual_cm', sa.Numeric(10, 2), nullable=False),
            sa.Column('es_retazo', sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.Column('fecha_ingreso', sa.DateTime(), server_default=sa.func.current_timestamp()),
        )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_stock_piezas_insumo_retazo "
        "ON stock_piezas_detalle (id_insumo, es_retazo)"
    )

    insumos = bind.execute(sa.text("SELECT id, name, unidad_medida, largo_pieza_cm FROM insumos")).fetchall()
    perfiles = []
    for id_, nombre, _unidad, largo_actual in insumos:
        largo = largo_pieza_cm(nombre)
        if largo and not largo_actual:
            bind.execute(sa.text("UPDATE insumos SET largo_pieza_cm = :l WHERE id = :i"), {'l': largo, 'i': id_})
        if _ES_ESPAGUETI.match(nombre or ''):
            bind.execute(sa.text("UPDATE insumos SET unidad_medida = 'metro' WHERE id = :i"), {'i': id_})
        elif _ES_CINTA.match(nombre or '') and (largo or largo_actual):
            bind.execute(sa.text("UPDATE insumos SET unidad_medida = 'rollo' WHERE id = :i"), {'i': id_})
        elif _ES_PERFIL.match(nombre or '') and (largo or largo_actual):
            perfiles.append(id_)

    for id_ in perfiles:
        bind.execute(
            sa.text("UPDATE recetas_bom SET tipo_calculo = 'perfil' "
                    "WHERE id_insumo = :i AND tipo_calculo = 'lineal_ancho'"),
            {'i': id_},
        )

    # La tela usaba cantidad_base = 1.05 como merma, pero ese campo no se aplicaba al costo
    bind.execute(sa.text(
        "UPDATE recetas_bom SET merma_pct = ROUND((cantidad_base - 1) * 100, 2), cantidad_base = 1 "
        "WHERE tipo_calculo IN ('lineal_alto', 'superficie') AND cantidad_base > 1 AND cantidad_base <= 2 "
        "AND COALESCE(merma_pct, 0) = 0"
    ))


def downgrade():
    op.drop_index('ix_stock_piezas_insumo_retazo', table_name='stock_piezas_detalle')
    op.drop_column('recetas_bom', 'minutos_mano_obra')
    op.drop_column('recetas_bom', 'merma_pct')
    op.drop_column('insumos', 'largo_pieza_cm')
