import json
import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from ..constants.api_route import API_MAIN_ROUTE
from ..domains.rules import Rule
from ..services.rules_service import RulesService, RulesServiceException

rules_api = Blueprint('rules', __name__, url_prefix=API_MAIN_ROUTE)
logger = logging.getLogger(__name__)
rules_service = RulesService()

@rules_api.route('/rule', methods= ["POST"])
@jwt_required()
def create_rule():
    logger.debug("create_rule")

    try:
        rule_description=request.json['rule_description']
        action_over_document=request.json['action_over_document']
        movement_type=request.json['movement_type']
        update_issue_date=request.json['update_issue_date']
        update_due_date=request.json['update_due_date']
        update_reference=request.json['update_reference']

        try:
            newComp = rules_service.create_rule(rule_description=rule_description, action_over_document=action_over_document, movement_type=movement_type, update_issue_date=update_issue_date, update_due_date=update_due_date, update_reference=update_reference)
            if newComp is None:
                return jsonify({
                    'message': "Bad request"
                }), HTTP_400_BAD_REQUEST
            else:
                return jsonify({
                    'message': "Rule created",
                    'rule': newComp.jsonObject()
                }), HTTP_201_CREATED
        except RulesServiceException as compSerExpto:
            logger.debug(f'Error: {compSerExpto.code}, {compSerExpto.message}')
            return jsonify({
                'message': compSerExpto.message,
                'code': compSerExpto.code
            }), HTTP_400_BAD_REQUEST
    except KeyError as errorKeyError:
        logger.debug(f'Error: {errorKeyError.__str__()}')
        return jsonify({
            'message': f'Please check the input data: {errorKeyError.__str__()}'
        }), HTTP_400_BAD_REQUEST

@rules_api.route('/rule', methods= ["GET"])
@jwt_required()
def get_all_rules():
    logger.debug("get_all_rules")

    data = []
    rules = rules_service.get_all()
    for rule in rules:
        data.append(rule.jsonObject())

    return jsonify({'rules': data}), HTTP_200_OK

@rules_api.route('/rule/<int:id>', methods= ["GET"])
@jwt_required()
def get_rule_by_id(id):
    logger.debug(f'get_rule_by_id: {id}')

    try:
        rule = rules_service.get_rule_by_id(id=id)
        if rule is None:
            return jsonify({
                'message': "Rule not found"
            }), HTTP_404_NOT_FOUND
        else:
            logger.debug(f'rule: {rule.jsonObject()}')
            return jsonify({
                'rule': rule.jsonObject()
            }), HTTP_200_OK
    except RulesServiceException as compSerExpto:
        logger.debug(f'Error: {compSerExpto.code}, {compSerExpto.message}')
        return jsonify({
            'message': compSerExpto.message,
            'code': compSerExpto.code
        }), HTTP_404_NOT_FOUND

@rules_api.route('/rule/<int:id>', methods= ["PUT"])
@jwt_required()
def update_rule_by_id(id):
    logger.debug(f'update_rule_by_id: {id}')

    try:
        rule_description=request.json['rule_description']
        action_over_document=request.json['action_over_document']
        movement_type=request.json['movement_type']
        update_issue_date=request.json['update_issue_date']
        update_due_date=request.json['update_due_date']
        update_reference=request.json['update_reference']

        try:
            rule = rules_service.update_rule(id=id, rule_description=rule_description, action_over_document=action_over_document, movement_type=movement_type, update_issue_date=update_issue_date, update_due_date=update_due_date, update_reference=update_reference)
            if rule is None:
                return jsonify({
                    'message': "Rule not found"
                }), HTTP_404_NOT_FOUND
            else:
                return jsonify({
                    'rule': rule.jsonObject()
                }), HTTP_200_OK
        except RulesServiceException as compSerExpto:
            logger.debug(f'Error: {compSerExpto.code}, {compSerExpto.message}')
            return jsonify({
                'message': compSerExpto.message,
                'code': compSerExpto.code
            }), HTTP_400_BAD_REQUEST
    except KeyError as errorKeyError:
        logger.debug(f'Error: {errorKeyError.__str__()}')
        return jsonify({
            'message': f'Please check the input data: {errorKeyError.__str__()}'
        }), HTTP_400_BAD_REQUEST

@rules_api.route('/rule/<int:id>', methods= ["DELETE"])
@jwt_required()
def delete_rule_by_id(id):
    logger.debug(f'update_rule_by_id: {id}')

    try:
        if rules_service.delete_rule(id=id):
            return jsonify({
                'message': "Rule was deleted"
            }), HTTP_200_OK
        else:
            return jsonify({
                'message': "Rule not found"
            }), HTTP_404_NOT_FOUND

    except RulesServiceException as compSerExpto:
        logger.debug(f'Error: {compSerExpto.code}, {compSerExpto.message}')
        return jsonify({
            'message': compSerExpto.message,
            'code': compSerExpto.code
        }), HTTP_404_NOT_FOUND

