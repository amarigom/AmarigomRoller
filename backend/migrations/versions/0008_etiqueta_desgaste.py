"""Insumo de etiqueta y costo de desgaste en producciones.

Revision ID: 0008_etiqueta_desgaste
Revises: 0007_historial_producciones
"""
from alembic import op
import sqlalchemy as sa

revision = '0008_etiqueta_desgaste'
down_revision = '0007_historial_producciones'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    columnas = {c['name'] for c in sa.inspect(bind).get_columns('producciones')}
    if 'total_desgaste' not in columnas:
        op.add_column('producciones', sa.Column(
            'total_desgaste', sa.Numeric(14, 2), nullable=False, server_default='0'))

    sku = 'ROLLER-ETIQUETA'
    existente = bind.execute(sa.text(
        "SELECT id, codigo_sku, name, unidad_medida FROM insumos "
        "WHERE codigo_sku = :sku OR lower(trim(name)) = 'etiqueta'"
    ), {'sku': sku}).all()
    if existente:
        if (len(existente) == 1 and existente[0].codigo_sku == sku
                and existente[0].name == 'Etiqueta' and existente[0].unidad_medida == 'unidad'):
            return
        raise RuntimeError("Ya existe un insumo Etiqueta o el SKU ROLLER-ETIQUETA. Revisá los datos antes de migrar.")
    bind.execute(sa.text(
        "INSERT INTO categorias_insumos (name) SELECT 'Accesorios' "
        "WHERE NOT EXISTS (SELECT 1 FROM categorias_insumos WHERE name = 'Accesorios')"))
    bind.execute(sa.text(
        "INSERT INTO insumos (categoria_id, codigo_sku, name, unidad_medida, precio_costo_unitario, "
        "stock_actual, stock_minimo, activo) "
        "SELECT id, :sku, 'Etiqueta', 'unidad', 200, 0, 0, :activo "
        "FROM categorias_insumos WHERE name = 'Accesorios'"), {'sku': sku, 'activo': True})
    bind.execute(sa.text(
        "INSERT INTO historial_precios_insumos (id_insumo, precio, motivo) "
        "SELECT id, 200, 'Precio inicial de etiqueta' FROM insumos WHERE codigo_sku = :sku"), {'sku': sku})
    bind.execute(sa.text(
        "INSERT INTO inventario_movimientos (id_insumo, tipo, cantidad, stock_resultante, referencia) "
        "SELECT id, 'apertura', 0, 0, 'Alta de etiqueta' FROM insumos WHERE codigo_sku = :sku"), {'sku': sku})


def downgrade():
    # El insumo y su historial pueden tener movimientos posteriores y deben conservarse.
    op.drop_column('producciones', 'total_desgaste')
