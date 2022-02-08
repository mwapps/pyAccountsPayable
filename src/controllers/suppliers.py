import json
import logging
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required
from ..constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from flasgger import swag_from

from ..constants.api_route import API_MAIN_ROUTE
from ..domains.suppliers import Supplier
from ..services.suppliers_service import SuppliersService, SuppliersServiceException

suppliers_api = Blueprint('suppliers', __name__, url_prefix=API_MAIN_ROUTE)
logger = logging.getLogger(__name__)
suppliers_service = SuppliersService()

@suppliers_api.route('/supplier', methods= ["POST"])
@jwt_required()
@swag_from('../swagger/supplier_post.yaml')
def create_supplier():
    logger.debug("create_supplier")

    try:
        newComp = suppliers_service.create_supplier(supplier_name=request.json['supplier_name'])
        return jsonify({
            'message': "Supplier created",
            'supplier': {
                'supplier_id': newComp.supplier_id,
                'supplier_name': newComp.supplier_name
            }
        }), HTTP_201_CREATED
    except SuppliersServiceException as compSerExpto:
        logger.debug(f'Error: {compSerExpto.code}, {compSerExpto.message}')
        return jsonify({
            'message': compSerExpto.message,
            'code': compSerExpto.code
        }), HTTP_400_BAD_REQUEST

@suppliers_api.route('/supplier', methods= ["GET"])
@jwt_required()
@swag_from('../swagger/supplier_get_all.yaml')
def get_all_suppliers():
    logger.debug("get_all_suppliers")

    data = []
    suppliers = suppliers_service.get_all()
    for supplier in suppliers:
        data.append({
            'supplier_id': supplier.supplier_id,
            'supplier_name': supplier.supplier_name
        })

    return jsonify({'suppliers': data}), HTTP_200_OK

@suppliers_api.route('/supplier/<int:id>', methods= ["GET"])
@jwt_required()
@swag_from('../swagger/supplier_get_one.yaml')
def get_supplier_by_id(id):
    logger.debug(f'get_supplier_by_id: {id}')

    try:
        supplier = suppliers_service.get_supplier_by_id(id=id)
        if supplier is None:
            return jsonify({
                'message': "Supplier not found"
            }), HTTP_404_NOT_FOUND
        else:
            return jsonify({
                'supplier': {
                    'supplier_id': supplier.supplier_id,
                    'supplier_name': supplier.supplier_name
                }
            }), HTTP_200_OK
    except SuppliersServiceException as compSerExpto:
        logger.debug(f'Error: {compSerExpto.code}, {compSerExpto.message}')
        return jsonify({
            'message': compSerExpto.message,
            'code': compSerExpto.code
        }), HTTP_404_NOT_FOUND

@suppliers_api.route('/supplier/<int:id>', methods= ["PUT"])
@jwt_required()
@swag_from('../swagger/supplier_put.yaml')
def update_supplier_by_id(id):
    logger.debug(f'update_supplier_by_id: {id}')

    try:
        supplier = suppliers_service.update_supplier(id=id, supplier_name=request.json['supplier_name'])
        if supplier is None:
            return jsonify({
                'message': "Supplier not found"
            }), HTTP_404_NOT_FOUND
        else:
            return jsonify({
                'supplier': {
                    'supplier_id': supplier.supplier_id,
                    'supplier_name': supplier.supplier_name
                }
            }), HTTP_200_OK
    except SuppliersServiceException as compSerExpto:
        logger.debug(f'Error: {compSerExpto.code}, {compSerExpto.message}')
        return jsonify({
            'message': compSerExpto.message,
            'code': compSerExpto.code
        }), HTTP_400_BAD_REQUEST

@suppliers_api.route('/supplier/<int:id>', methods= ["DELETE"])
@jwt_required()
@swag_from('../swagger/supplier_delete.yaml')
def delete_supplier_by_id(id):
    logger.debug(f'update_supplier_by_id: {id}')

    try:
        if suppliers_service.delete_supplier(id=id):
            return jsonify({
                'message': "Supplier was deleted"
            }), HTTP_200_OK
        else:
            return jsonify({
                'message': "Supplier not found"
            }), HTTP_404_NOT_FOUND

    except SuppliersServiceException as compSerExpto:
        logger.debug(f'Error: {compSerExpto.code}, {compSerExpto.message}')
        return jsonify({
            'message': compSerExpto.message,
            'code': compSerExpto.code
        }), HTTP_404_NOT_FOUND
