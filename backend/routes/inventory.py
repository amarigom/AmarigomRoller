from flask import Blueprint, request, jsonify
from uuid import uuid4
from models import db, Rollo  

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/inventory', methods=['GET'])
def get_inventory():
    try:
        # SELECT * FROM rollos;
        rollos = Rollo.query.all()
        return jsonify([r.to_dict() for r in rollos])
    except Exception as e:
        return jsonify({"error": f"Error al obtener inventario: {str(e)}"}), 500

@inventory_bp.route('/inventory', methods=['POST'])
def add_inventory():
    data = request.json
    try:
        # Generamos el ID aquí para que nunca sea NULL
        nuevo_id = str(uuid4())
        
        # Mapeamos los nombres del JSON (Frontend) a las columnas de la DB
        nuevo_rollo = Rollo(
            id=nuevo_id,
            name=data.get('name'),
            code=data.get('code'),
            category=data.get('category'),
            width_cm=float(data.get('widthCm', 0)),
            price_per_meter=float(data.get('pricePerMeter', 0)),
            meters_left=float(data.get('metersLeft', 0)),
            status=data.get('status', 'in_stock')
        )
        
        db.session.add(nuevo_rollo)
        db.session.commit()
        
        return jsonify(nuevo_rollo.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
@inventory_bp.route('/inventory', methods=['PATCH'])
def update_stock():
    data = request.json
    print("\n--- DEBUG START ---")
    print(f"1. Datos que llegan del Frontend: {data}")
    try:
        if not data or 'id' not in data:
            return jsonify({"error": "ID de rollo requerido"}), 400

        # Buscamos el rollo directamente por su ID
        rollo = Rollo.query.get(data['id'])
        
        if not rollo:
            return jsonify({"error": "Rollo no encontrado"}), 404
            
        used = float(data.get('usedMeters', 0))
        rollo.meters_left = round(max(0, (rollo.meters_left or 0) - used), 2)
        
        db.session.commit()
        return jsonify(rollo.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400