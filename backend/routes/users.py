from flask import Blueprint, jsonify, request

import container
from schemas.auth import UserCreateIn, UserUpdateIn
from schemas.common import parse_payload
from security.decorators import permission_required
from security.permissions import USERS_MANAGE

users_bp = Blueprint('users', __name__)


@users_bp.route('', methods=['GET'])
@permission_required(USERS_MANAGE)
def list_users():
    return jsonify([u.model_dump(mode='json') for u in container.user_service().list_users()])


@users_bp.route('', methods=['POST'])
@permission_required(USERS_MANAGE)
def create_user():
    datos = parse_payload(UserCreateIn, request.get_json(silent=True))
    return jsonify(container.user_service().create_user(datos).model_dump(mode='json')), 201


@users_bp.route('/<int:user_id>', methods=['PATCH'])
@permission_required(USERS_MANAGE)
def update_user(user_id):
    datos = parse_payload(UserUpdateIn, request.get_json(silent=True))
    return jsonify(container.user_service().update_user(user_id, datos).model_dump(mode='json'))
