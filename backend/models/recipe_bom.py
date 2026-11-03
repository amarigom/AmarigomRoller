from extensions import db


class RecipeBOM(db.Model):
    __tablename__ = 'recetas_bom'
    __table_args__ = (
        db.Index('ix_recetas_bom_id_padre', 'id_padre'),
        {'extend_existing': True},
    )

    id = db.Column(db.Integer, primary_key=True)
    id_padre = db.Column(db.Integer, db.ForeignKey('recetas_bom.id'), nullable=True)
    id_insumo = db.Column(db.Integer, db.ForeignKey('insumos.id'), nullable=True)

    nombre_producto = db.Column(db.String(100), nullable=False)
    delta_ancho_cm = db.Column(db.Numeric(12, 2), default=0.00)
    delta_alto_cm = db.Column(db.Numeric(12, 2), default=0.00)
    tipo_calculo = db.Column(db.String(30), nullable=False)
    descripcion = db.Column(db.Text)
    cantidad_base = db.Column(db.Numeric(12, 4), default=1.0000)
    merma_pct = db.Column(db.Numeric(5, 2), default=0)
    minutos_mano_obra = db.Column(db.Numeric(8, 2), default=0)

    insumo = db.relationship('Supply', backref='recetas')
