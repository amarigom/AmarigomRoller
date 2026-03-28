from flask import Blueprint, jsonify, request
from models import db, Cliente 

clients_bp = Blueprint('clients', __name__)


@clients_bp.route('/', methods=['GET'])
def get_clients():
    clientes = Cliente.query.all()
    # Usamos el método to_dict() que creamos en el modelo
    return jsonify([c.to_dict() for c in clientes]), 200

@clients_bp.route('/', methods=['POST'])
def create_client():
    data = request.json
    
    # 1. Validación básica (Responsabilidad del Backend)
    if not data.get('nombre') or not data.get('apellido'):
        return jsonify({"status": "error", "message": "Faltan datos obligatorios"}), 400
    
    try:
        # 2. Creamos la instancia del modelo que definimos antes
        nuevo_cliente = Cliente(
            nombre=data.get('nombre'),
            apellido=data.get('apellido'),
            telefono=data.get('telefono'),
            email=data.get('email'),
            direccion=data.get('direccion'),
            notas=data.get('notas')
        )
        
        db.session.add(nuevo_cliente)
        db.session.commit()
        
        return jsonify({"status": "success", "client": nuevo_cliente.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500