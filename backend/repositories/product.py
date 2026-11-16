from models import Product
from repositories.base import BaseRepository


class ProductRepository(BaseRepository):
    model = Product

    def list_active(self):
        return Product.query.filter_by(activo=True).all()

    def list_promos(self):
        return Product.query.filter_by(categoria='promo', activo=True).all()
