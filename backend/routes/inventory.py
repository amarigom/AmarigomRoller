from flask import Blueprint, request, jsonify
from uuid import uuid4
from models import db, Rollo  # <--- Importamos nuestro modelo modularizado

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/inventory', methods=['GET'])
def get_inventory():
    try:
        # SELECT * FROM rollos;
        rollos = Rollo.query.all()
        return jsonify([r.to_dict() for r in rollos])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@inventory_bp.route('/inventory', methods=['POST'])
def add_inventory():
    data = request.json
    try:
        # Generamos ID si no existe
        nuevo_id = data.get('id') or str(uuid4())
        
        # Creamos la instancia del modelo (usando los nombres de tu nueva DB)
        nuevo_rollo = Rollo(
            id=nuevo_id,
            name=data['name'],
            color=data.get('color', ''),
            meters_total=float(data.get('metersTotal', 0)),
            meters_left=float(data.get('metersLeft', data.get('metersTotal', 0)))
        )
        
        db.session.add(nuevo_rollo)
        db.session.commit()
        
        return jsonify(nuevo_rollo.to_dict()), 201
    except Exception as e:
        db.session.rollback() # Si falla, deshacemos cambios
        return jsonify({"error": str(e)}), 400

@inventory_bp.route('/inventory', methods=['PATCH'])
def update_stock():
    data = request.json
    try:
        # Buscamos el rollo directamente por su ID (Mucho más eficiente que el for loop)
        rollo = Rollo.query.get(data['id'])
        
        if not rollo:
            return jsonify({"error": "Rollo no encontrado"}), 404
            
        used = float(data['usedMeters'])
        rollo.meters_left = round(max(0, rollo.meters_left - used), 2)
        
        db.session.commit()
        return jsonify(rollo.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400