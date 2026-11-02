from flask import Blueprint, jsonify

import container
from services.products import ProductService

products_bp = Blueprint('products_api', __name__)


@products_bp.route('', methods=['GET'], strict_slashes=False)
def list_products():
    return jsonify([p.model_dump() for p in container.product_service().list_active()])


@products_bp.route('/promos', methods=['GET'])
def list_promos():
    return jsonify([p.model_dump() for p in container.product_service().list_promos()])


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    return jsonify(container.product_service().get(product_id).model_dump())
