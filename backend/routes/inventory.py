from flask import Blueprint, jsonify, request

import container
from schemas.common import parse_payload
from schemas.inventory import (
    BulkPriceIn, InsumoIn, InventoryMovementIn, ScrapReservationIn, StockMinimumIn,
)
from security.decorators import permission_required
from security.permissions import (
    INVENTORY_DELETE, INVENTORY_MANAGE, INVENTORY_READ, INVENTORY_WRITE,
)

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


@inventory_bp.route('/inventory/alerts', methods=['GET'])
@inventory_bp.route('/inventory/purchase-suggestions', methods=['GET'])
@permission_required(INVENTORY_READ)
def stock_alerts():
    return jsonify([a.model_dump() for a in container.inventory_service().alertas_stock()])


@inventory_bp.route('/inventory/scraps', methods=['GET'])
@permission_required(INVENTORY_READ)
def list_scraps():
    limit = request.args.get('limit', default=500, type=int)
    return jsonify([r.model_dump() for r in container.inventory_service().retazos_disponibles(limit)])


@inventory_bp.route('/inventory/scraps/<int:scrap_id>/reserve', methods=['POST'])
@permission_required(INVENTORY_WRITE)
def reserve_scrap(scrap_id):
    datos = parse_payload(ScrapReservationIn, request.get_json(silent=True))
    retazo = container.inventory_service().reservar_retazo(scrap_id, datos.referencia)
    return jsonify(retazo.model_dump(mode='json'))


@inventory_bp.route('/inventory/scraps/<int:scrap_id>/release', methods=['POST'])
@permission_required(INVENTORY_WRITE)
def release_scrap(scrap_id):
    retazo = container.inventory_service().liberar_retazo(scrap_id)
    return jsonify(retazo.model_dump(mode='json'))


@inventory_bp.route('/inventory/<int:item_id>/movements', methods=['GET'])
@permission_required(INVENTORY_READ)
def list_movements(item_id):
    limit = request.args.get('limit', default=100, type=int)
    return jsonify([m.model_dump(mode='json') for m in container.inventory_service().movimientos(item_id, limit)])


@inventory_bp.route('/inventory/<int:item_id>/movements', methods=['POST'])
@permission_required(INVENTORY_WRITE)
def add_movement(item_id):
    datos = parse_payload(InventoryMovementIn, request.get_json(silent=True))
    movement = container.inventory_service().registrar_movimiento(item_id, datos)
    return jsonify(movement.model_dump(mode='json')), 201


@inventory_bp.route('/inventory/<int:item_id>/minimum', methods=['PATCH'])
@permission_required(INVENTORY_MANAGE)
def update_stock_minimum(item_id):
    datos = parse_payload(StockMinimumIn, request.get_json(silent=True))
    return jsonify(container.inventory_service().actualizar_stock_minimo(
        item_id, datos.stock_minimo).model_dump())


@inventory_bp.route('/inventory/<int:item_id>/prices', methods=['GET'])
@permission_required(INVENTORY_READ)
def price_history(item_id):
    return jsonify([p.model_dump(mode='json') for p in container.inventory_service().historial_precios(item_id)])


@inventory_bp.route('/inventory/prices', methods=['POST'])
@permission_required(INVENTORY_MANAGE)
def update_prices():
    datos = parse_payload(BulkPriceIn, request.get_json(silent=True))
    return jsonify(container.inventory_service().actualizar_precios(datos))


@inventory_bp.route('/categories', methods=['GET'])
@permission_required(INVENTORY_READ)
def get_categories():
    return jsonify([c.model_dump() for c in container.inventory_service().list_categories()])


@inventory_bp.route('/inventory/<int:item_id>', methods=['DELETE'])
@permission_required(INVENTORY_DELETE)
def delete_item(item_id):
    container.inventory_service().delete_supply(item_id)
    return jsonify({"message": "Insumo archivado correctamente"})
