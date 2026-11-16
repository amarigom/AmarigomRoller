import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

DEFAULT_CORS_ORIGINS = [
    "https://amarigom-roller-frontend1.vercel.app",
    "https://amarigom-roller.vercel.app",
    "http://localhost:3000",
]


def _database_uri():
    uri = os.environ.get('DATABASE_URL')
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    return uri


def _cors_origins():
    raw = os.environ.get('CORS_ORIGINS')
    if not raw:
        return DEFAULT_CORS_ORIGINS
    return [o.strip() for o in raw.split(',') if o.strip()]


class Config:
    """Configuración de la aplicación Flask (se lee del entorno)."""

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGINS = _cors_origins()

    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # Autenticación
    JWT_EXPIRES_MINUTES = int(os.environ.get('JWT_EXPIRES_MINUTES', 480))
    LOGIN_MAX_ATTEMPTS = int(os.environ.get('LOGIN_MAX_ATTEMPTS', 5))
    LOGIN_LOCK_MINUTES = int(os.environ.get('LOGIN_LOCK_MINUTES', 15))

    # Notificaciones (cotizaciones). Sin RESEND_API_KEY solo se registran en el log.
    RESEND_API_KEY = os.environ.get('RESEND_API_KEY')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'onboarding@resend.dev')
    QUOTE_RECIPIENT = os.environ.get('QUOTE_RECIPIENT') or os.environ.get('MAIL_USERNAME')

    # Información de contacto
    CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL') or 'contacto@amarigom.com'
    WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER') or '+5492494630750'
    INSTAGRAM_URL = os.environ.get('INSTAGRAM_URL') or 'https://instagram.com/amarigom'

    # Base nueva: AUTO_CREATE_TABLES=1 una sola vez y luego `flask db upgrade`
    AUTO_CREATE_TABLES = os.environ.get('AUTO_CREATE_TABLES') == '1'

    # Producción: sobrante mínimo de un perfil para guardarlo como retazo y costo de la mano de obra
    MIN_RETAZO_PERFIL_CM = float(os.environ.get('MIN_RETAZO_PERFIL_CM', 95))
    MIN_RETAZO_TELA_CM = float(os.environ.get('MIN_RETAZO_TELA_CM', 80))
    COSTO_MINUTO_MANO_OBRA = float(os.environ.get('COSTO_MINUTO_MANO_OBRA', 133))
    COSTO_DESGASTE_MAQUINARIA = os.environ.get('COSTO_DESGASTE_MAQUINARIA', '2000')
    TARIFA_BASE_COLOCACION = os.environ.get('TARIFA_BASE_COLOCACION', '8000')
    COSTO_POR_KM = os.environ.get('COSTO_POR_KM', '450')

    GOOGLE_SHEETS_ID = os.environ.get('GOOGLE_SHEETS_ID')
    GOOGLE_SHEETS_TAB = os.environ.get('GOOGLE_SHEETS_TAB', 'PRODUCTOS_INVENTARIO')
    GOOGLE_SHEETS_CREDENTIALS_JSON = os.environ.get('GOOGLE_SHEETS_CREDENTIALS_JSON')
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
