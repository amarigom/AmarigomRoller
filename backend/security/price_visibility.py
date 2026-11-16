from flask import g

from security.permissions import COSTS_READ, has_permission


def puede_ver_costos():
    return has_permission(g.current_user.rol, COSTS_READ)


def _seleccionar(datos, campos):
    return {campo: datos[campo] for campo in campos if campo in datos}


def _material(item):
    salida = _seleccionar(item, (
        'id_insumo', 'componente', 'consumo_m_o_m2', 'unidad', 'consumo_cm', 'medida_corte',
        'metodo', 'id_retazo', 'mensaje', 'merma_pct', 'minutos',
    ))
    if 'cortes' in item:
        salida['cortes'] = [
            _seleccionar(corte, ('origen', 'id_pieza', 'largo_origen', 'corte', 'sobrante',
                                'reutilizable', 'desperdicio'))
            for corte in item['cortes']
        ]
    return salida


def explosion_visible(datos):
    if puede_ver_costos():
        return datos
    salida = _seleccionar(datos, ('status', 'version', 'total_minutos'))
    salida['explosion'] = [_material(item) for item in datos['explosion']]
    return salida


def cotizacion_visible(datos):
    if puede_ver_costos():
        return datos
    salida = explosion_visible(datos)
    salida.update(_seleccionar(datos, ('receta_id', 'total_presupuesto')))
    salida['precio_producto'] = _seleccionar(datos['precio_producto'], ('precio_venta_final',))
    salida['servicio_colocacion'] = _seleccionar(
        datos['servicio_colocacion'], ('km_ida', 'km_totales', 'total_colocacion'))
    return salida


def presupuesto_visible(datos):
    if puede_ver_costos():
        return datos
    salida = _seleccionar(datos, ('id', 'producto_id', 'producto_nombre', 'receta_id', 'receta_version',
                                 'ancho_cm', 'alto_cm', 'referencia', 'opciones', 'usuario', 'creado_en'))
    salida['resultado'] = cotizacion_visible(datos['resultado'])
    return salida


def produccion_visible(datos):
    if puede_ver_costos():
        return datos
    salida = _seleccionar(datos, ('status', 'produccion_id', 'version', 'descontado', 'retazos_usados',
                                 'retazos_perfil_generados', 'retazos_tela_generados', 'total_minutos'))
    salida['descontado'] = [
        _seleccionar(item, ('id_insumo', 'insumo', 'cantidad', 'stock_restante', 'unidad'))
        for item in datos['descontado']
    ]
    return salida


def historial_produccion_visible(datos):
    if puede_ver_costos():
        return datos
    salida = _seleccionar(datos, ('id', 'producto_id', 'producto_nombre', 'receta_version', 'ancho_cm',
                                 'alto_cm', 'opciones', 'referencia', 'total_minutos', 'usuario', 'creado_en'))
    salida['detalle'] = [_material(item) for item in datos['detalle']]
    return salida
