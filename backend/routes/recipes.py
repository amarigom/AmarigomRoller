import logging

from flask import Blueprint, jsonify, request
from sqlalchemy.orm import joinedload

from models import db, RecipeBOM, RetazoTela
from services.costeo import calcular_explosion

recipes_bp = Blueprint('recipes', __name__)
logger = logging.getLogger(__name__)

MAX_MEDIDA_CM = 1000


def _leer_medida(nombre, default):
    valor = float(request.args.get(nombre, default))
    if not 0 < valor <= MAX_MEDIDA_CM:
        raise ValueError(nombre)
    return valor


@recipes_bp.route('/test-recipe/<int:product_id>', methods=['GET'])
def test_recipe(product_id):
    try:
        try:
            w_pedido = _leer_medida('w', 100.0)
            h_pedido = _leer_medida('h', 100.0)
        except ValueError:
            return jsonify({
                "status": "error",
                "message": f"Medidas inválidas: deben ser números entre 0 y {MAX_MEDIDA_CM} cm"
            }), 400

        components = (
            RecipeBOM.query
            .options(joinedload(RecipeBOM.insumo))
            .filter_by(id_padre=product_id)
            .all()
        )
        if not components:
            return jsonify({
                "status": "error",
                "message": f"El producto {product_id} aún no tiene definida su explosión de materiales."
            }), 404

        ids_insumo = {c.id_insumo for c in components if c.id_insumo}
        retazos_por_insumo = {}
        if ids_insumo:
            retazos = RetazoTela.query.filter(
                RetazoTela.id_insumo_base.in_(ids_insumo),
                RetazoTela.estado == 'disponible'
            ).all()
            for r in retazos:
                retazos_por_insumo.setdefault(r.id_insumo_base, []).append(r)

        resultado, total = calcular_explosion(components, retazos_por_insumo, w_pedido, h_pedido)

        return jsonify({
            "status": "success",
            "explosion": resultado,
            "total_materiales": total
        })

    except Exception:
        logger.exception("Error calculando la receta del producto %s", product_id)
        return jsonify({"status": "error", "message": "Error interno al calcular la receta"}), 500


@recipes_bp.route('/recipes/<int:product_id>', methods=['GET'])
def get_recipe_base(product_id):
    try:
        components = (
            RecipeBOM.query
            .options(joinedload(RecipeBOM.insumo))
            .filter_by(id_padre=product_id)
            .all()
        )

        if not components:
            return jsonify({
                "status": "error",
                "message": f"El producto {product_id} no tiene una receta definida en la base de datos."
            }), 404

        resultado = []
        for item in components:
            insumo = item.insumo
            nombre = (insumo.name if insumo else None) or item.nombre_producto or "Insumo"
            resultado.append({
                "id": item.id,
                "componente": nombre,
                "cantidad_base": float(item.cantidad_base or 0.0)
            })

        return jsonify(resultado), 200

    except Exception:
        logger.exception("Error obteniendo la receta del producto %s", product_id)
        return jsonify({"status": "error", "message": "Error interno al obtener la receta"}), 500
