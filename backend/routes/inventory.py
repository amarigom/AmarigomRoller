import logging

from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from models import db, Supply, SupplyCategory
from schemas import InsumoIn

inventory_bp = Blueprint('inventory', __name__)
logger = logging.getLogger(__name__)

MAX_PAGE_SIZE = 500


def _errores_validacion(e):
    return [f"{'.'.join(str(p) for p in err['loc'])}: {err['msg']}" for err in e.errors()]


# --- 1. OBTENER INVENTARIO (con paginación opcional: ?limit=50&offset=0) ---
@inventory_bp.route('/inventory', methods=['GET'])
def get_inventory():
    try:
        query = Supply.query.options(joinedload(Supply.category)).order_by(Supply.id)

        limit = request.args.get('limit', type=int)
        if limit is not None:
            offset = max(request.args.get('offset', default=0, type=int), 0)
            query = query.limit(min(max(limit, 1), MAX_PAGE_SIZE)).offset(offset)

        return jsonify([s.to_dict() for s in query.all()])
    except Exception:
        logger.exception("Error al obtener inventario")
        return jsonify({"error": "Error al obtener inventario"}), 500


# --- 2. AGREGAR NUEVO INSUMO ---
@inventory_bp.route('/inventory', methods=['POST'])
def add_inventory():
    try:
        datos = InsumoIn.model_validate(request.get_json(silent=True) or {})
    except ValidationError as e:
        return jsonify({"error": "Datos inválidos", "detalles": _errores_validacion(e)}), 400

    try:
        nuevo_insumo = Supply(
            name=datos.name,
            codigo_sku=datos.codigo_sku,
            categoria_id=datos.categoria_id,
            ancho_cm=datos.ancho_cm,
            precio_costo_unitario=datos.precio_costo_unitario,
            stock_actual=datos.stock_actual,
            unidad_medida=datos.unidad_medida,
        )
        db.session.add(nuevo_insumo)
        db.session.commit()
        return jsonify(nuevo_insumo.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "El código SKU ya existe o la categoría no es válida"}), 409
    except Exception:
        db.session.rollback()
        logger.exception("Error al crear insumo")
        return jsonify({"error": "No se pudo guardar el insumo"}), 500


# --- 3. OBTENER CATEGORÍAS ---
@inventory_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        categorias = SupplyCategory.query.order_by(SupplyCategory.name).all()
        return jsonify([{"id": c.id, "name": c.name} for c in categorias]), 200
    except Exception:
        logger.exception("Error al obtener categorías")
        return jsonify({"error": "Error al obtener categorías"}), 500


# --- 4. ELIMINAR INSUMO ---
@inventory_bp.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    insumo = db.session.get(Supply, item_id)
    if insumo is None:
        return jsonify({"error": "Insumo no encontrado"}), 404
    try:
        db.session.delete(insumo)
        db.session.commit()
        return jsonify({"message": "Insumo eliminado correctamente"}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "No se puede eliminar: el insumo se usa en recetas o retazos"}), 409
    except Exception:
        db.session.rollback()
        logger.exception("Error al eliminar insumo %s", item_id)
        return jsonify({"error": "No se pudo eliminar el insumo"}), 500
