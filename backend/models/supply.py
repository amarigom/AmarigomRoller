from . import db

class Supply(db.Model):
    __tablename__ = 'insumos'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias_insumos.id'), nullable=False)
    
    codigo_sku = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(255), nullable=False)
    unidad_medida = db.Column(db.String(20))
    precio_costo_unitario = db.Column(db.Numeric(12, 4))
    stock_actual = db.Column(db.Numeric(12, 4))
    ancho_cm = db.Column(db.Numeric(10, 2))
    
    def to_dict(self):
        return {
            "id": self.id,
            "code": self.codigo_sku,
            "name": self.name,
            # Esto busca el nombre de la categoría automáticamente
            "category": self.category.name if self.category else "Sin Categoría",
            "metersLeft": float(self.stock_actual or 0),
            "widthCm": float(self.ancho_cm or 0),
            "unit": self.unidad_medida,
            "price": float(self.precio_costo_unitario or 0),
            "totalMeters": float(self.stock_actual or 0)
        }