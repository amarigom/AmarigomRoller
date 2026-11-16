from exceptions import NotFoundError
from repositories.product import ProductRepository
from schemas.products import ProductOut


class ProductService:
    def __init__(self, products=None):
        self.products = products or ProductRepository()

    def list_active(self):
        return [ProductOut.from_model(p) for p in self.products.list_active()]

    def list_promos(self):
        return [ProductOut.from_model(p) for p in self.products.list_promos()]

    def get(self, product_id):
        producto = self.products.get(product_id)
        if producto is None:
            raise NotFoundError("Producto no encontrado")
        return ProductOut.from_model(producto)
