from models import db

class Product(db.Model):
    __tablename__ = 'productos' # O 'modelos_cortinas' según tu DB en Neon
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)

    # Relación con la receta (BOM) para saber qué insumos lleva
    receta = db.relationship('RecipeBOM', backref='producto_padre', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name_es": self.nombre, # Lo mapeamos a 'name_es' para que React no llore
            "description": self.descripcion
        }