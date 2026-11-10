"""Explosión de materiales de una receta (sin acceso a base de datos). La lógica por tipo vive en strategies.costing."""
from dataclasses import asdict

from flask import current_app, has_app_context

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


def _elegir_perfil(item, corte, extras):
    """Perfil que cubre el corte: el de la receta si alcanza; si no, la alternativa más corta que alcance."""
    nombre = getattr(item, 'nombre', None) or getattr(item, 'nombre_producto', None) or 'componente'
    candidatos = [(item.id_insumo, item.insumo)]
    candidatos += [(i, extras[i]) for i in (getattr(item, 'insumos_alternativos', None) or []) if i in extras]
    con_largo = [(i, s) for i, s in candidatos if s is not None and getattr(s, 'largo_pieza_cm', None)]
    if not con_largo:
        return item.id_insumo, item.insumo
    largo = lambda par: float(par[1].largo_pieza_cm)
    principal = con_largo[0]
    if candidatos[0] == principal and largo(principal) + 1e-9 >= corte:
        return principal
    alcanzan = sorted((p for p in con_largo if largo(p) + 1e-9 >= corte), key=lambda p: (largo(p), p[0]))
    if not alcanzan:
        raise UnprocessableError(
            f"{nombre}: el corte de {corte:g} cm no entra en ningún perfil disponible "
            f"(el más largo mide {max(largo(p) for p in con_largo):g} cm). "
            "Agregá un perfil más largo como alternativa en la receta.")
    return alcanzan[0]


def calcular_explosion(componentes, retazos_por_insumo, w_pedido, h_pedido,
                       sobrantes_perfil=None, min_retazo_cm=MIN_RETAZO_PERFIL_CM, opciones=None,
                       insumos_alternativos=None):
    """
    componentes: ítems de receta con su insumo ya cargado.
    retazos_por_insumo: {id_insumo: [retazos de tela disponibles]}.
    sobrantes_perfil: {id_insumo: [piezas sobrantes de perfil]} con `id` y `longitud_actual_cm`.
    opciones: variantes del pedido (sistema, color...) que usan las condiciones y fórmulas.
    insumos_alternativos: {id: insumo} de los perfiles alternativos que pueden reemplazar al de la receta.
    Devuelve (lista de componentes calculados, total de materiales). Los ítems cuya
    condición da falso no aparecen en el resultado.
    """
    resultado = []
    retazos_usados = set()
    extras = insumos_alternativos or {}
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

        strategy = get_strategy(item.tipo_calculo)

        ancho = w_pedido + float(item.delta_ancho_cm or 0)
        alto = h_pedido + float(item.delta_alto_cm or 0)
        cantidad = float(item.cantidad_base or 1.0)
        if getattr(item, 'formula_ancho', None):
            ancho = _evaluar(item, item.formula_ancho, contexto, numerico=True)
        if getattr(item, 'formula_alto', None):
            alto = _evaluar(item, item.formula_alto, contexto, numerico=True)
        if getattr(item, 'formula_cantidad', None):
            cantidad = _evaluar(item, item.formula_cantidad, contexto, numerico=True)

        id_insumo, insumo = item.id_insumo, item.insumo
        retazos = []
        if usa_retazos(item.tipo_calculo):
            retazos = [
                r for r in retazos_por_insumo.get(id_insumo, [])
                if r.id not in retazos_usados
            ]
        elif usa_perfiles(item.tipo_calculo):
            id_insumo, insumo = _elegir_perfil(item, round(ancho, 2), extras)
            retazos = pool_perfiles.setdefault(id_insumo, [])

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
        fila['id_insumo'] = id_insumo
        if item.tipo_calculo in ('lineal_alto', 'superficie') and calculo.metodo == 'ROLLO' and insumo:
            ancho_sobrante = round(float(getattr(insumo, 'ancho_cm', 0) or 0) - ancho, 2)
            minimo_retazo_tela = (
                float(current_app.config.get('MIN_RETAZO_TELA_CM', 80)) if has_app_context() else 80.0
            )
            if ancho_sobrante > minimo_retazo_tela and alto > minimo_retazo_tela:
                fila['retazo_tela'] = {
                    'ancho_cm': ancho_sobrante,
                    'largo_cm': round(alto, 2),
                    'id_insumo': id_insumo,
                }
        resultado.append(fila)

    total = round(sum(i['costo_parcial'] for i in resultado), 2)
    return resultado, total
