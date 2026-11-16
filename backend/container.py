"""Composición de dependencias: arma los servicios con su configuración. Se crean por pedido (son livianos)."""
from flask import current_app

from repositories.user import UserRepository
from security.tokens import TokenService
from services.auth import AuthService
from services.clients import ClientService
from services.inventory import InventoryService
from services.products import ProductService
from services.quote import QuoteService
from services.recipes import RecipeService
from services.users import UserService


def auth_service():
    cfg = current_app.config
    return AuthService(
        UserRepository(),
        TokenService(cfg['SECRET_KEY'], cfg['JWT_EXPIRES_MINUTES']),
        cfg['LOGIN_MAX_ATTEMPTS'],
        cfg['LOGIN_LOCK_MINUTES'],
    )


def user_service():
    return UserService()


def inventory_service():
    return InventoryService()


def client_service():
    return ClientService()


def recipe_service():
    return RecipeService()


def product_service():
    return ProductService()


def quote_service():
    return QuoteService(current_app.extensions['notifier'], current_app.config['QUOTE_RECIPIENT'])
