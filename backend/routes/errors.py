import logging

from flask import jsonify
from werkzeug.exceptions import HTTPException

from exceptions import AppError

logger = logging.getLogger(__name__)


def _body(status, message, detalles=None):
    # "error" lo lee el inventario y "message" el resto del front
    return jsonify({
        "status": "error", "error": message, "message": message, "detalles": detalles or [],
    }), status


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(e):
        return _body(e.status_code, e.message, e.detalles)

    @app.errorhandler(HTTPException)
    def handle_http_error(e):
        return _body(e.code, e.description)

    @app.errorhandler(Exception)
    def handle_unexpected(e):
        logger.exception("Error no controlado")
        return _body(500, "Error interno del servidor")
