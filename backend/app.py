import re
import os
from flask import Flask
from flask_cors import CORS
from models import db
# Asegurate de que estas importaciones coincidan con tus nombres de archivos
from routes.main import main_bp
from routes.inventory import inventory_bp
from routes.recipes import recipes_bp
from routes.products import products_bp
from routes.clients import clients_bp
from dotenv import load_dotenv
load_dotenv() 

app = Flask(__name__)
app.url_map.strict_slashes = False
# --- CONFIGURACIÓN DE BASE DE DATOS ---
uri = os.environ.get("DATABASE_URL")

if not uri:
    # Si falla, imprimimos dónde está parado el sistema para debuguear
    print(f"Directorio actual: {os.getcwd()}")
    raise ValueError("ERROR CRÍTICO: La variable DATABASE_URL no está configurada.")


if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "amarigom-secret-2026")


# --- CONFIGURACIÓN DE CORS (EL PORTERO) ---
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000",re.compile(r"https://.*\.vercel\.app$")],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"],
        "supports_credentials": True,
        "expose_headers": ["Content-Type", "Authorization"]
    }
})

# Inicializamos la DB
db.init_app(app)

# --- REGISTRO DE BLUEPRINTS ---
# IMPORTANTE: Cambiamos el prefix de clientes para que no choque con la barra final
app.register_blueprint(main_bp)
app.register_blueprint(inventory_bp, url_prefix='/api')
app.register_blueprint(recipes_bp, url_prefix='/api')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(clients_bp, url_prefix='/api/clients')

# Creamos las tablas en Neon si no existen
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Usamos 127.0.0.1 para que coincida con tu prueba de PowerShell
    app.run(host='127.0.0.1', port=5000, debug=True)