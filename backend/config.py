import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()
class Config:
    """Configuración de la aplicación Flask"""
    
    # Clave secreta para sesiones (cambiar en producción)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configuración de Flask-Mail para envío de cotizaciones
    MAIL_SERVER ='smtp.gmail.com'
    #os.environ.get('MAIL_SERVER')
    MAIL_PORT =587
    #int(os.environ.get('MAIL_PORT',587))
    MAIL_USE_TLS =True
    #os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME ='amarigomdeco@gmail.com'
    #os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD ='odfxdjynvjoroaho'
    #os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER ='amarigomdeco@gmail.com'
    #os.environ.get('MAIL_DEFAULT_SENDER') or 'amarigomdeco@gmail.com'
        
    # Configuración de sesión
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Configuración de uploads (para subir imágenes)
    UPLOAD_FOLDER = 'static/images/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Información de contacto
    CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL') or 'contacto@amarigom.com'
    WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER') or '+5492494630750'
    INSTAGRAM_URL = os.environ.get('INSTAGRAM_URL') or 'https://instagram.com/amarigom'


    
    # PostgreSQL:
    uri = os.environ.get('DATABASE_URL')
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_ENABLED = os.environ.get('MAIL_ENABLED') == 'True'