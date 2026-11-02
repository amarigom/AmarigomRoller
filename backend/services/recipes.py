from decimal import Decimal

from exceptions import ConflictError, NotFoundError
from repositories.recipe import RecipeRepository, ScrapRepository
from repositories.supply import SupplyRepository
from schemas.recipes import ExplosionItemOut, ExplosionOut, ProduccionOut, RecipeItemOut, StockDescontadoOut
from services.costeo import calcular_explosion


class RecipeService:
    def __init__(self, recipes=None, scraps=None, supplies=None):
        self.recipes = recipes or RecipeRepository()
        self.scraps = scraps or ScrapRepository()
        self.supplies = supplies or SupplyRepository()

    def base_recipe(self, product_id):
        componentes = self.recipes.components_for_product(product_id)
        if not componentes:
            raise NotFoundError(f"El producto {product_id} no tiene una receta definida en la base de datos.")
        return [RecipeItemOut.from_model(c) for c in componentes]

    def _calcular(self, product_id, w, h):
        componentes = self.recipes.components_for_product(product_id)
        if not componentes:
            raise NotFoundError(f"El producto {product_id} aún no tiene definida su explosión de materiales.")
        ids_insumo = {c.id_insumo for c in componentes if c.id_insumo}
        retazos = self.scraps.available_by_supply(ids_insumo)
        resultado, total = calcular_explosion(componentes, retazos, w, h)
        return componentes, resultado, total

    def explode(self, product_id, w, h):
        _, resultado, total = self._calcular(product_id, w, h)
        return ExplosionOut(
            explosion=[ExplosionItemOut(**r) for r in resultado],
            total_materiales=total,
        )

    def produce(self, product_id, w, h):
        """Confirma una producción: descuenta stock y marca como usados los retazos.

        Se recalcula en el servidor (el cliente solo manda las medidas) y todo se aplica
        en una única transacción: si algo falta, no se descuenta nada.
        """
        componentes, resultado, total = self._calcular(product_id, w, h)

        retazos_ids = {r['id_retazo'] for r in resultado if r['id_retazo'] is not None}
        retazos = self.scraps.lock_available(retazos_ids)
        if retazos_ids - set(retazos):
            self.scraps.session.rollback()
            raise ConflictError("Un retazo ya fue usado por otra producción. Recalculá la receta.")

        necesario = {}
        for item, r in zip(componentes, resultado):
            if r['metodo'] != 'RETAZO' and item.id_insumo:
                necesario[item.id_insumo] = necesario.get(item.id_insumo, Decimal(0)) + Decimal(str(r['consumo_m_o_m2']))

        insumos = self.supplies.lock_many(list(necesario))
        faltantes = []
        for insumo_id, cantidad in necesario.items():
            insumo = insumos.get(insumo_id)
            disponible = Decimal(insumo.stock_actual or 0) if insumo else Decimal(0)
            if disponible < cantidad:
                nombre = insumo.name if insumo else f"insumo {insumo_id}"
                faltantes.append(f"{nombre}: necesita {cantidad}, hay {disponible}")
        if faltantes:
            self.supplies.session.rollback()
            raise ConflictError("Stock insuficiente para producir", detalles=faltantes)

        descontados = []
        for insumo_id, cantidad in necesario.items():
            insumo = insumos[insumo_id]
            insumo.stock_actual = Decimal(insumo.stock_actual or 0) - cantidad
            descontados.append(StockDescontadoOut(
                id_insumo=insumo_id, insumo=insumo.name, cantidad=float(cantidad),
                stock_restante=float(insumo.stock_actual), unidad=insumo.unidad_medida))
        for retazo in retazos.values():
            retazo.estado = 'usado'
        self.supplies.commit()

        return ProduccionOut(
            descontado=descontados,
            retazos_usados=sorted(retazos),
            total_materiales=total,
        )
