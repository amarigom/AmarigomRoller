from flask import Blueprint, jsonify
from models.recipe_bom import RecipeBOM
from models import db

recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/api/recipes/<int:product_id>', methods=['GET'])
def get_recipe_explosion(product_id):
    try:
        # Buscamos los componentes que tienen como parent_id al product_id enviado
        components = RecipeBOM.query.filter_by(parent_id=product_id).all()
        
        if not components:
            return jsonify({"error": "No se encontró la receta para este producto"}), 404

        # Armamos la lista para el Frontend
        recipe_data = []
        for item in components:
            recipe_data.append({
                "id": item.id,
                "component_name": item.component_name, # El nombre en inglés que definimos
                "width_delta": float(item.width_delta_cm),
                "height_delta": float(item.height_delta_cm),
                "base_quantity": float(item.base_quantity),
                "calculation_type": item.calculation_type,
                "description": item.description,
                "sku": item.supply.codigo_sku if item.supply else None
            })

        return jsonify(recipe_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500