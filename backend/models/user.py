import enum

from extensions import db
from utils.clock import utcnow


class Role(str, enum.Enum):
    ADMIN = 'admin'
    VENTAS = 'ventas'
    TALLER = 'taller'


class User(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    nombre = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default=Role.VENTAS.value)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    intentos_fallidos = db.Column(db.Integer, nullable=False, default=0)
    bloqueado_hasta = db.Column(db.DateTime)
    ultimo_login = db.Column(db.DateTime)
    creado_en = db.Column(db.DateTime, nullable=False, default=utcnow)
