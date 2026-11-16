from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import joinedload

from models import PiezaStock, ProductionRecord, Product, Receta, RecetaItem, RetazoTela
from repositories.base import BaseRepository


def ahora():
    """Hora UTC sin zona, como se guardan las vigencias."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class RecipeRepository(BaseRepository):
    model = Receta

    def _con_items(self):
        return Receta.query.options(joinedload(Receta.items).joinedload(RecetaItem.insumo))

    def vigente(self, product_id, momento=None):
        """Versión de la receta vigente en `momento` (por defecto, ahora)."""
        momento = momento or ahora()
        return (
            self._con_items()
            .filter(
                Receta.producto_id == product_id,
                Receta.vigente_desde <= momento,
                (Receta.vigente_hasta.is_(None)) | (Receta.vigente_hasta > momento),
            )
            .order_by(Receta.version.desc())
            .first()
        )

    def por_version(self, product_id, version):
        return self._con_items().filter_by(producto_id=product_id, version=version).first()

    def por_id(self, recipe_id):
        return self._con_items().filter_by(id=recipe_id).first()

    def versiones(self, product_id):
        return Receta.query.filter_by(producto_id=product_id).order_by(Receta.version.desc()).all()

    def ultima_version(self, product_id):
        return self.session.query(func.max(Receta.version)).filter(Receta.producto_id == product_id).scalar() or 0

    def vigentes(self):
        """Versión vigente de cada producto (una consulta, con sus ítems)."""
        momento = ahora()
        return (
            Receta.query.options(joinedload(Receta.items))
            .filter(Receta.vigente_desde <= momento,
                    (Receta.vigente_hasta.is_(None)) | (Receta.vigente_hasta > momento))
            .order_by(Receta.version.desc())
            .all()
        )

    def productos(self):
        return Product.query.order_by(Product.nombre).all()

    def producto_por_nombre(self, nombre):
        return Product.query.filter(func.lower(Product.nombre) == nombre.strip().lower()).first()

    def historial_producciones(self, product_id=None, referencia=None, limit=100, offset=0):
        query = ProductionRecord.query
        if product_id is not None:
            query = query.filter(ProductionRecord.producto_id == product_id)
        if referencia:
            query = query.filter(ProductionRecord.referencia.ilike(f'%{referencia}%'))
        return (
            query.order_by(ProductionRecord.creado_en.desc(), ProductionRecord.id.desc())
            .limit(min(max(limit, 1), 500))
            .offset(max(offset, 0))
            .all()
        )


class ScrapRepository(BaseRepository):
    model = RetazoTela

    def available_by_supply(self, supply_ids, referencia=None):
        """Retazos disponibles agrupados por insumo, en una sola consulta."""
        if not supply_ids:
            return {}
        query = RetazoTela.query.filter(RetazoTela.id_insumo_base.in_(supply_ids))
        if referencia:
            query = query.filter(
                (RetazoTela.estado == 'disponible')
                | ((RetazoTela.estado == 'reservado') & (RetazoTela.referencia == referencia))
            )
        else:
            query = query.filter(RetazoTela.estado == 'disponible')
        rows = query.all()
        agrupados = {}
        for r in rows:
            agrupados.setdefault(r.id_insumo_base, []).append(r)
        return agrupados

    def lock_available(self, scrap_ids, referencia=None):
        """Retazos aún disponibles, bloqueados hasta el commit."""
        if not scrap_ids:
            return {}
        query = RetazoTela.query.filter(RetazoTela.id.in_(scrap_ids))
        if referencia:
            query = query.filter(
                (RetazoTela.estado == 'disponible')
                | ((RetazoTela.estado == 'reservado') & (RetazoTela.referencia == referencia))
            )
        else:
            query = query.filter(RetazoTela.estado == 'disponible')
        rows = query.with_for_update().all()
        return {r.id: r for r in rows}


class PieceRepository(BaseRepository):
    model = PiezaStock

    def lock_by_supply(self, supply_ids):
        if not supply_ids:
            return []
        return (PiezaStock.query.filter(PiezaStock.id_insumo.in_(supply_ids),
                                       PiezaStock.longitud_actual_cm > 0)
                .order_by(PiezaStock.id_insumo, PiezaStock.id).populate_existing().with_for_update().all())

    def remnants_by_supply(self, supply_ids):
        """Sobrantes de perfil aún utilizables, agrupados por insumo."""
        if not supply_ids:
            return {}
        rows = PiezaStock.query.filter(
            PiezaStock.id_insumo.in_(supply_ids),
            PiezaStock.es_retazo.is_(True),
            PiezaStock.longitud_actual_cm > 0,
        ).order_by(PiezaStock.id).all()
        agrupados = {}
        for r in rows:
            agrupados.setdefault(r.id_insumo, []).append(r)
        return agrupados

    def lock_remnants(self, piece_ids):
        if not piece_ids:
            return {}
        rows = PiezaStock.query.filter(
            PiezaStock.id.in_(piece_ids),
            PiezaStock.es_retazo.is_(True),
            PiezaStock.longitud_actual_cm > 0,
        ).populate_existing().with_for_update().all()
        return {r.id: r for r in rows}
