from flask import Blueprint, request, jsonify, session

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    """Agregar producto al carrito"""
    data = request.get_json()
    
    if 'cart' not in session:
        session['cart'] = []
    
    cart_item = {
        'product_id': data['product_id'],
        'name': data['name'],
        'price': data['price'],
        'quantity': data.get('quantity', 1),
        'image': data.get('image', '')
    }
    
    # Verificar si el producto ya está en el carrito
    existing_item = next((item for item in session['cart'] 
                         if item['product_id'] == cart_item['product_id']), None)
    
    if existing_item:
        existing_item['quantity'] += cart_item['quantity']
    else:
        session['cart'].append(cart_item)
    
    session.modified = True
    
    return jsonify({
        'success': True,
        'cart_count': len(session['cart']),
        'message': 'Producto agregado al carrito'
    })

@cart_bp.route('/get')
def get_cart():
    """Obtener contenido del carrito"""
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    
    return jsonify({
        'items': cart,
        'total': total,
        'count': len(cart)
    })

@cart_bp.route('/remove/<int:product_id>', methods=['DELETE'])
def remove_from_cart(product_id):
    """Eliminar producto del carrito"""
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] 
                          if item['product_id'] != product_id]
        session.modified = True
    
    return jsonify({'success': True})

@cart_bp.route('/clear', methods=['POST'])
def clear_cart():
    """Vaciar el carrito"""
    session['cart'] = []
    session.modified = True
    return jsonify({'success': True})
