from exceptions import ConflictError
from models import Product
from repositories.recipe import ahora
from schemas.recipes import RecipeItemIn, RecipeVersionIn
from services.normalizacion_inicial import normalizar_inicial
from services.recipes import RecipeService


def preparar_telas_lineales(aplicar=False, plan_esperado=None, commit=True):
    servicio = RecipeService()
    session = servicio.recipes.session
    plan = normalizar_inicial(aplicar=True, commit=False)
    session.flush()
    productos = Product.query.order_by(Product.id).with_for_update().all()
    for producto in productos:
        receta = servicio.recipes.vigente(producto.id, ahora())
        if receta is None:
            continue
        if any(i.tipo_calculo == 'superficie' and (not i.insumo or not i.insumo.es_tela) for i in receta.items):
            raise ConflictError(f'Producto {producto.id}: un ítem por superficie no tiene una tela normalizada')
        afectados = [i for i in receta.items if i.tipo_calculo == 'superficie' and i.insumo and i.insumo.es_tela]
        if not afectados:
            continue
        items = []
        for item in receta.items:
            campos = {key: getattr(item, key) for key in RecipeItemIn.model_fields}
            if item in afectados:
                campos['tipo_calculo'] = 'lineal_alto'
            items.append(RecipeItemIn(**campos))
        nueva = servicio.publish_version(
            producto.id, RecipeVersionIn(items=items, nota='Tela por metro lineal'), commit=False)
        plan.append(f'Producto {producto.id}: receta v{receta.version} -> v{nueva.version}, tela por metro lineal')
    if plan_esperado is not None and plan != plan_esperado:
        raise ConflictError('El plan cambió desde la simulación; revisalo antes de aplicar')
    if aplicar and commit:
        session.commit()
    elif aplicar:
        session.flush()
    else:
        session.rollback()
    return plan
