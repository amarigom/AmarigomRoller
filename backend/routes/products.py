from flask import Blueprint, jsonify
from models import Product # Importamos el modelo que se conecta a Neon

# 1. Definimos el Blueprint con un nombre único
products_bp = Blueprint('products_api', __name__)

@products_bp.route('', methods=['GET'], strict_slashes=False)
def list_products():
    """Trae los productos reales de la tabla de Neon para la calculadora"""
    try:
        # Consultamos la tabla 'productos' en Neon
        # Usamos el to_dict() que mapeamos para React (con 'name' y 'category')
        db_products = Product.query.filter_by(activo=True).all()
        return jsonify([p.to_dict() for p in db_products])
    except Exception as e:
        print(f" Error en Neon (AMARIGOM DECO): {e}")
        return jsonify({"error": "No se pudo conectar con la base de datos"}), 500

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Busca un producto específico por su ID manual en Neon"""
    try:
        product = Product.query.get(product_id)
        if product:
            return jsonify(product.to_dict())
        return jsonify({'error': 'Producto no encontrado'}, {"message": f"El producto {product_id} aún no tiene definida su explosión de materiales."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@products_bp.route('/promos', methods=['GET'])
def list_promos():
    """Lista productos cuya categoría sea 'promo' en Neon"""
    try:
        promos = Product.query.filter_by(categoria='promo', activo=True).all()
        return jsonify([p.to_dict() for p in promos])
    except Exception as e:
        return jsonify({"error": str(e)}), 500