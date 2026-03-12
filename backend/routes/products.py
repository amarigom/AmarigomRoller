from flask import Blueprint, render_template, jsonify

products_bp = Blueprint('products', __name__)

# Datos de productos (en producción esto vendría de una base de datos)
PRODUCTS = [
    {
        'id': 1,
        'name_es': 'Cortina Roller Sunscreen',
        'name_en': 'Sunscreen Roller Blind',
        'description_es': 'Filtra la luz solar manteniendo la visibilidad hacia el exterior',
        'description_en': 'Filters sunlight while maintaining outward visibility',
        'image': '/static/images/products/sunscreen.jpg',
        'category': 'sunscreen',
        'price': 15000
    },
    {
        'id': 2,
        'name_es': 'Cortina Roller Blackout',
        'name_en': 'Blackout Roller Blind',
        'description_es': 'Bloqueo total de luz para máxima privacidad',
        'description_en': 'Complete light blocking for maximum privacy',
        'image': '/static/images/products/blackout.jpg',
        'category': 'blackout',
        'price': 18000
    },
    {
        'id': 3,
        'name_es': 'Cortinas Tradicionales',
        'name_en': 'Traditional Curtains',
        'description_es': 'Elegancia clásica con telas de alta calidad',
        'description_en': 'Classic elegance with high-quality fabrics',
        'image': '/static/images/products/traditional.jpg',
        'category': 'traditional',
        'price': 25000
    },
    {
        'id': 101,
        'name_es': 'Combo Sunscreen',
        'name_en': 'Sunscreen Combo',
        'description_es': '2 cortinas roller sunscreen de hasta 1.5m x 2m',
        'description_en': '2 sunscreen roller blinds up to 1.5m x 2m',
        'image': '/static/images/products/sunscreen.jpg',
        'category': 'promo',
        'price': 22500,
        'original_price': 30000,
        'discount': 25
    },
    {
        'id': 102,
        'name_es': 'Blackout Premium',
        'name_en': 'Premium Blackout',
        'description_es': 'Cortina blackout premium con instalación incluida',
        'description_en': 'Premium blackout blind with installation included',
        'image': '/static/images/products/blackout.jpg',
        'category': 'promo',
        'price': 17500,
        'original_price': 25000,
        'discount': 30
    }
]

@products_bp.route('/')
def list_products():
    """Lista todos los productos"""
    return jsonify(PRODUCTS)

@products_bp.route('/<int:product_id>')
def get_product(product_id):
    """Obtiene un producto específico"""
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({'error': 'Producto no encontrado'}), 404

@products_bp.route('/promos')
def list_promos():
    """Lista solo productos en promoción"""
    promos = [p for p in PRODUCTS if p.get('category') == 'promo']
    return jsonify(promos)
