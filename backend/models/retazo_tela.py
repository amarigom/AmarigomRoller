from extensions import db


class RetazoTela(db.Model):
    __tablename__ = 'retazos_telas'
    __table_args__ = (
        db.Index('ix_retazos_telas_insumo_estado', 'id_insumo_base', 'estado'),
    )

    id = db.Column(db.Integer, primary_key=True)
    id_insumo_base = db.Column(db.Integer, db.ForeignKey('insumos.id'), nullable=False)
    ancho_cm = db.Column(db.Numeric(10, 2), nullable=False)
    largo_cm = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_generado = db.Column(db.DateTime, default=db.func.current_timestamp())
    estado = db.Column(db.String(20), default='disponible')
    referencia = db.Column(db.String(255))
    notas = db.Column(db.Text)

    insumo_base = db.relationship('Supply', backref='retazos')
