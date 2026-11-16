from flask import Blueprint, jsonify, request

import container
from schemas.clients import ClienteIn
from schemas.common import parse_payload
from security.decorators import permission_required
from security.permissions import CLIENTS_READ, CLIENTS_WRITE

clients_bp = Blueprint('clients', __name__)


@clients_bp.route('/', methods=['GET'], strict_slashes=False)
@permission_required(CLIENTS_READ)
def list_clients():
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', default=0, type=int)
    clientes = container.client_service().list_clients(limit, offset)
    return jsonify([c.model_dump() for c in clientes])


@clients_bp.route('/', methods=['POST'], strict_slashes=False)
@permission_required(CLIENTS_WRITE)
def create_client():
    datos = parse_payload(ClienteIn, request.get_json(silent=True))
    cliente = container.client_service().create_client(datos)
    return jsonify({
        "status": "success",
        "message": "Cliente guardado con éxito",
        "client": cliente.model_dump(),
    }), 201
