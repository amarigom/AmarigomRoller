import re
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db
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
    raise ValueError("ERROR CRÍTICO: La variable DATABASE_URL no está configurada.")

if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "amarigom-secret-2026")

# --- CONFIGURACIÓN DE CORS ---
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://amarigom-roller-frontend1.vercel.app", 
            "http://localhost:3000",
            "https://amarigom-roller.vercel.app"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept", "X-Requested-With"],
        "supports_credentials": True
    }
})

@app.after_request
def add_cors_headers(response):
    origin = request.headers.get('Origin')
    if origin and (".vercel.app" in origin or "localhost" in origin):
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# --- INICIALIZACIÓN ---
db.init_app(app)

# --- REGISTRO DE BLUEPRINTS ---
# Aseguramos que todas las rutas de negocio cuelguen de /api
app.register_blueprint(main_bp)
app.register_blueprint(inventory_bp, url_prefix='/api')
app.register_blueprint(recipes_bp, url_prefix='/api')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(clients_bp, url_prefix='/api/clients')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()