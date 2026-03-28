from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from database import db 
# 2. IMPORTAMOS LOS BLUEPRINTS (ahora no habrá círculo porque db nace aparte)
from routes.inventory import inventory_bp
from routes.main import main_bp
from routes.products import products_bp
from routes.recipes import recipes_bp
from routes.clients import clients_bp
import os
# --- NUEVAS LÍNEAS PARA LEER EL .ENV ---
from dotenv import load_dotenv

# Esto carga las variables del archivo .env a la memoria
load_dotenv() 
# ---------------------------------------

app = Flask(__name__)

# --- CONFIGURACIÓN DE DB ---
# Ahora os.environ.get sí podrá encontrar la variable
uri = os.environ.get("DATABASE_URL")

if not uri:
    # Si falla, imprimimos dónde está parado el sistema para debuguear
    print(f"Directorio actual: {os.getcwd()}")
    raise ValueError("ERROR CRÍTICO: La variable DATABASE_URL no está configurada.")

# Corrección obligatoria para SQLAlchemy (Neon usa postgres://)
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "amarigom-secret-2026")



CORS(app, resources={r"/api/*": {"origins": "*"}})

db.init_app(app)

app.register_blueprint(main_bp)
app.register_blueprint(inventory_bp, url_prefix='/api')
app.register_blueprint(recipes_bp, url_prefix='/api')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(clients_bp, url_prefix='/api/clients')

with app.app_context():
    db.create_all()

app = app

if __name__ == '__main__':
    app.run()