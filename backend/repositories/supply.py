from sqlalchemy.orm import joinedload

from models import Supply, SupplyCategory
from repositories.base import BaseRepository


class SupplyRepository(BaseRepository):
    model = Supply

    def list(self, limit=None, offset=0):
        query = Supply.query.options(joinedload(Supply.category)).order_by(Supply.id)
        return self.paginate(query, limit, offset).all()

    def get_with_category(self, supply_id):
        return (
            Supply.query.options(joinedload(Supply.category))
            .filter(Supply.id == supply_id)
            .first()
        )

    def lock_many(self, supply_ids):
        """Trae los insumos bloqueándolos hasta el commit (evita descuentos simultáneos pisados)."""
        if not supply_ids:
            return {}
        rows = Supply.query.filter(Supply.id.in_(supply_ids)).with_for_update().all()
        return {s.id: s for s in rows}

    def get_many(self, supply_ids):
        if not supply_ids:
            return []
        return Supply.query.filter(Supply.id.in_(list(supply_ids))).all()

    def category_exists(self, category_id):
        return self.session.get(SupplyCategory, category_id) is not None


class CategoryRepository(BaseRepository):
    model = SupplyCategory

    def list(self):
        return SupplyCategory.query.order_by(SupplyCategory.name).all()
