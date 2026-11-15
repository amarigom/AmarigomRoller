from decimal import Decimal

from extensions import db
from models import InventoryMovement, PiezaStock, Product, Receta, RecetaItem, Supply, SupplyCategory, SupplyPriceHistory
from repositories.recipe import ahora
from services.production_costs import ETIQUETA_SKU

SKUS = ('DEMO-TELA-300', 'DEMO-PERFIL-400')
NOMBRES = ('DEMO Roller', 'DEMO Cortina tradicional')


def cargar_demo():
    if Supply.query.filter(Supply.codigo_sku.in_(SKUS)).first() or Product.query.filter(Product.nombre.in_(NOMBRES)).first():
        raise ValueError('Ya existen datos DEMO con esos códigos o nombres; no se modificó nada')
    etiqueta = Supply.query.filter_by(codigo_sku=ETIQUETA_SKU, activo=True).with_for_update().first()
    if etiqueta is None:
        raise ValueError('Falta el insumo obligatorio Etiqueta; aplicá las migraciones')
    categoria = SupplyCategory.query.filter_by(name='DEMO Fabricación').first()
    if categoria is None:
        categoria = SupplyCategory(name='DEMO Fabricación')
        db.session.add(categoria)
        db.session.flush()
    tela = Supply(categoria_id=categoria.id, codigo_sku=SKUS[0], name='DEMO Tela ancho 300 cm',
                  unidad_medida='metro', ancho_cm=300, largo_pieza_cm=3000, es_tela=True,
                  unidad_compra='rollo', factor_conversion=30,
                  precio_costo_unitario=3000, stock_actual=30, stock_minimo=5)
    perfil = Supply(categoria_id=categoria.id, codigo_sku=SKUS[1], name='DEMO Perfil 400 cm',
                    unidad_medida='cm', largo_pieza_cm=400, precio_costo_unitario=20,
                    stock_actual=1200, stock_minimo=400)
    db.session.add_all([tela, perfil])
    db.session.flush()
    for insumo in (tela, perfil):
        db.session.add(InventoryMovement(id_insumo=insumo.id, tipo='apertura', cantidad=insumo.stock_actual,
                                         stock_resultante=insumo.stock_actual, unidad=insumo.unidad_medida,
                                         referencia='Carga DEMO'))
        db.session.add(SupplyPriceHistory(id_insumo=insumo.id, precio=insumo.precio_costo_unitario,
                                          unidad=insumo.unidad_medida, precio_m2=insumo.precio_m2, motivo='Carga DEMO'))
    db.session.add_all([PiezaStock(id_insumo=perfil.id, longitud_original_cm=400,
                                   longitud_actual_cm=400, es_retazo=False) for _ in range(3)])
    if Decimal(etiqueta.stock_actual or 0) < 10:
        cantidad = Decimal(10) - Decimal(etiqueta.stock_actual or 0)
        etiqueta.stock_actual = Decimal(10)
        db.session.add(InventoryMovement(id_insumo=etiqueta.id, tipo='entrada', cantidad=cantidad,
                                         stock_resultante=10, unidad=etiqueta.unidad_medida, referencia='Carga DEMO',
                                         notas='Etiquetas ficticias para pruebas'))
    roller = Product(nombre=NOMBRES[0], categoria='DEMO', activo=True)
    tradicional = Product(nombre=NOMBRES[1], categoria='DEMO', activo=True)
    db.session.add_all([roller, tradicional])
    db.session.flush()
    for producto in (roller, tradicional):
        receta = Receta(producto_id=producto.id, version=1, vigente_desde=ahora(), nota='Carga DEMO ficticia')
        receta.items.append(RecetaItem(orden=0, id_insumo=tela.id, nombre='Tela', tipo_calculo='lineal_alto',
                                       cantidad_base=1, merma_pct=5))
        if producto is roller:
            receta.items.append(RecetaItem(orden=1, id_insumo=perfil.id, nombre='Perfil', tipo_calculo='perfil',
                                           cantidad_base=1, merma_pct=0))
        db.session.add(receta)
    db.session.commit()
