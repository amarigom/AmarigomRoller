import os
from datetime import timedelta

class Config:
    """Configuración de la aplicación Flask"""
    
    # Clave secreta para sesiones (cambiar en producción)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configuración de Flask-Mail para envío de cotizaciones
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT',587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'amarigomdeco@gmail.com'
    
    MAIL_ENABLED = bool(MAIL_SERVER and MAIL_USERNAME and MAIL_PASSWORD)
    
    # Configuración de sesión
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Configuración de uploads (si necesitas subir imágenes)
    UPLOAD_FOLDER = 'static/images/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Información de contacto
    CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL') or 'contacto@amarigom.com'
    WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER') or '+5492494630750'
    INSTAGRAM_URL = os.environ.get('INSTAGRAM_URL') or 'https://instagram.com/amarigom'
