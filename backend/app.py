from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from models import db
# Importamos los blueprints (asegurate que las rutas existan)
from routes.inventory import inventory_bp
from routes.main import main_bp
import os

app = Flask(__name__)

# --- CONFIGURACIÓN DE DB SEGURA ---
uri = os.environ.get("DATABASE_URL")
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "amarigom-secret-2026")

# Habilitar CORS para el Frontend
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Inicializar DB
db.init_app(app)

# Registrar Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(inventory_bp, url_prefix='/api')

# Crear tablas (Cuidado: esto puede tardar en Serverless, pero está bien para QA)
with app.app_context():
    db.create_all()

# Necesario para Vercel
app = app

if __name__ == '__main__':
    app.run()