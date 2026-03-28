from database import db
class Product(db.Model):
    __tablename__ = 'productos'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    # AGREGÁ ESTA LÍNEA si la tenés en la DB, o usá una relación si es otra tabla
    categoria = db.Column(db.String(100)) 
    activo = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.nombre, # Cambiamos 'name_es' a 'name' para unificar con Vercel
            "category": self.categoria or "General", # <--- ESTO ES LO QUE FALTA
            "description": self.descripcion
        }
    # En product.py
