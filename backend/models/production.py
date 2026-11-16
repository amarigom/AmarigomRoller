from extensions import db


class ProductionRecord(db.Model):
    __tablename__ = 'producciones'
    __table_args__ = (
        db.Index('ix_producciones_fecha', 'creado_en'),
        db.Index('ix_producciones_producto_fecha', 'producto_id', 'creado_en'),
    )

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    producto_nombre = db.Column(db.String(255), nullable=False)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'), nullable=False)
    receta_version = db.Column(db.Integer, nullable=False)
    ancho_cm = db.Column(db.Numeric(10, 2), nullable=False)
    alto_cm = db.Column(db.Numeric(10, 2), nullable=False)
    opciones = db.Column(db.JSON, nullable=False, default=dict)
    referencia = db.Column(db.String(255))
    total_materiales = db.Column(db.Numeric(14, 2), nullable=False)
    total_minutos = db.Column(db.Numeric(10, 2), nullable=False)
    total_mano_obra = db.Column(db.Numeric(14, 2), nullable=False)
    total_desgaste = db.Column(db.Numeric(14, 2), nullable=False, default=0, server_default='0')
    total = db.Column(db.Numeric(14, 2), nullable=False)
    detalle = db.Column(db.JSON, nullable=False, default=list)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    usuario_nombre = db.Column(db.String(100))
    creado_en = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())

    producto = db.relationship('Product')
    receta = db.relationship('Receta')
    usuario = db.relationship('User')
