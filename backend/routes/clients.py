from flask import Blueprint, jsonify, request
from models import db, Cliente 

# Creamos el Blueprint normal
clients_bp = Blueprint('clients', __name__)

# --- GET: OBTENER CLIENTES ---
@clients_bp.route('/', methods=['GET', 'OPTIONS'], strict_slashes=False)
def get_clients():
    if request.method == 'OPTIONS':
        return '', 204
    
    clientes = Cliente.query.all()
    return jsonify([c.to_dict() for c in clientes]), 200

# --- POST: CREAR CLIENTE ---
@clients_bp.route('/', methods=['POST', 'OPTIONS'], strict_slashes=False)
def create_client():
    # 1. Manejo del Preflight (La pregunta de seguridad del navegador)
    if request.method == 'OPTIONS':
        return '', 204

    data = request.json
    
    # 2. Validación: Agregamos el email como obligatorio ya que Neon lo pide
    if not data or not data.get('nombre') or not data.get('apellido') or not data.get('email'):
        return jsonify({
            "status": "error", 
            "message": "Faltan datos obligatorios (Nombre, Apellido y Email)"
        }), 400
    
    try:
        # 3. Creamos la instancia para Neon
        nuevo_cliente = Cliente(
            nombre=data.get('nombre').strip(),
            apellido=data.get('apellido').strip(),
            telefono=data.get('telefono'),
            email=data.get('email').strip(),
            direccion=data.get('direccion'),
            notas=data.get('notas')
        )
        
        db.session.add(nuevo_cliente)
        db.session.commit()
        
        return jsonify({
            "status": "success", 
            "message": "Cliente guardado con éxito",
            "client": nuevo_cliente.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        # Si el error es por email duplicado, mandamos un mensaje claro
        error_str = str(e)
        if "unique constraint" in error_str.lower():
            return jsonify({
                "status": "error", 
                "message": "Este email ya está registrado"
            }), 409
            
        return jsonify({"status": "error", "message": error_str}), 500