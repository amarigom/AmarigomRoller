from extensions import db


class Receta(db.Model):
    """Versión de la receta de un producto. Solo una está vigente en cada momento."""

    __tablename__ = 'recetas'
    __table_args__ = (
        db.UniqueConstraint('producto_id', 'version', name='uq_recetas_producto_version'),
        db.Index('ix_recetas_producto_vigencia', 'producto_id', 'vigente_desde'),
    )

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    version = db.Column(db.Integer, nullable=False)
    vigente_desde = db.Column(db.DateTime, nullable=False)
    vigente_hasta = db.Column(db.DateTime)
    nota = db.Column(db.String(255))
    creado_en = db.Column(db.DateTime, default=db.func.current_timestamp())

    producto = db.relationship('Product', backref='recetas')
    items = db.relationship(
        'RecetaItem', backref='receta', cascade='all, delete-orphan', order_by='RecetaItem.orden, RecetaItem.id')


class RecetaItem(db.Model):
    __tablename__ = 'receta_items'
    __table_args__ = (db.Index('ix_receta_items_receta', 'receta_id'),)

    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'), nullable=False)
    orden = db.Column(db.Integer, nullable=False, default=0)
    id_insumo = db.Column(db.Integer, db.ForeignKey('insumos.id'))
    nombre = db.Column(db.String(100), nullable=False)
    tipo_calculo = db.Column(db.String(30), nullable=False)
    descripcion = db.Column(db.Text)

    delta_ancho_cm = db.Column(db.Numeric(12, 2), default=0)
    delta_alto_cm = db.Column(db.Numeric(12, 2), default=0)
    cantidad_base = db.Column(db.Numeric(12, 4), default=1)
    merma_pct = db.Column(db.Numeric(5, 2), default=0)
    minutos_mano_obra = db.Column(db.Numeric(8, 2), default=0)

    # Fórmulas opcionales: reemplazan la medida de corte o la cantidad calculada con los deltas
    formula_ancho = db.Column(db.String(200))
    formula_alto = db.Column(db.String(200))
    formula_cantidad = db.Column(db.String(200))
    # Si se carga y da falso, el componente no entra (ej: "ancho > 200", "sistema == 'motor'")
    condicion = db.Column(db.String(200))

    insumo = db.relationship('Supply')

    @property
    def nombre_producto(self):
        return self.nombre
