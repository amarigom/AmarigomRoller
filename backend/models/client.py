from extensions import db


class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)
    direccion = db.Column(db.String(200))
    ciudad = db.Column(db.String(100), default="Tandil")
    notas = db.Column(db.Text)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())
