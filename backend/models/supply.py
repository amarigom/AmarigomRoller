from extensions import db


class Supply(db.Model):
    __tablename__ = 'insumos'
    __table_args__ = (
        db.Index('ix_insumos_categoria_id', 'categoria_id'),
        {'extend_existing': True},
    )

    id = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias_insumos.id'), nullable=False)

    codigo_sku = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(255), nullable=False)
    unidad_medida = db.Column(db.String(20))
    precio_costo_unitario = db.Column(db.Numeric(12, 4))
    stock_actual = db.Column(db.Numeric(12, 4))
    ancho_cm = db.Column(db.Numeric(10, 2))
    # Largo de la pieza que se compra (perfil de 200/400/600 cm, rollo de cinta de 5000 cm)
    largo_pieza_cm = db.Column(db.Numeric(10, 2))
