from flask import Blueprint, request, jsonify
from models import db, Supply, SupplyCategory, RecipeBOM ,RetazoTela



inventory_bp = Blueprint('inventory', __name__)

# --- 1. OBTENER TODO EL INVENTARIO ---
@inventory_bp.route('/inventory', methods=['GET'])
def get_inventory():
    try:
        insumos = Supply.query.all()
        return jsonify([r.to_dict() for r in insumos])
    except Exception as e:
        return jsonify({"error": f"Error al obtener inventario: {str(e)}"}), 500

# --- 2. AGREGAR NUEVO INSUMO ---
@inventory_bp.route('/inventory', methods=['POST'])
def add_inventory():
    data = request.json
    try:
        nuevo_insumo = Supply(
            name=data.get('name'),
            codigo_sku=data.get('codigo_sku'),
            categoria_id=data.get('categoria_id'),
            ancho_cm=float(data.get('ancho_cm', 0)),
            precio_costo_unitario=float(data.get('precio_costo_unitario', 0)),
            stock_actual=float(data.get('stock_actual', 0)),
            unidad_medida=data.get('unidad_medida', 'metro') 
        )
        db.session.add(nuevo_insumo)
        db.session.commit()
        return jsonify(nuevo_insumo.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# --- 5. OBTENER CATEGORÍAS ---
@inventory_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        categorias = SupplyCategory.query.all()
        resultado = [{"id": c.id, "name": c.name} for c in categorias]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 6. ELIMINAR INSUMO ---
@inventory_bp.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        insumo = Supply.query.get_or_404(item_id)
        db.session.delete(insumo)
        db.session.commit()
        return jsonify({"message": "Insumo eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400