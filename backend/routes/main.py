from flask import Blueprint, jsonify, request, session

import container
from schemas.common import parse_payload
from schemas.quote import PresupuestoIn
from utils.translations import get_translations

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    lang = session.get('language', 'es')
    return jsonify({
        "status": "ok",
        "message": "Cerebro de Python conectado",
        "translations": get_translations()[lang],
    })


@main_bp.route('/set-language/<lang>')
def set_language(lang):
    if lang in ['es', 'en']:
        session['language'] = lang
        session.modified = True
    return jsonify({'success': True, 'language': lang}), 200


@main_bp.route('/api/presupuesto', methods=['POST'])
def recibir_presupuesto():
    datos = parse_payload(PresupuestoIn, request.get_json(silent=True))
    container.quote_service().request_quote(datos)
    return jsonify({
        "status": "success",
        "message": "¡Solicitud enviada! Nos contactaremos pronto.",
    }), 200
