"""Explosión de materiales de una receta (sin acceso a base de datos). La lógica por tipo vive en strategies.costing."""
from dataclasses import asdict

from strategies.costing import ComponentInput, get_strategy, usa_retazos


def calcular_explosion(componentes, retazos_por_insumo, w_pedido, h_pedido):
    """
    componentes: filas de receta con su insumo ya cargado.
    retazos_por_insumo: {id_insumo: [retazos disponibles]}.
    Devuelve (lista de componentes calculados, total de materiales).
    """
    resultado = []
    retazos_usados = set()

    for item in componentes:
        insumo = item.insumo
        strategy = get_strategy(item.tipo_calculo)

        retazos = []
        if usa_retazos(item.tipo_calculo):
            retazos = [
                r for r in retazos_por_insumo.get(item.id_insumo, [])
                if r.id not in retazos_usados
            ]

        calculo = strategy.calculate(ComponentInput(
            nombre=(insumo.name if insumo else None) or item.nombre_producto or "Insumo sin nombre",
            unidad=((insumo.unidad_medida if insumo else None) or 'metro').strip().lower(),
            precio_unitario=float((insumo.precio_costo_unitario if insumo else 0) or 0),
            ancho_corte=w_pedido + float(item.delta_ancho_cm or 0),
            alto_corte=h_pedido + float(item.delta_alto_cm or 0),
            cantidad_base=float(item.cantidad_base or 1.0),
            retazos=retazos,
        ))
        if calculo.id_retazo is not None:
            retazos_usados.add(calculo.id_retazo)
        resultado.append(asdict(calculo))

    total = round(sum(i['costo_parcial'] for i in resultado), 2)
    return resultado, total
