"""Explosión de materiales de una receta (sin acceso a base de datos). La lógica por tipo vive en strategies.costing."""
from dataclasses import asdict

from exceptions import UnprocessableError
from strategies import formulas
from strategies.costing import (
    MIN_RETAZO_PERFIL_CM, ComponentInput, get_strategy, usa_perfiles, usa_retazos,
)


def _contexto(w, h, opciones):
    # Las opciones no pueden pisar las medidas del pedido
    return {**(opciones or {}), 'ancho': float(w), 'alto': float(h)}


def _evaluar(item, texto, contexto, numerico):
    nombre = getattr(item, 'nombre', None) or getattr(item, 'nombre_producto', None) or 'componente'
    try:
        return formulas.evaluar_numero(texto, contexto) if numerico else formulas.evaluar_condicion(texto, contexto)
    except formulas.FormulaError as exc:
        raise UnprocessableError(f"{nombre}: {exc} (fórmula '{texto}')")


def calcular_explosion(componentes, retazos_por_insumo, w_pedido, h_pedido,
                       sobrantes_perfil=None, min_retazo_cm=MIN_RETAZO_PERFIL_CM, opciones=None):
    """
    componentes: ítems de receta con su insumo ya cargado.
    retazos_por_insumo: {id_insumo: [retazos de tela disponibles]}.
    sobrantes_perfil: {id_insumo: [piezas sobrantes de perfil]} con `id` y `longitud_actual_cm`.
    opciones: variantes del pedido (sistema, color...) que usan las condiciones y fórmulas.
    Devuelve (lista de componentes calculados, total de materiales). Los ítems cuya
    condición da falso no aparecen en el resultado.
    """
    resultado = []
    retazos_usados = set()
    contexto = _contexto(w_pedido, h_pedido, opciones)
    pool_perfiles = {
        id_insumo: [
            {'id': p.id, 'tok': f"p{p.id}", 'largo': float(p.longitud_actual_cm)}
            for p in piezas
        ]
        for id_insumo, piezas in (sobrantes_perfil or {}).items()
    }

    for item in componentes:
        condicion = getattr(item, 'condicion', None)
        if condicion and not _evaluar(item, condicion, contexto, numerico=False):
            continue

        insumo = item.insumo
        strategy = get_strategy(item.tipo_calculo)

        retazos = []
        if usa_retazos(item.tipo_calculo):
            retazos = [
                r for r in retazos_por_insumo.get(item.id_insumo, [])
                if r.id not in retazos_usados
            ]
        elif usa_perfiles(item.tipo_calculo):
            retazos = pool_perfiles.setdefault(item.id_insumo, [])

        ancho = w_pedido + float(item.delta_ancho_cm or 0)
        alto = h_pedido + float(item.delta_alto_cm or 0)
        cantidad = float(item.cantidad_base or 1.0)
        if getattr(item, 'formula_ancho', None):
            ancho = _evaluar(item, item.formula_ancho, contexto, numerico=True)
        if getattr(item, 'formula_alto', None):
            alto = _evaluar(item, item.formula_alto, contexto, numerico=True)
        if getattr(item, 'formula_cantidad', None):
            cantidad = _evaluar(item, item.formula_cantidad, contexto, numerico=True)

        largo_pieza = getattr(insumo, 'largo_pieza_cm', None) if insumo else None
        calculo = strategy.calculate(ComponentInput(
            nombre=(insumo.name if insumo else None) or getattr(item, 'nombre', None)
            or getattr(item, 'nombre_producto', None) or "Insumo sin nombre",
            unidad=((insumo.unidad_medida if insumo else None) or 'metro').strip().lower(),
            precio_unitario=float((insumo.precio_costo_unitario if insumo else 0) or 0),
            ancho_corte=ancho,
            alto_corte=alto,
            cantidad_base=cantidad,
            retazos=retazos,
            merma_pct=float(getattr(item, 'merma_pct', 0) or 0),
            minutos=float(getattr(item, 'minutos_mano_obra', 0) or 0),
            largo_pieza_cm=float(largo_pieza) if largo_pieza else None,
            min_retazo_cm=min_retazo_cm,
        ))
        if calculo.id_retazo is not None:
            retazos_usados.add(calculo.id_retazo)
        fila = asdict(calculo)
        fila['id_insumo'] = item.id_insumo
        resultado.append(fila)

    total = round(sum(i['costo_parcial'] for i in resultado), 2)
    return resultado, total
