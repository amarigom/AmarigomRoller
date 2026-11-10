from flask import Blueprint, jsonify, request

import container
from exceptions import ValidationFailed
from schemas.common import parse_payload
from schemas.recipes import (
    MAX_MEDIDA_CM, DuplicateIn, ImportIn, MedidasIn, PreviewIn, ProductIn, RecipeVersionIn,
)
from security.decorators import permission_required
from security.permissions import RECIPES_PRODUCE, RECIPES_READ, RECIPES_WRITE
from services import recipe_import

recipes_bp = Blueprint('recipes', __name__)

PARAMETROS_RESERVADOS = {'w', 'h', 'fecha', 'version', 'opciones', 'referencia'}
MAX_OPCIONES = 20


def _medidas(source):
    try:
        return parse_payload(MedidasIn, source)
    except ValidationFailed as e:
        raise ValidationFailed(
            f"Medidas inválidas: deben ser números entre 0 y {MAX_MEDIDA_CM} cm", e.detalles)


def _valor(texto):
    if not isinstance(texto, str):
        return texto
    try:
        return float(texto)
    except ValueError:
        return texto


def _opciones(pares):
    """Variantes del pedido (sistema=motor, color=blanco...): usables en condiciones y fórmulas."""
    opciones = {
        k: _valor(v) for k, v in pares.items()
        if k not in PARAMETROS_RESERVADOS and k.isidentifier() and len(k) <= 30
        and isinstance(v, (str, int, float)) and len(str(v)) <= 50
    }
    if len(opciones) > MAX_OPCIONES:
        raise ValidationFailed(f"Se permiten hasta {MAX_OPCIONES} opciones")
    return opciones


@recipes_bp.route('/test-recipe/<int:product_id>', methods=['GET'])
@recipes_bp.route('/recipes/<int:product_id>/explosion', methods=['GET'])
@permission_required(RECIPES_READ)
def explosion(product_id):
    medidas = _medidas(request.args.to_dict())
    resultado = container.recipe_service().explode(
        product_id, medidas.w, medidas.h,
        opciones=_opciones(request.args.to_dict()), fecha=medidas.fecha, version=medidas.version,
        referencia=medidas.referencia)
    return jsonify(resultado.model_dump())


@recipes_bp.route('/recipes/<int:product_id>/produce', methods=['POST'])
@permission_required(RECIPES_PRODUCE)
def produce(product_id):
    cuerpo = request.get_json(silent=True) or {}
    if "w" not in cuerpo or "h" not in cuerpo:
        raise ValidationFailed("Indicá el ancho (w) y el alto (h) en cm")
    medidas = _medidas(cuerpo)
    opciones = cuerpo.get('opciones') if isinstance(cuerpo.get('opciones'), dict) else {}
    resultado = container.recipe_service().produce(
        product_id, medidas.w, medidas.h, _opciones(opciones), medidas.referencia)
    return jsonify(resultado.model_dump())


@recipes_bp.route('/recipes/<int:product_id>', methods=['GET'])
@permission_required(RECIPES_READ)
def get_recipe_base(product_id):
    items = container.recipe_service().base_recipe(product_id)
    return jsonify([i.model_dump() for i in items])


@recipes_bp.route('/recipes/calculation-types', methods=['GET'])
@permission_required(RECIPES_READ)
def calculation_types():
    return jsonify(container.recipe_service().calculation_types())


@recipes_bp.route('/recipes/<int:product_id>/versions', methods=['GET'])
@permission_required(RECIPES_READ)
def list_versions(product_id):
    return jsonify([v.model_dump(mode='json') for v in container.recipe_service().versions(product_id)])


@recipes_bp.route('/recipes/<int:product_id>/versions', methods=['POST'])
@permission_required(RECIPES_WRITE)
def publish_version(product_id):
    datos = parse_payload(RecipeVersionIn, request.get_json(silent=True))
    version = container.recipe_service().publish_version(product_id, datos)
    return jsonify(version.model_dump(mode='json')), 201


@recipes_bp.route('/recipes/products', methods=['GET'])
@permission_required(RECIPES_READ)
def list_products():
    return jsonify([p.model_dump() for p in container.recipe_service().products()])


@recipes_bp.route('/recipes/products', methods=['POST'])
@permission_required(RECIPES_WRITE)
def create_product():
    datos = parse_payload(ProductIn, request.get_json(silent=True))
    return jsonify(container.recipe_service().create_product(datos).model_dump()), 201


@recipes_bp.route('/recipes/<int:product_id>/detail', methods=['GET'])
@permission_required(RECIPES_READ)
def recipe_detail(product_id):
    version = request.args.get('version', type=int)
    items = container.recipe_service().version_detail(product_id, version)
    return jsonify([i.model_dump() for i in items])


@recipes_bp.route('/recipes/preview', methods=['POST'])
@permission_required(RECIPES_WRITE)
def preview():
    datos = parse_payload(PreviewIn, request.get_json(silent=True))
    datos.opciones = _opciones(datos.opciones)
    return jsonify(container.recipe_service().preview(datos).model_dump())


@recipes_bp.route('/recipes/<int:product_id>/duplicate', methods=['POST'])
@permission_required(RECIPES_WRITE)
def duplicate(product_id):
    datos = parse_payload(DuplicateIn, request.get_json(silent=True))
    producto, version = container.recipe_service().duplicate(product_id, datos)
    return jsonify({'producto': producto.model_dump(), 'version': version.model_dump(mode='json')}), 201


@recipes_bp.route('/recipes/import', methods=['POST'])
@permission_required(RECIPES_WRITE)
def import_recipes():
    datos = parse_payload(ImportIn, request.get_json(silent=True))
    return jsonify(container.recipe_service().import_csv(datos))


@recipes_bp.route('/recipes/import/template', methods=['GET'])
@permission_required(RECIPES_READ)
def import_template():
    return jsonify({'csv': recipe_import.plantilla()})
