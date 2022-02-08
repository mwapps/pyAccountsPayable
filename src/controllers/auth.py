import validators
import logging
from flask import Blueprint, app, request, jsonify
from flask_jwt_extended import get_jwt, set_access_cookies, jwt_required, create_access_token, create_refresh_token, get_jwt_identity, unset_jwt_cookies
from flasgger import swag_from

from ..domains.users import User
from ..constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT, HTTP_404_NOT_FOUND
from ..constants.api_route import API_MAIN_ROUTE
from ..services.users_service import UsersService, UsersServiceException

auth = Blueprint("auth", __name__, url_prefix=API_MAIN_ROUTE+"/auth")
logger = logging.getLogger(__name__)

users_service = UsersService()

@auth.route('/user', methods= ["POST"])
@swag_from('../swagger/auth_post.yaml')
def create_new_user():
    logger.debug('start create_new_user')

    try:
        newUser = users_service.create_user(request.json['username'], request.json['email'], request.json['password'])
        return jsonify({
            'message': "User created",
            'user': {
                'username': newUser.user_name,
                'email': newUser.user_email
            }
        }), HTTP_201_CREATED
    except UsersServiceException as userSerExpto:
        return jsonify({
            'message': userSerExpto.message,
            'code': userSerExpto.code
        }), HTTP_400_BAD_REQUEST


@auth.route('/login', methods= ["POST"])
@swag_from('../swagger/auth_login.yaml')
def login():
    logger.debug('start login')

    try:
        user = users_service.login_user(email=request.json.get('email', ''), password=request.json.get('password', ''))

        logger.debug(f'the user_name: {user.user_name} and the id is {user.user_id}')

        refresh = create_refresh_token(identity=user.user_id)
        access = create_access_token(identity=user.user_id)

        return jsonify({
            'user': {
                'refresh': refresh,
                'access': access,
                'username': user.user_name,
                'email': user.user_email
            }

        }), HTTP_200_OK
    except UsersServiceException as userSerExpto:
        logger.debug(f'bad credentials: {userSerExpto.code}, {userSerExpto.message}')
        return jsonify({
            'message': userSerExpto.message,
            'code': userSerExpto.code
        }), HTTP_401_UNAUTHORIZED

@auth.route("/user", methods=["DELETE"])
@jwt_required()
@swag_from('../swagger/auth_delete.yaml')
def delete_user():
    logger.debug('start delete_user')
    email = request.json['email']

    try:
        user = users_service.delete_user(email=request.json.get('email', ''))
        return jsonify({
            'message': "The user was deleted",
        }), HTTP_200_OK
    except UsersServiceException as userSerExpto:
        logger.debug(f'Error: {userSerExpto.code}, {userSerExpto.message}')
        return jsonify({
            'message': userSerExpto.message,
            'code': userSerExpto.code
        }), HTTP_404_NOT_FOUND


@auth.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    logger.debug("logout")
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

@auth.route("/me", methods= ["GET"])
@jwt_required()
@swag_from('../swagger/auth_me.yaml')
def me():
    user_id = get_jwt_identity()
    logger.debug(f'logged user_id: {user_id}')

    user = users_service.get_user_by_id(user_id)

    return jsonify({
	    'username': user.user_name,
	    'email': user.user_email
    }), HTTP_200_OK

@auth.route("/me/reset_password", methods= ["POST"])
@jwt_required()
@swag_from('../swagger/auth_reset_password.yaml')
def reset_password():
    user_id = get_jwt_identity()
    logger.debug(f'logged user_id: {user_id}')

    try:
        users_service.reset_password(user_id=user_id, old_password=request.json.get('old_password', ''), new_password=request.json.get('new_password', ''))
        return jsonify({
            'message': "Password was changed",
        }), HTTP_200_OK
    except UsersServiceException as userSerExpto:
        logger.debug(f'Error: {userSerExpto.code}, {userSerExpto.message}')
        return jsonify({
            'message': userSerExpto.message,
            'code': userSerExpto.code
        }), HTTP_401_UNAUTHORIZED

@auth.route('/token/refresh', methods= ["POST"])
@jwt_required(refresh=True)
@swag_from('../swagger/auth_me_refresh.yaml')
def refresh_users_token():
    identity = get_jwt_identity()
    logger.debug(f'logged user_id: {identity}')
    access = create_access_token(identity=identity)

    return jsonify({
        'access': access
    }), HTTP_200_OK
