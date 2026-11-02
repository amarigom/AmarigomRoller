import logging

from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Cliente
from schemas import ClienteIn

clients_bp = Blueprint('clients', __name__)
logger = logging.getLogger(__name__)

MAX_PAGE_SIZE = 500


# --- GET: OBTENER CLIENTES (con paginación opcional: ?limit=50&offset=0) ---
@clients_bp.route('/', methods=['GET'], strict_slashes=False)
def get_clients():
    try:
        query = Cliente.query.order_by(Cliente.id)
        limit = request.args.get('limit', type=int)
        if limit is not None:
            offset = max(request.args.get('offset', default=0, type=int), 0)
            query = query.limit(min(max(limit, 1), MAX_PAGE_SIZE)).offset(offset)
        return jsonify([c.to_dict() for c in query.all()]), 200
    except Exception:
        logger.exception("Error al obtener clientes")
        return jsonify({"status": "error", "message": "Error al obtener clientes"}), 500


# --- POST: CREAR CLIENTE ---
@clients_bp.route('/', methods=['POST'], strict_slashes=False)
def create_client():
    try:
        datos = ClienteIn.model_validate(request.get_json(silent=True) or {})
    except ValidationError:
        return jsonify({
            "status": "error",
            "message": "Faltan datos obligatorios o son inválidos (Nombre, Apellido y Email)"
        }), 400

    try:
        nuevo_cliente = Cliente(
            nombre=datos.nombre.strip(),
            apellido=datos.apellido.strip(),
            telefono=datos.telefono,
            email=datos.email.strip(),
            direccion=datos.direccion,
            notas=datos.notas
        )
        db.session.add(nuevo_cliente)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Cliente guardado con éxito",
            "client": nuevo_cliente.to_dict()
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"status": "error", "message": "Este email ya está registrado"}), 409
    except Exception:
        db.session.rollback()
        logger.exception("Error al crear cliente")
        return jsonify({"status": "error", "message": "No se pudo guardar el cliente"}), 500
