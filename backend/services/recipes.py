from exceptions import NotFoundError
from repositories.recipe import RecipeRepository, ScrapRepository
from schemas.recipes import ExplosionItemOut, ExplosionOut, RecipeItemOut
from services.costeo import calcular_explosion


class RecipeService:
    def __init__(self, recipes=None, scraps=None):
        self.recipes = recipes or RecipeRepository()
        self.scraps = scraps or ScrapRepository()

    def base_recipe(self, product_id):
        componentes = self.recipes.components_for_product(product_id)
        if not componentes:
            raise NotFoundError(f"El producto {product_id} no tiene una receta definida en la base de datos.")
        return [RecipeItemOut.from_model(c) for c in componentes]

    def explode(self, product_id, w, h):
        componentes = self.recipes.components_for_product(product_id)
        if not componentes:
            raise NotFoundError(f"El producto {product_id} aún no tiene definida su explosión de materiales.")
        ids_insumo = {c.id_insumo for c in componentes if c.id_insumo}
        retazos = self.scraps.available_by_supply(ids_insumo)
        resultado, total = calcular_explosion(componentes, retazos, w, h)
        return ExplosionOut(
            explosion=[ExplosionItemOut(**r) for r in resultado],
            total_materiales=total,
        )
