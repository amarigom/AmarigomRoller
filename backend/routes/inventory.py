from flask import Blueprint, jsonify, request

import container
from schemas.common import parse_payload
from schemas.inventory import InsumoIn
from security.decorators import permission_required
from security.permissions import INVENTORY_DELETE, INVENTORY_READ, INVENTORY_WRITE

inventory_bp = Blueprint('inventory', __name__)


@inventory_bp.route('/inventory', methods=['GET'])
@permission_required(INVENTORY_READ)
def get_inventory():
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', default=0, type=int)
    items = container.inventory_service().list_supplies(limit, offset)
    return jsonify([i.model_dump() for i in items])


@inventory_bp.route('/inventory', methods=['POST'])
@permission_required(INVENTORY_WRITE)
def add_inventory():
    datos = parse_payload(InsumoIn, request.get_json(silent=True))
    return jsonify(container.inventory_service().create_supply(datos).model_dump()), 201


@inventory_bp.route('/categories', methods=['GET'])
@permission_required(INVENTORY_READ)
def get_categories():
    return jsonify([c.model_dump() for c in container.inventory_service().list_categories()])


@inventory_bp.route('/inventory/<int:item_id>', methods=['DELETE'])
@permission_required(INVENTORY_DELETE)
def delete_item(item_id):
    container.inventory_service().delete_supply(item_id)
    return jsonify({"message": "Insumo eliminado correctamente"})
