from sqlalchemy.orm import joinedload

from models import RecipeBOM, RetazoTela
from repositories.base import BaseRepository


class RecipeRepository(BaseRepository):
    model = RecipeBOM

    def components_for_product(self, product_id):
        return (
            RecipeBOM.query
            .options(joinedload(RecipeBOM.insumo))
            .filter_by(id_padre=product_id)
            .order_by(RecipeBOM.id)
            .all()
        )


class ScrapRepository(BaseRepository):
    model = RetazoTela

    def available_by_supply(self, supply_ids):
        """Retazos disponibles agrupados por insumo, en una sola consulta."""
        if not supply_ids:
            return {}
        rows = RetazoTela.query.filter(
            RetazoTela.id_insumo_base.in_(supply_ids),
            RetazoTela.estado == 'disponible',
        ).all()
        agrupados = {}
        for r in rows:
            agrupados.setdefault(r.id_insumo_base, []).append(r)
        return agrupados

    def lock_available(self, scrap_ids):
        """Retazos aún disponibles, bloqueados hasta el commit."""
        if not scrap_ids:
            return {}
        rows = RetazoTela.query.filter(
            RetazoTela.id.in_(scrap_ids), RetazoTela.estado == 'disponible'
        ).with_for_update().all()
        return {r.id: r for r in rows}
