from . import db

class RecipeBOM(db.Model):
    __tablename__ = 'recetas_bom'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    id_padre = db.Column(db.Integer, db.ForeignKey('recetas_bom.id'), nullable=True)
    id_insumo = db.Column(db.Integer, db.ForeignKey('insumos.id'), nullable=True)
    
    # IMPORTANTE: Usamos nombre_producto porque así está en tu CREATE TABLE de Neon
    nombre_producto = db.Column(db.String(100), nullable=False)
    
    delta_ancho_cm = db.Column(db.Numeric(12, 2), default=0.00)
    delta_alto_cm = db.Column(db.Numeric(12, 2), default=0.00)
    tipo_calculo = db.Column(db.String(30), nullable=False)
    descripcion = db.Column(db.Text)
    
    # Si agregaste cantidad_base después, dejala. Si no, poné un valor fijo en el cálculo.
    cantidad_base = db.Column(db.Numeric(12, 4), default=1.0000)

    # Relación con insumos
    insumo = db.relationship('Supply', backref='recetas')

    def to_dict(self):
        return {
            "id": self.id,
            "id_padre": self.id_padre,
            "id_insumo": self.id_insumo,
            "nombre": self.nombre_producto, # Antes decía nombre_item
            "delta_ancho": float(self.delta_ancho_cm),
            "delta_alto": float(self.delta_alto_cm),
            "tipo_calculo": self.tipo_calculo,
            "stock_info": {
                "medida": self.insumo.unidad_medida if self.insumo else None,
                "precio_base": float(self.insumo.precio_costo_unitario) if self.insumo else 0
            }
        }