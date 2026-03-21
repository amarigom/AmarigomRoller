from flask import Blueprint, request, jsonify
from models import db, Supply, SupplyCategory, RecipeBOM 

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

# --- 3. ACTUALIZAR STOCK ---
@inventory_bp.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_stock_by_id(item_id):
    data = request.json
    try:
        insumo = Supply.query.get_or_404(item_id)
        
        if 'used_meters' in data:
            descuento = float(data['used_meters'])
            insumo.stock_actual = round(max(0, (insumo.stock_actual or 0) - descuento), 2)
        
        elif 'add_units' in data:
            incremento = float(data['add_units'])
            insumo.stock_actual = round((insumo.stock_actual or 0) + incremento, 2)
            
        elif 'new_total' in data:
            insumo.stock_actual = float(data['new_total'])

        db.session.commit()
        return jsonify(insumo.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# --- 4. CÁLCULO DINÁMICO DE RECETA (EXPLOSIÓN DE MATERIALES) ---
@inventory_bp.route('/test-recipe/<int:product_id>')
def test_recipe(product_id):
    try:
        # Buscamos los componentes (hijos) del producto padre
        components = RecipeBOM.query.filter_by(id_padre=product_id).all()
        
        if not components:
            return jsonify({"error": f"No se encontraron componentes para el ID {product_id}"}), 404
        
        # Medidas base de simulación (puedes luego recibirlas por query params)
        w_pedido = float(request.args.get('w', 150.0))
        h_pedido = float(request.args.get('h', 200.0))
        
        resultado = []

        for item in components:
            # Medidas y Deltas
            d_w = float(item.delta_ancho_cm or 0)
            d_h = float(item.delta_alto_cm or 0)
            c_base = float(getattr(item, 'cantidad_base', 1.0))
            
            # Cálculo de dimensiones finales (en metros para el consumo)
            final_w_m = (w_pedido + d_w) / 100
            final_h_m = (h_pedido + d_h) / 100
            
            # Lógica de consumo según el tipo de cálculo
            consumo = 0
            if item.tipo_calculo == 'lineal_ancho':
                consumo = final_w_m * c_base
            elif item.tipo_calculo == 'lineal_alto':
                consumo = final_h_m * c_base
            elif item.tipo_calculo == 'superficie':
                consumo = (final_w_m * final_h_m) * c_base
            elif item.tipo_calculo == 'fijo':
                consumo = c_base

            # NUEVO: Lógica de Costeo
            # Accedemos al precio que está en la tabla 'insumos' vía la relación
            precio_unit = float(item.insumo.precio_costo_unitario or 0) if item.insumo else 0
            costo_parcial = round(consumo * precio_unit, 2)

            resultado.append({
                "componente": item.nombre_producto,
                "consumo_m_o_m2": round(consumo, 4),
                "medida_corte": f"{w_pedido + d_w} x {h_pedido + d_h} cm",
                "precio_unitario": precio_unit,
                "costo_parcial": costo_parcial
            })
            
        return jsonify({
            "status": "success", 
            "medidas_pedido": {"ancho": w_pedido, "alto": h_pedido},
            "explosion": resultado
        })
    
    except Exception as e:
        return jsonify({"error": f"Error en el cálculo: {str(e)}"}), 500

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