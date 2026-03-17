# backend/models/rollo.py
from . import db

class Rollo(db.Model):
    __tablename__ = 'rollos'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50))
    category = db.Column(db.String(50))
    width_cm = db.Column(db.Integer)
    price_per_meter = db.Column(db.Float)
    meters_left = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default="in_stock")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "category": self.category,
            "widthCm": self.width_cm,
            "pricePerMeter": self.price_per_meter,
            "metersLeft": self.meters_left,
            "status": self.status
        }