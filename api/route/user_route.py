import jsonschema
from api.schema.user_schema import *
from flask import Blueprint, request, jsonify
from api.service.user_service import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity
from jsonschema.exceptions import ValidationError
from werkzeug.exceptions import NotFound, BadRequest, Unauthorized

from api.errors.errors import *

user_bp = Blueprint('user', __name__)

@user_bp.route("/api/v1/user/register", methods=["POST"])
def create_user():

    user_data = request.get_json()

    try:    
        jsonschema.validate(user_data, user_register_schema)
    except ValidationError as ve:  
        return handle_bad_request_error(ve) # Raises 400 error
    
    try:
        new_user = UserService.create_user(**user_data)
        return jsonify({"msg": "User created successfully"}), 201
    except Exception as e:  
        return handle_generic_error(e)

@user_bp.route("/api/v1/user/login", methods=["POST"])
def login_user(): 
    user_data = request.get_json()

    try:    
        jsonschema.validate(user_data, user_login_schema)
    except ValidationError as ve:
        return handle_bad_request_error(ve)
    
    try:
        token = UserService.login_user(**user_data)
        return jsonify({"access_token": token}), 200
    except Exception as e:
        return handle_generic_error(e)
    

@user_bp.route("/api/v1/user", methods=["GET"])
@jwt_required()
def get_user(): 
    current_user = get_jwt_identity()
    mail, geometry = UserService.get_user_attributes(current_user)
    
    return jsonify({"email":mail, "geometry":geometry}), 200


@user_bp.route("/api/v1/user/check-email", methods=["POST"])
def check_email():
    email_data = request.get_json()
    
    if 'email' not in email_data:
        return handle_bad_request_error("Email is required")
    
    email = email_data['email']
    
    try:
        user = UserService.get_user(email)
        if user:
            return handle_conflict_error("User already exists.")
    except NotFound:
        return jsonify({"msg": "Email is available"}), 200
    except Exception as e:
        return handle_generic_error(e)
