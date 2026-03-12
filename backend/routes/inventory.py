# backend/routes/inventory.py
from flask import Blueprint, request, jsonify
import json
import os
from uuid import uuid4
from schemas import RolloBase # El que armamos antes

inventory_bp = Blueprint('inventory', __name__)
JSON_PATH = os.path.join(os.getcwd(), 'data', 'inventory.json')

def read_json():
    if not os.path.exists(JSON_PATH): return []
    with open(JSON_PATH, 'r') as f: return json.load(f)

def write_json(data):
    with open(JSON_PATH, 'w') as f: json.dump(data, f, indent=2)

@inventory_bp.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(read_json())

@inventory_bp.route('/inventory', methods=['POST'])
def add_inventory():
    inventory = read_json()
    new_roll = request.json
    
    # Pydantic valida que los datos estén bien antes de guardar
    try:
        # Agregamos ID si no viene
        if 'id' not in new_roll: new_roll['id'] = str(uuid4())
        
        # Validamos 
        valid_roll = RolloBase(**new_roll)
        
        inventory.append(valid_roll.model_dump(by_alias=True))
        write_json(inventory)
        return jsonify(inventory), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@inventory_bp.route('/inventory', methods=['PATCH'])
def update_stock():
    data = request.json
    inventory = read_json()
    
    for roll in inventory:
        if roll.get('id') == data['id']:
            current = float(roll['metersLeft'])
            used = float(data['usedMeters'])
            roll['metersLeft'] = round(max(0, current - used), 2)
            break
            
    write_json(inventory)
    return jsonify(inventory)