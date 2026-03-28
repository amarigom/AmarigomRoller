from database import db
class RetazoTela(db.Model):
        __tablename__ = 'retazos_telas'
        id = db.Column(db.Integer, primary_key=True)
        id_insumo_base = db.Column(db.Integer, db.ForeignKey('insumos.id'), nullable=False)
        ancho_cm = db.Column(db.Numeric(10, 2), nullable=False)
        largo_cm = db.Column(db.Numeric(10, 2), nullable=False)
        fecha_generado = db.Column(db.DateTime, default=db.func.current_timestamp())
        estado = db.Column(db.String(20), default='disponible')
        notas = db.Column(db.Text)
        # Relación opcional para ver qué tela es el retazo
        insumo_base = db.relationship('Supply', backref='retazos')