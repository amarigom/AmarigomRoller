from flask import Blueprint, jsonify, request

import container
from schemas.auth import ChangePasswordIn, LoginIn
from schemas.common import parse_payload
from security.decorators import auth_required
from flask import g

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    datos = parse_payload(LoginIn, request.get_json(silent=True))
    return jsonify(container.auth_service().login(datos.email, datos.password).model_dump(mode='json'))


@auth_bp.route('/me', methods=['GET'])
@auth_required
def me():
    return jsonify(container.auth_service().token_response(g.current_user).model_dump(mode='json', exclude={'token'}))


@auth_bp.route('/change-password', methods=['POST'])
@auth_required
def change_password():
    datos = parse_payload(ChangePasswordIn, request.get_json(silent=True))
    container.auth_service().change_password(g.current_user, datos.actual, datos.nueva)
    return jsonify({"status": "success", "message": "Contraseña actualizada"})
