from extensions import db


class Product(db.Model):
    __tablename__ = 'productos'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    categoria = db.Column(db.String(100))
    activo = db.Column(db.Boolean, default=True)
