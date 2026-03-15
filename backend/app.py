# backend/app.py
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os

# 1. Importaciones de modelos con punto (.)
from models import db          
from models.rollo import Rollo 

app = Flask(__name__)

# --- HARD-FIX DE CONFIGURACIÓN ---
# Leemos directamente del entorno del SISTEMA, no del archivo .env ni de Config
uri = os.environ.get("DATABASE_URL")

if uri:
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
else:
    # Si falla, esto nos va a decir en el LOG exactamente qué está viendo Python
    print(f"DEBUG: Las variables de entorno actuales son: {list(os.environ.keys())}")
    # Solo como último recurso intenta Config
    from .config import Config
    app.config.from_object(Config)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "amarigom-secret-2026")
# ---------------------------------

CORS(app)

# 2. Conectar la DB
db.init_app(app)
app.db = db 

# ... (El resto de tus Blueprints con el punto adelante, ej: from .routes.main import main_bp)

# lógica de Mail...
if app.config.get('MAIL_ENABLED'):
    from flask_mail import Mail
    mail = Mail(app)
    app.mail = mail
else:
    app.mail = None

# 3. Importar y Registrar Blueprints
from routes.inventory import inventory_bp
from routes.main import main_bp
from routes.products import products_bp
from routes.quote import quote_bp
from routes.cart import cart_bp

app.register_blueprint(main_bp)
app.register_blueprint(inventory_bp, url_prefix='/api') 
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(quote_bp, url_prefix='/api/quote')
app.register_blueprint(cart_bp, url_prefix='/api/cart')

# Crear tablas automáticamente al arrancar
with app.app_context():
    db.create_all() # Ahora sí, detectará el modelo Rollo

@app.context_processor
def inject_language():
    return dict(lang=session.get('language', 'es'))
app = app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)