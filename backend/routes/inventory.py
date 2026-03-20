from flask import Blueprint, request, jsonify
from uuid import uuid4
from models import db, Supply, SupplyCategory  

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/inventory', methods=['GET'])
def get_inventory():
    try:
        
        insumos = Supply.query.all()
        return jsonify([r.to_dict() for r in insumos])
    except Exception as e:
        return jsonify({"error": f"Error al obtener inventario: {str(e)}"}), 500

@inventory_bp.route('/inventory', methods=['POST'])
def add_inventory():
    data = request.json
    try:
        # Generamos el ID aquí para que nunca sea NULL
        nuevo_id = str(uuid4())
        
        # Mapeamos los nombres del JSON (Frontend) a las columnas de la DB
        nuevo_insumo = Supply(
        # A la IZQUIERDA: Nombre en la DB (Python/SQLAlchemy)
        # A la DERECHA: Nombre que viene en el JSON de React (data.get)
        name=data.get('name'),
        codigo_sku=data.get('codigo_sku'),           # Antes decía code=
        categoria_id=data.get('categoria_id'),       # Usamos el ID que viene del select
        ancho_cm=float(data.get('ancho_cm', 0)),     # Antes decía widthCm=
        precio_costo_unitario=float(data.get('precio_costo_unitario', 0)), # Antes decía price=
        stock_actual=float(data.get('stock_actual', 0)), # Antes decía metersLeft=
        unidad_medida=data.get('unidad_medida', 'metro') 
    )
        
        db.session.add(nuevo_insumo)
        db.session.commit()
        
        return jsonify(nuevo_insumo.to_dict()), 201
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
            return jsonify({"error": "ID de insumo requerido"}), 400

        # Buscamos el rollo directamente por su ID
        insumo = Supply.query.get(data['id'])
        
        if not insumo:
            return jsonify({"error": "Insumo no encontrado"}), 404
            
        used = float(data.get('usedMeters', 0))
        insumo.meters_left = round(max(0, (insumo.meters_left or 0) - used), 2)
        
        db.session.commit()
        return jsonify(insumo.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
    # --- NUEVA RUTA PARA CATEGORÍAS ---
@inventory_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        # Buscamos todas las categorías de la tabla 'categorias_insumos'
        categorias = SupplyCategory.query.all()
        
        # Las convertimos a una lista de diccionarios para que React las entienda
        resultado = [{"id": c.id, "name": c.name} for c in categorias]
        
        return jsonify(resultado), 200
    except Exception as e:
        print(f"Error en get_categories: {e}") # Esto sale en tu terminal de Python
        return jsonify({"error": str(e)}), 500