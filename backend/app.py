from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from models import db
from routes.inventory import inventory_bp
from routes.main import main_bp
import os

app = Flask(__name__)

# --- CONFIGURACIÓN DE DB ---
uri = os.environ.get("DATABASE_URL")

if not uri:
    # Esto detendrá el programa con un mensaje claro si olvidas setear la variable
    raise ValueError("ERROR CRÍTICO: La variable DATABASE_URL no está configurada.")

# Corrección obligatoria para SQLAlchemy
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "amarigom-secret-2026")

CORS(app, resources={r"/api/*": {"origins": "*"}})

db.init_app(app)

app.register_blueprint(main_bp)
app.register_blueprint(inventory_bp, url_prefix='/api')

with app.app_context():
    db.create_all()

app = app

if __name__ == '__main__':
    app.run()