from extensions import db


class PriceSyncState(db.Model):
    __tablename__ = 'sincronizacion_precios'

    id = db.Column(db.Integer, primary_key=True)
    ultimo_intento = db.Column(db.DateTime)
    ultima_exitosa = db.Column(db.DateTime)
    error = db.Column(db.Text)
    actualizados = db.Column(db.Integer)
    omitidos = db.Column(db.Integer)
