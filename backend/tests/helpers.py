from datetime import datetime

from extensions import db
from models import Product, Receta, RecetaItem


def crear_receta(producto_id, items, version=1, desde=None, hasta=None):
    """Siembra una versión de receta. `items` son dicts con los campos de RecetaItem (nombre, tipo_calculo...)."""
    if db.session.get(Product, producto_id) is None:
        db.session.add(Product(id=producto_id, nombre=f"Producto {producto_id}"))
    receta = Receta(producto_id=producto_id, version=version,
                    vigente_desde=desde or datetime(2000, 1, 1), vigente_hasta=hasta)
    for orden, datos in enumerate(items):
        datos = dict(datos)
        datos.setdefault('nombre', 'Componente')
        receta.items.append(RecetaItem(orden=orden, **datos))
    db.session.add(receta)
    db.session.commit()
    return receta
