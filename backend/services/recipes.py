from decimal import Decimal

from flask import current_app

from exceptions import ConflictError, NotFoundError
from models import PiezaStock
from repositories.recipe import PieceRepository, RecipeRepository, ScrapRepository
from repositories.supply import SupplyRepository
from schemas.recipes import ExplosionItemOut, ExplosionOut, ProduccionOut, RecipeItemOut, StockDescontadoOut
from services.costeo import calcular_explosion
from strategies.costing import MIN_RETAZO_PERFIL_CM, usa_perfiles


class RecipeService:
    def __init__(self, recipes=None, scraps=None, supplies=None, pieces=None):
        self.recipes = recipes or RecipeRepository()
        self.scraps = scraps or ScrapRepository()
        self.supplies = supplies or SupplyRepository()
        self.pieces = pieces or PieceRepository()

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
        ids_perfil = {c.id_insumo for c in componentes if c.id_insumo and usa_perfiles(c.tipo_calculo)}
        retazos = self.scraps.available_by_supply(ids_insumo)
        sobrantes = self.pieces.remnants_by_supply(ids_perfil)
        resultado, total = calcular_explosion(
            componentes, retazos, w, h, sobrantes_perfil=sobrantes,
            min_retazo_cm=current_app.config.get('MIN_RETAZO_PERFIL_CM', MIN_RETAZO_PERFIL_CM),
        )
        return componentes, resultado, total

    @staticmethod
    def _mano_obra(resultado):
        minutos = round(sum(r['minutos'] for r in resultado), 2)
        costo_minuto = float(current_app.config.get('COSTO_MINUTO_MANO_OBRA', 0) or 0)
        return minutos, round(minutos * costo_minuto, 2)

    def explode(self, product_id, w, h):
        _, resultado, total = self._calcular(product_id, w, h)
        minutos, mano_obra = self._mano_obra(resultado)
        return ExplosionOut(
            explosion=[ExplosionItemOut(**r) for r in resultado],
            total_materiales=total,
            total_minutos=minutos,
            total_mano_obra=mano_obra,
            total=round(total + mano_obra, 2),
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

        cortes = [c for r in resultado for c in r['cortes']]
        piezas_ids = {c['id_pieza'] for c in cortes if c['id_pieza'] is not None}
        piezas = self.pieces.lock_remnants(piezas_ids)
        if piezas_ids - set(piezas):
            self.pieces.session.rollback()
            raise ConflictError("Un sobrante de perfil ya fue usado por otra producción. Recalculá la receta.")

        necesario = {}
        for item, r in zip(componentes, resultado):
            if r['metodo'] not in ('RETAZO', 'MANO_OBRA') and item.id_insumo:
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
        generados = self._aplicar_cortes_perfil(componentes, resultado, piezas)
        self.supplies.commit()

        minutos, mano_obra = self._mano_obra(resultado)
        return ProduccionOut(
            descontado=descontados,
            retazos_usados=sorted(retazos),
            retazos_perfil_generados=generados,
            total_materiales=total,
            total_minutos=minutos,
            total_mano_obra=mano_obra,
            total=round(total + mano_obra, 2),
        )

    def _aplicar_cortes_perfil(self, componentes, resultado, piezas):
        """Reproduce los cortes en orden: actualiza los sobrantes usados y guarda los nuevos."""
        por_token = {}
        generados = 0
        for item, r in zip(componentes, resultado):
            for corte in r['cortes']:
                origen = None
                if corte['origen'] == 'retazo':
                    origen = piezas.get(corte['id_pieza']) or por_token.get(corte['tok_origen'])
                if corte['reutilizable']:
                    if origen is not None:
                        origen.longitud_actual_cm = Decimal(str(corte['sobrante']))
                        por_token[corte['tok_sobrante']] = origen
                    else:
                        nueva = PiezaStock(
                            id_insumo=item.id_insumo,
                            longitud_original_cm=Decimal(str(corte['largo_origen'])),
                            longitud_actual_cm=Decimal(str(corte['sobrante'])),
                            es_retazo=True,
                        )
                        self.pieces.session.add(nueva)
                        por_token[corte['tok_sobrante']] = nueva
                        generados += 1
                elif origen is not None:
                    origen.longitud_actual_cm = Decimal(0)
        return generados
