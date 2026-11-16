from flask import Blueprint, jsonify, request

import container
from schemas.common import parse_payload
from schemas.inventory import (
    BulkPriceIn, FabricPriceCsvIn, InsumoIn, InventoryMovementIn, InventoryMovementOut, ProfilePiecesIn, ProfileReconcileIn, PurchaseIn, ScrapReservationIn,
    StockMinimumIn, StockReconcileIn, TelaConfigIn,
)
from security.decorators import permission_required
from security.permissions import (
    COSTS_READ, INVENTORY_DELETE, INVENTORY_MANAGE, INVENTORY_READ, INVENTORY_WRITE, QUOTES_READ,
)
from security.price_visibility import puede_ver_costos

inventory_bp = Blueprint('inventory', __name__)


@inventory_bp.route('/inventory', methods=['GET'])
@permission_required(INVENTORY_READ)
def get_inventory():
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', default=0, type=int)
    items = container.inventory_service().list_supplies(limit, offset)
    campos = {'id', 'code', 'name', 'category', 'metersLeft', 'widthCm', 'unit', 'totalMeters',
              'stock_minimo', 'es_tela', 'largo_pieza_cm', 'unidad_compra', 'factor_conversion',
              'perfil_en_receta', 'piezas_enteras', 'piezas_retazos', 'longitud_piezas_cm', 'piezas_conciliadas'}
    return jsonify([i.model_dump() if puede_ver_costos() else i.model_dump(include=campos) for i in items])


@inventory_bp.route('/inventory', methods=['POST'])
@permission_required(INVENTORY_MANAGE)
def add_inventory():
    datos = parse_payload(InsumoIn, request.get_json(silent=True))
    return jsonify(container.inventory_service().create_supply(datos).model_dump()), 201


@inventory_bp.route('/inventory/<int:item_id>/fabric', methods=['PATCH'])
@permission_required(INVENTORY_MANAGE)
def configure_fabric(item_id):
    datos = parse_payload(TelaConfigIn, request.get_json(silent=True))
    return jsonify(container.inventory_service().configurar_tela(item_id, datos).model_dump())


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


@inventory_bp.route('/inventory/<int:item_id>/reconcile', methods=['GET'])
@permission_required(INVENTORY_READ)
def stock_reconciliation_status(item_id):
    return jsonify(container.inventory_service().estado_conciliacion(item_id))


@inventory_bp.route('/inventory/<int:item_id>/reconcile', methods=['POST'])
@permission_required(INVENTORY_MANAGE)
def reconcile_stock(item_id):
    datos = parse_payload(StockReconcileIn, request.get_json(silent=True))
    return jsonify(container.inventory_service().conciliar_stock(item_id, datos))


@inventory_bp.route('/inventory/<int:item_id>/pieces', methods=['POST'])
@permission_required(INVENTORY_WRITE)
def add_profile_pieces(item_id):
    datos = parse_payload(ProfilePiecesIn, request.get_json(silent=True))
    movement = container.inventory_service().ingresar_piezas(item_id, datos)
    return jsonify(movement.model_dump(mode='json')), 201


@inventory_bp.route('/inventory/<int:item_id>/pieces/reconcile', methods=['GET'])
@permission_required(INVENTORY_READ)
def get_profile_reconciliation(item_id):
    return jsonify(container.inventory_service().estado_piezas(item_id))


@inventory_bp.route('/inventory/<int:item_id>/pieces/reconcile', methods=['POST'])
@permission_required(INVENTORY_MANAGE)
def reconcile_profile_pieces(item_id):
    datos = parse_payload(ProfileReconcileIn, request.get_json(silent=True))
    movement = container.inventory_service().conciliar_piezas(item_id, datos)
    return jsonify(InventoryMovementOut.from_model(movement).model_dump(mode='json')), 201


@inventory_bp.route('/inventory/<int:item_id>/purchases', methods=['POST'])
@permission_required(INVENTORY_WRITE)
def add_purchase(item_id):
    datos = parse_payload(PurchaseIn, request.get_json(silent=True))
    movement = container.inventory_service().ingresar_compra(item_id, datos)
    return jsonify(movement.model_dump(mode='json')), 201


@inventory_bp.route('/inventory/<int:item_id>/minimum', methods=['PATCH'])
@permission_required(INVENTORY_MANAGE)
def update_stock_minimum(item_id):
    datos = parse_payload(StockMinimumIn, request.get_json(silent=True))
    return jsonify(container.inventory_service().actualizar_stock_minimo(
        item_id, datos.stock_minimo).model_dump())


@inventory_bp.route('/inventory/<int:item_id>/prices', methods=['GET'])
@permission_required(COSTS_READ)
def price_history(item_id):
    return jsonify([p.model_dump(mode='json') for p in container.inventory_service().historial_precios(item_id)])


@inventory_bp.route('/inventory/prices', methods=['POST'])
@permission_required(INVENTORY_MANAGE)
def update_prices():
    datos = parse_payload(BulkPriceIn, request.get_json(silent=True))
    return jsonify(container.inventory_service().actualizar_precios(datos))


@inventory_bp.route('/inventory/prices/sheets', methods=['GET'])
@permission_required(QUOTES_READ)
def sheets_status():
    from services.google_sheets_prices import estado_sincronizacion
    estado = estado_sincronizacion()
    if not puede_ver_costos():
        estado['error'] = None
    return jsonify(estado)


@inventory_bp.route('/inventory/prices/sheets', methods=['POST'])
@permission_required(INVENTORY_MANAGE)
def sheets_sync():
    from services.google_sheets_prices import sincronizar_precios
    return jsonify(sincronizar_precios())


@inventory_bp.route('/inventory/prices/fabrics/import', methods=['POST'])
@permission_required(INVENTORY_MANAGE)
def import_fabric_prices():
    datos = parse_payload(FabricPriceCsvIn, request.get_json(silent=True))
    return jsonify(container.inventory_service().importar_precios_tela(datos))


@inventory_bp.route('/categories', methods=['GET'])
@permission_required(INVENTORY_READ)
def get_categories():
    return jsonify([c.model_dump() for c in container.inventory_service().list_categories()])


@inventory_bp.route('/inventory/<int:item_id>', methods=['DELETE'])
@permission_required(INVENTORY_DELETE)
def delete_item(item_id):
    container.inventory_service().delete_supply(item_id)
    return jsonify({"message": "Insumo archivado correctamente"})
