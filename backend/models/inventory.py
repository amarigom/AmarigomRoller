from extensions import db


class InventoryMovement(db.Model):
    __tablename__ = 'inventario_movimientos'
    __table_args__ = (
        db.Index('ix_inventario_movimientos_insumo_fecha', 'id_insumo', 'creado_en'),
    )

    id = db.Column(db.Integer, primary_key=True)
    id_insumo = db.Column(db.Integer, db.ForeignKey('insumos.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    cantidad = db.Column(db.Numeric(14, 4), nullable=False)
    stock_resultante = db.Column(db.Numeric(14, 4), nullable=False)
    referencia = db.Column(db.String(255))
    notas = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    creado_en = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())

    insumo = db.relationship('Supply')
    usuario = db.relationship('User', foreign_keys=[usuario_id])


class SupplyPriceHistory(db.Model):
    __tablename__ = 'historial_precios_insumos'
    __table_args__ = (
        db.Index('ix_historial_precios_insumo_fecha', 'id_insumo', 'vigente_desde'),
    )

    id = db.Column(db.Integer, primary_key=True)
    id_insumo = db.Column(db.Integer, db.ForeignKey('insumos.id'), nullable=False)
    precio = db.Column(db.Numeric(12, 4), nullable=False)
    vigente_desde = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    motivo = db.Column(db.String(255))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    insumo = db.relationship('Supply')
    usuario = db.relationship('User', foreign_keys=[usuario_id])
