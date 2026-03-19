from . import db
from datetime import datetime

class CategoriaInsumo(db.Model):
    __tablename__ = 'categorias_insumos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    # Esta línea es la que permite que Insumo use .categoria
    insumos = db.relationship('Insumo', backref='categoria', lazy=True)
    
class Insumo(db.Model):
    __tablename__ = 'insumos'
    
    id = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias_insumos.id'), nullable=False)
    codigo_sku = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    unidad_medida = db.Column(db.String(20), nullable=False)
    
    # Coincide con lo que acabamos de renombrar en SQL
    precio_costo_unitario = db.Column(db.Numeric(12, 4), default=0.0000)
    stock_actual = db.Column(db.Numeric(12, 4), default=0.0000)
    stock_minimo = db.Column(db.Numeric(12, 4), default=0.0000)
    ancho_cm = db.Column(db.Numeric(10, 2), default=0.00)
    
    ultima_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.codigo_sku,
            "name": self.nombre,
            "category": self.categoria.nombre if self.categoria else "General",
            "metersLeft": float(self.stock_actual or 0),
            "widthCm": float(self.ancho_cm or 0),
            "unit": self.unidad_medida,
            "price": float(self.precio_costo_unitario or 0),
            "lastUpdate": self.ultima_actualizacion.strftime('%Y-%m-%d %H:%M') if self.ultima_actualizacion else None
        }