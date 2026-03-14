from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os

# Importaciones con el punto (.) para que Vercel las encuentre
from .config import Config      
from .models import db          
from .models.rollo import Rollo 
from .routes.inventory import inventory_bp

# 1. Inicializar la app y cargar config
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# 2. Conectar la DB modularizada
db.init_app(app) # <--- En lugar de db = SQLAlchemy(app)
app.db = db 

# Mantenemos tu lógica de Mail...
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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)