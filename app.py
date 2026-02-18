from flask import Flask, render_template, request, jsonify, session
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

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
    app.run(debug=True, host='0.0.0.0', port=5000)
