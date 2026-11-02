from flask import Blueprint, jsonify, request

import container
from exceptions import ValidationFailed
from schemas.common import parse_payload
from schemas.recipes import MAX_MEDIDA_CM, MedidasIn
from security.decorators import permission_required
from security.permissions import RECIPES_PRODUCE, RECIPES_READ

recipes_bp = Blueprint('recipes', __name__)


def _medidas(source):
    try:
        return parse_payload(MedidasIn, source)
    except ValidationFailed as e:
        raise ValidationFailed(
            f"Medidas inválidas: deben ser números entre 0 y {MAX_MEDIDA_CM} cm", e.detalles)


@recipes_bp.route('/test-recipe/<int:product_id>', methods=['GET'])
@recipes_bp.route('/recipes/<int:product_id>/explosion', methods=['GET'])
@permission_required(RECIPES_READ)
def explosion(product_id):
    medidas = _medidas(request.args.to_dict())
    resultado = container.recipe_service().explode(product_id, medidas.w, medidas.h)
    return jsonify(resultado.model_dump())


@recipes_bp.route('/recipes/<int:product_id>/produce', methods=['POST'])
@permission_required(RECIPES_PRODUCE)
def produce(product_id):
    cuerpo = request.get_json(silent=True) or {}
    if "w" not in cuerpo or "h" not in cuerpo:
        raise ValidationFailed("Indicá el ancho (w) y el alto (h) en cm")
    medidas = _medidas(cuerpo)
    resultado = container.recipe_service().produce(product_id, medidas.w, medidas.h)
    return jsonify(resultado.model_dump())


@recipes_bp.route('/recipes/<int:product_id>', methods=['GET'])
@permission_required(RECIPES_READ)
def get_recipe_base(product_id):
    items = container.recipe_service().base_recipe(product_id)
    return jsonify([i.model_dump() for i in items])
