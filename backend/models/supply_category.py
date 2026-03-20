from . import db

class SupplyCategory(db.Model):
    __tablename__ = 'categorias_insumos'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    # Relación con los insumos
    supplies = db.relationship('Supply', backref='category', lazy=True)