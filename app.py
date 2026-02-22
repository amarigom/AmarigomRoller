from flask import Flask, render_template, request, jsonify, session
from config import Config
from flask_cors import CORS
import os

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

if app.config['MAIL_ENABLED']:
    from flask_mail import Mail
    mail = Mail(app)
    app.mail = mail
else:
    app.mail = None
    print("⚠️  AVISO: Email no configurado. Las cotizaciones se guardarán pero no se enviarán por email.")

# Importar blueprints (rutas modulares)
from routes.main import main_bp
from routes.products import products_bp
from routes.quote import quote_bp
from routes.cart import cart_bp

# Registrar blueprints
app.register_blueprint(main_bp)
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(quote_bp, url_prefix='/quote')
app.register_blueprint(cart_bp, url_prefix='/cart')

# Contexto global para templates (idioma)
@app.context_processor
def inject_language():
    return dict(lang=session.get('language', 'es'))



if __name__ == '__main__':
    # Intentamos leer el puerto que nos da Render, si no existe, usamos el 5000
    port = int(os.environ.get("PORT", 5000))
    # En producción (Render) el debug debe ser False por seguridad
    app.run(host='0.0.0.0', port=port, debug=False)
