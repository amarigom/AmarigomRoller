"""Calculo de la explosion de materiales de una receta (sin acceso a base de datos)."""

UNIDADES_METRO = {'metro', 'metros', 'm', 'mt', 'mts', 'ml'}
UNIDADES_M2 = {'m2', 'm²'}
TIPOS_TELA = {'lineal_alto', 'superficie'}
TIPOS_LINEALES = {'lineal_alto', 'lineal_ancho', 'superficie'}


def cm_a_unidad(cm_lineales, ancho_cm, unidad, tipo_calculo):
    """Convierte el consumo en cm a la unidad en que esta cargado el precio del insumo."""
    if unidad in UNIDADES_METRO:
        return cm_lineales / 100.0
    if unidad in UNIDADES_M2 and tipo_calculo == 'superficie':
        return (ancho_cm * cm_lineales) / 10000.0
    if unidad in UNIDADES_M2:
        return cm_lineales / 100.0
    return cm_lineales


def buscar_retazo(retazos, ancho_corte, alto_corte):
    """Devuelve el retazo disponible mas chico que cubre la medida, o None."""
    candidatos = [
        r for r in retazos
        if float(r.ancho_cm) >= ancho_corte and float(r.largo_cm) >= alto_corte
    ]
    if not candidatos:
        return None
    return min(candidatos, key=lambda r: float(r.ancho_cm) * float(r.largo_cm))


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
        nombre = (insumo.name if insumo else None) or item.nombre_producto or "Insumo sin nombre"
        precio_unitario = float((insumo.precio_costo_unitario if insumo else 0) or 0)
        unidad = ((insumo.unidad_medida if insumo else None) or 'metro').strip().lower()

        ancho_corte = w_pedido + float(item.delta_ancho_cm or 0)
        alto_corte = h_pedido + float(item.delta_alto_cm or 0)

        metodo = "ROLLO"
        id_retazo = None
        mensaje = ""
        consumo_cm = alto_corte

        if item.tipo_calculo in TIPOS_TELA:
            disponibles = [
                r for r in retazos_por_insumo.get(item.id_insumo, [])
                if r.id not in retazos_usados
            ]
            retazo = buscar_retazo(disponibles, ancho_corte, alto_corte)
            if retazo:
                retazos_usados.add(retazo.id)
                metodo = "RETAZO"
                id_retazo = retazo.id
                mensaje = f"Usar retazo de {int(retazo.ancho_cm)}x{int(retazo.largo_cm)} cm"
                consumo_cm = 1.0
        elif item.tipo_calculo == 'lineal_ancho':
            metodo = "BARRA"
            consumo_cm = ancho_corte
        elif item.tipo_calculo == 'fijo':
            metodo = "UNIDAD"
            consumo_cm = float(item.cantidad_base or 1.0)

        if item.tipo_calculo in TIPOS_LINEALES:
            cm_lineales = ancho_corte if item.tipo_calculo == 'lineal_ancho' else alto_corte
            consumo_unidad = cm_a_unidad(cm_lineales, ancho_corte, unidad, item.tipo_calculo)
        else:
            consumo_unidad = consumo_cm

        # Un retazo ya fue pagado como parte del rollo original: no suma costo
        costo_parcial = 0.0 if metodo == "RETAZO" else round(consumo_unidad * precio_unitario, 2)

        resultado.append({
            "componente": nombre,
            "consumo_m_o_m2": round(consumo_unidad, 4),
            "unidad": unidad,
            "consumo_cm": round(consumo_cm, 2),
            "medida_corte": f"{ancho_corte} x {alto_corte} cm",
            "precio_unitario": precio_unitario,
            "costo_parcial": costo_parcial,
            "metodo": metodo,
            "id_retazo": id_retazo,
            "mensaje": mensaje,
        })

    total = round(sum(i['costo_parcial'] for i in resultado), 2)
    return resultado, total
