from decimal import Decimal, ROUND_HALF_UP

from flask import current_app


CENTAVOS = Decimal('0.01')
MARKUP = Decimal('1.00')


def _importe(valor):
    return valor.quantize(CENTAVOS, rounding=ROUND_HALF_UP)


def calcular_cotizacion(explosion, km_ida):
    costo = _importe(Decimal(str(explosion.total)))
    reposicion = sum((Decimal(str(item.costo_reposicion)) for item in explosion.explosion), Decimal(0))
    precio = _importe((costo + reposicion) * (1 + MARKUP))
    ganancia = precio - costo
    margen = _importe(ganancia * 100 / precio) if precio else Decimal(0)
    tarifa = Decimal(str(current_app.config['TARIFA_BASE_COLOCACION']))
    costo_km = Decimal(str(current_app.config['COSTO_POR_KM']))
    if not tarifa.is_finite() or not costo_km.is_finite() or tarifa < 0 or costo_km < 0:
        raise ValueError("Las tarifas de colocación y traslado deben ser finitas y no negativas")
    tarifa = _importe(tarifa)
    km_totales = km_ida * 2
    traslado = _importe(km_totales * costo_km)
    colocacion = tarifa + traslado
    return {
        'desglose_fabricacion': {
            'costo_materiales': explosion.total_materiales,
            'costo_operaciones': explosion.total_mano_obra,
            'costo_desgaste': explosion.total_desgaste,
            'costo_total_fabricacion': float(costo),
        },
        'precio_producto': {
            'markup_pct': float(MARKUP * 100),
            'ganancia_markup': float(ganancia),
            'margen_sobre_ventas_pct': float(margen),
            'precio_venta_final': float(precio),
        },
        'servicio_colocacion': {
            'tarifa_base': float(tarifa),
            'km_ida': float(km_ida),
            'km_totales': float(km_totales),
            'costo_traslado': float(traslado),
            'total_colocacion': float(colocacion),
        },
        'total_presupuesto': float(precio + colocacion),
    }
