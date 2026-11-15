from extensions import db


class SavedQuote(db.Model):
    __tablename__ = 'presupuestos_guardados'
    __table_args__ = (db.Index('ix_presupuestos_guardados_fecha', 'creado_en'),)

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    producto_nombre = db.Column(db.String(255), nullable=False)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'), nullable=False)
    receta_version = db.Column(db.Integer, nullable=False)
    ancho_cm = db.Column(db.Float, nullable=False)
    alto_cm = db.Column(db.Float, nullable=False)
    referencia = db.Column(db.String(255))
    opciones = db.Column(db.JSON, nullable=False)
    resultado = db.Column(db.JSON, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    usuario_nombre = db.Column(db.String(100))
    creado_en = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
