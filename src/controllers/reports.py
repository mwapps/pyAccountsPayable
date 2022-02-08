import json
import logging
from datetime import date
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flasgger import swag_from

from ..constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from ..constants.api_route import API_MAIN_ROUTE
from ..domains.companies import Company
from ..services.reports_service import ReportsService, ReportsServiceException
from flasgger import swag_from


report_api = Blueprint('report', __name__, url_prefix=API_MAIN_ROUTE+'/report')
logger = logging.getLogger(__name__)
reports_service = ReportsService()

@report_api.route('/documents', methods= ["GET"])
@jwt_required()
@swag_from('../swagger/reports_documents.yaml')
def process_documents_reports():
    logger.debug('start process_documents_reports')

    args = request.args

    user_id = get_jwt_identity()
    logger.debug(f'logged user_id: {user_id}')

    try:
        data = []
        documents = reports_service.process_documents_reports(company_id=args.get("company_id"), supplier_id=args.get("supplier_id"), document_number=args.get("document_number"), from_date=args.get("from_date"), to_date=args.get("to_date"))
        if documents is not None:
            data = list(map(lambda theDocument: theDocument.jsonObject(), documents))

        logger.debug('finish process_documents_reports')
        return jsonify({
            'documents': data
        }), HTTP_200_OK
    except KeyError as errorKeyError:
        logger.debug(f'Error: {errorKeyError.__str__()}')
        return jsonify({
            'message': f'Please check the input data: {errorKeyError.__str__()}'
        }), HTTP_400_BAD_REQUEST
    except ReportsServiceException as compSerExpto:
        logger.debug(f'Error: {compSerExpto.code}, {compSerExpto.message}')
        return jsonify({
            'message': compSerExpto.message,
            'code': compSerExpto.code
        }), HTTP_400_BAD_REQUEST

@report_api.route('/movements', methods= ["GET"])
@jwt_required()
@swag_from('../swagger/reports_movements.yaml')
def process_movements_reports():
    logger.debug('start process_movements_reports')

    args = request.args

    user_id = get_jwt_identity()
    logger.debug(f'logged user_id: {user_id}')

    try:
        data = []
        movements = reports_service.process_movements_reports(company_id=args.get("company_id"), supplier_id=args.get("supplier_id"), document_number=args.get("document_number"), rule_id=args.get("rule_id"), from_date=args.get("from_date"), to_date=args.get("to_date"))
        if movements is not None:
            data = list(map(lambda theDocument: theDocument.jsonObject(), movements))

        logger.debug('finish process_documents_reports')
        return jsonify({
            'movements': data
        }), HTTP_200_OK
    except KeyError as errorKeyError:
        logger.debug(f'Error: {errorKeyError.__str__()}')
        return jsonify({
            'message': f'Please check the input data: {errorKeyError.__str__()}'
        }), HTTP_400_BAD_REQUEST
    except ReportsServiceException as compSerExpto:
        logger.debug(f'Error: {compSerExpto.code}, {compSerExpto.message}')
        return jsonify({
            'message': compSerExpto.message,
            'code': compSerExpto.code
        }), HTTP_400_BAD_REQUEST

