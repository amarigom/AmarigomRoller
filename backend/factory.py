from flask import Flask
from flask_cors import CORS

import models  # noqa: F401  (registra los modelos para las migraciones)
from cli import register_cli
from config import Config
from extensions import db, migrate
from routes import register_blueprints
from routes.errors import register_error_handlers
from strategies.notifications import create_notifier


def create_app(config_overrides=None):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(Config)
    app.config.update(config_overrides or {})

    if not app.config.get('SECRET_KEY'):
        raise ValueError("ERROR CRÍTICO: La variable SECRET_KEY no está configurada.")
    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        raise ValueError("ERROR CRÍTICO: La variable DATABASE_URL no está configurada.")

    CORS(app, resources={r"/api/*": {
        "origins": app.config['CORS_ORIGINS'],
        "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept", "X-Requested-With"],
        "supports_credentials": True,
    }})

    db.init_app(app)
    migrate.init_app(app, db)
    app.extensions['notifier'] = create_notifier(app.config)

    register_blueprints(app)
    register_error_handlers(app)
    register_cli(app)

    # En una base nueva: AUTO_CREATE_TABLES=1 una sola vez y luego `flask db upgrade`.
    if app.config.get('AUTO_CREATE_TABLES'):
        with app.app_context():
            db.create_all()

    return app
