from extensions import db
from .supply_category import SupplyCategory
from .supply import Supply
from .recipe_bom import RecipeBOM
from .retazo_tela import RetazoTela
from .product import Product
from .client import Cliente
from .user import User, Role

__all__ = [
    'db', 'Supply', 'SupplyCategory', 'RecipeBOM', 'RetazoTela',
    'Product', 'Cliente', 'User', 'Role',
]
