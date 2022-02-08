import json
import logging
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required
from flasgger import swag_from

from ..constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from ..constants.api_route import API_MAIN_ROUTE
from ..domains.companies import Company
from ..services.companies_service import CompaniesService, CompaniesServiceException

companies_api = Blueprint('companies', __name__, url_prefix=API_MAIN_ROUTE)
logger = logging.getLogger(__name__)
companies_service = CompaniesService()

@companies_api.route('/company', methods= ["POST"])
@jwt_required()
@swag_from('../swagger/company_post.yaml')
def create_company():
    logger.debug("create_company")

    try:
        newComp = companies_service.create_company(business_name=request.json['business_name'])
        return jsonify({
            'message': "Company created",
            'company': {
                'company_id': newComp.company_id,
                'business_name': newComp.business_name
            }
        }), HTTP_201_CREATED
    except CompaniesServiceException as compSerExpto:
        logger.debug(f'Error: {compSerExpto.code}, {compSerExpto.message}')
        return jsonify({
            'message': compSerExpto.message,
            'code': compSerExpto.code
        }), HTTP_400_BAD_REQUEST

@companies_api.route('/company', methods= ["GET"])
@jwt_required()
@swag_from('../swagger/company_get_all.yaml')
def get_all_companies():
    logger.debug("get_all_companies")

    data = []
    companies = companies_service.get_all()
    for company in companies:
        data.append({
            'company_id': company.company_id,
            'business_name': company.business_name
        })

    return jsonify({'companies': data}), HTTP_200_OK

@companies_api.route('/company/<int:id>', methods= ["GET"])
@jwt_required()
@swag_from('../swagger/company_get_one.yaml')
def get_company_by_id(id):
    logger.debug(f'get_company_by_id: {id}')

    try:
        company = companies_service.get_company_by_id(id=id)
        if company is None:
            return jsonify({
                'message': "Company not found"
            }), HTTP_404_NOT_FOUND
        else:
            return jsonify({
                'company': {
                    'company_id': company.company_id,
                    'business_name': company.business_name
                }
            }), HTTP_200_OK
    except CompaniesServiceException as compSerExpto:
        logger.debug(f'Error: {compSerExpto.code}, {compSerExpto.message}')
        return jsonify({
            'message': compSerExpto.message,
            'code': compSerExpto.code
        }), HTTP_404_NOT_FOUND

@companies_api.route('/company/<int:id>', methods= ["PUT"])
@jwt_required()
@swag_from('../swagger/company_put.yaml')
def update_company_by_id(id):
    logger.debug(f'update_company_by_id: {id}')

    try:
        company = companies_service.update_company(id=id, business_name=request.json['business_name'])
        if company is None:
            return jsonify({
                'message': "Company not found"
            }), HTTP_404_NOT_FOUND
        else:
            return jsonify({
                'company': {
                    'company_id': company.company_id,
                    'business_name': company.business_name
                }
            }), HTTP_200_OK
    except CompaniesServiceException as compSerExpto:
        logger.debug(f'Error: {compSerExpto.code}, {compSerExpto.message}')
        return jsonify({
            'message': compSerExpto.message,
            'code': compSerExpto.code
        }), HTTP_400_BAD_REQUEST

@companies_api.route('/company/<int:id>', methods= ["DELETE"])
@jwt_required()
@swag_from('../swagger/company_delete.yaml')
def delete_company_by_id(id):
    logger.debug(f'update_company_by_id: {id}')

    try:
        if companies_service.delete_company(id=id):
            return jsonify({
                'message': "Company was deleted"
            }), HTTP_200_OK
        else:
            return jsonify({
                'message': "Company not found"
            }), HTTP_404_NOT_FOUND

    except CompaniesServiceException as compSerExpto:
        logger.debug(f'Error: {compSerExpto.code}, {compSerExpto.message}')
        return jsonify({
            'message': compSerExpto.message,
            'code': compSerExpto.code
        }), HTTP_404_NOT_FOUND
