from exceptions import ConflictError, NotFoundError
from models import Supply
from repositories.supply import CategoryRepository, SupplyRepository
from schemas.inventory import CategoryOut, SupplyOut


class InventoryService:
    def __init__(self, supplies=None, categories=None):
        self.supplies = supplies or SupplyRepository()
        self.categories = categories or CategoryRepository()

    def list_supplies(self, limit=None, offset=0):
        return [SupplyOut.from_model(s) for s in self.supplies.list(limit, offset)]

    def create_supply(self, datos):
        if not self.supplies.category_exists(datos.categoria_id):
            raise NotFoundError("La categoría indicada no existe")
        insumo = self.supplies.add(Supply(**datos.model_dump()))
        try:
            self.supplies.commit()
        except ConflictError as e:
            raise ConflictError("El código SKU ya existe") from e
        return SupplyOut.from_model(self.supplies.get_with_category(insumo.id))

    def delete_supply(self, supply_id):
        insumo = self.supplies.get(supply_id)
        if insumo is None:
            raise NotFoundError("Insumo no encontrado")
        self.supplies.delete(insumo)
        try:
            self.supplies.commit()
        except ConflictError as e:
            raise ConflictError("No se puede eliminar: el insumo se usa en recetas o retazos") from e

    def list_categories(self):
        return [CategoryOut.from_model(c) for c in self.categories.list()]
