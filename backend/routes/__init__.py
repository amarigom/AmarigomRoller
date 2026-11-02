"""Capa HTTP: solo traduce requests/responses y delega en los servicios."""
from routes.auth import auth_bp
from routes.clients import clients_bp
from routes.inventory import inventory_bp
from routes.main import main_bp
from routes.products import products_bp
from routes.recipes import recipes_bp
from routes.users import users_bp


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(inventory_bp, url_prefix='/api')
    app.register_blueprint(recipes_bp, url_prefix='/api')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(clients_bp, url_prefix='/api/clients')
