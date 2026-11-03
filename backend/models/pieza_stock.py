from extensions import db


class PiezaStock(db.Model):
    """Pieza física de un perfil o caño. Los sobrantes reutilizables se guardan con es_retazo=True."""

    __tablename__ = 'stock_piezas_detalle'
    __table_args__ = (
        db.Index('ix_stock_piezas_insumo_retazo', 'id_insumo', 'es_retazo'),
        {'extend_existing': True},
    )

    id = db.Column(db.Integer, primary_key=True)
    id_insumo = db.Column(db.Integer, db.ForeignKey('insumos.id'), nullable=False)
    longitud_original_cm = db.Column(db.Numeric(10, 2), nullable=False)
    longitud_actual_cm = db.Column(db.Numeric(10, 2), nullable=False)
    es_retazo = db.Column(db.Boolean, nullable=False, default=False)
    fecha_ingreso = db.Column(db.DateTime, default=db.func.current_timestamp())
