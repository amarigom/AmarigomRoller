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

    def category_exists(self, category_id):
        return self.session.get(SupplyCategory, category_id) is not None


class CategoryRepository(BaseRepository):
    model = SupplyCategory

    def list(self):
        return SupplyCategory.query.order_by(SupplyCategory.name).all()
