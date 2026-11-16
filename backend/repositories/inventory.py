from decimal import Decimal

from sqlalchemy.orm import joinedload

from models import InventoryMovement, PiezaStock, RecetaItem, RetazoTela, Supply, SupplyPriceHistory
from repositories.base import BaseRepository


class InventoryRepository(BaseRepository):
    def movimientos(self, supply_id, limit=100):
        return (
            InventoryMovement.query.options(joinedload(InventoryMovement.usuario))
            .filter_by(id_insumo=supply_id)
            .order_by(InventoryMovement.creado_en.desc(), InventoryMovement.id.desc())
            .limit(min(max(limit, 1), 500))
            .all()
        )

    def historial_precios(self, supply_id):
        return (
            SupplyPriceHistory.query.options(joinedload(SupplyPriceHistory.usuario))
            .filter_by(id_insumo=supply_id)
            .order_by(SupplyPriceHistory.vigente_desde.desc(), SupplyPriceHistory.id.desc())
            .all()
        )

    def alertas_stock(self):
        return Supply.query.filter(
            Supply.activo.is_(True),
            Supply.stock_minimo > 0,
            Supply.stock_actual <= Supply.stock_minimo,
        ).order_by(Supply.name).all()

    def retazos_disponibles(self, limit=500):
        return (
            RetazoTela.query.options(joinedload(RetazoTela.insumo_base))
            .filter(RetazoTela.estado.in_(('disponible', 'reservado')))
            .order_by(RetazoTela.fecha_generado.desc(), RetazoTela.id.desc())
            .limit(min(max(limit, 1), 1000))
            .all()
        )

    def retazo_bloqueado(self, scrap_id):
        return RetazoTela.query.filter_by(id=scrap_id).with_for_update().first()

    def insumo_en_receta(self, supply_id):
        return any(
            supply_id in (item.insumos_alternativos or [])
            for item in RecetaItem.query.filter_by(tipo_calculo='perfil').all()
        ) or self.session.query(RecetaItem.id).filter_by(id_insumo=supply_id).first() is not None

    def es_perfil(self, supply_id):
        insumo = self.session.get(Supply, supply_id)
        categoria = insumo.category.name.lower() if insumo and insumo.category else ''
        return ('perfil' in categoria or 'tubo' in categoria or
                any(item.id_insumo == supply_id or supply_id in (item.insumos_alternativos or [])
                    for item in RecetaItem.query.filter_by(tipo_calculo='perfil').all()))

    def piezas_por_insumo(self, supply_id):
        return (PiezaStock.query.filter_by(id_insumo=supply_id).filter(PiezaStock.longitud_actual_cm > 0)
                .order_by(PiezaStock.id).populate_existing().with_for_update().all())

    def resumen_perfiles(self, supply_ids):
        piezas = PiezaStock.query.filter(PiezaStock.id_insumo.in_(supply_ids),
                                         PiezaStock.longitud_actual_cm > 0).all() if supply_ids else []
        perfiles = set()
        for item in RecetaItem.query.filter_by(tipo_calculo='perfil').all():
            perfiles.add(item.id_insumo)
            perfiles.update(item.insumos_alternativos or [])
        for insumo in Supply.query.filter(Supply.id.in_(supply_ids)).all():
            categoria = insumo.category.name.lower() if insumo.category else ''
            if 'perfil' in categoria or 'tubo' in categoria:
                perfiles.add(insumo.id)
        perfiles.update(p.id_insumo for p in piezas)
        resumen = {}
        for pieza in piezas:
            fila = resumen.setdefault(pieza.id_insumo, {'enteras': 0, 'retazos': 0, 'total_cm': Decimal(0)})
            fila['retazos' if pieza.es_retazo else 'enteras'] += 1
            fila['total_cm'] += Decimal(pieza.longitud_actual_cm)
        return perfiles, resumen

    def insumo_tiene_retazos_o_piezas(self, supply_id):
        return (
            self.session.query(RetazoTela.id).filter_by(id_insumo_base=supply_id).first() is not None
            or self.session.query(PiezaStock.id).filter_by(id_insumo=supply_id).first() is not None
        )

    def agregar_movimiento(self, movement):
        self.session.add(movement)

    def agregar_precio(self, price):
        self.session.add(price)
