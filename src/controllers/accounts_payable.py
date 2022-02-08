import json
import logging
from datetime import date
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flasgger import swag_from

from ..constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from ..constants.api_route import API_MAIN_ROUTE
from ..domains.companies import Company
from ..services.accounts_payable_service import AccountsPayableService, AccountsPayableServiceException

accounts_payable_api = Blueprint('accountspayable', __name__, url_prefix=API_MAIN_ROUTE)
logger = logging.getLogger(__name__)
apayable_service = AccountsPayableService()

@accounts_payable_api.route('/accountspayable', methods= ["POST"])
@jwt_required()
@swag_from('../swagger/accountspayable.yaml')
def make_transaction():
    logger.debug('start make_transaction')

    user_id = get_jwt_identity()
    logger.debug(f'logged user_id: {user_id}')

    try:
        movement_date = date.today()
        company_id=request.json['company_id']
        supplier_id = request.json['supplier_id']
        document_number = request.json['document_number']
        rule_id=request.json['rule_id']
        amount = request.json['amount']
        issue_date = request.json['issue_date']
        due_date = request.json['due_date']
        reference = request.json['reference']
        user_id = user_id

        data = apayable_service.make_transaction(movement_date, company_id, supplier_id, document_number, rule_id, amount, issue_date, due_date, reference, user_id)

        logger.debug('finish make_transaction')
        return jsonify({
            'movement': data.jsonObject()
        }), HTTP_200_OK
    except KeyError as errorKeyError:
        logger.debug(f'Error: {errorKeyError.__str__()}')
        return jsonify({
            'message': f'Please check the input data: {errorKeyError.__str__()}'
        }), HTTP_400_BAD_REQUEST
    except AccountsPayableServiceException as compSerExpto:
        logger.debug(f'Error: {compSerExpto.code}, {compSerExpto.message}')
        return jsonify({
            'message': compSerExpto.message,
            'code': compSerExpto.code
        }), HTTP_400_BAD_REQUEST

