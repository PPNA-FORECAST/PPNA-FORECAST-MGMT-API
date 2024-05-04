import jsonschema
from api.schema.user_schema import *
from api.service.user_service import UserService
from flask import Blueprint, request, jsonify
from api.model.ppna import Ppna
from flask_jwt_extended import jwt_required, get_jwt_identity
from jsonschema.exceptions import ValidationError
from werkzeug.exceptions import NotFound, BadRequest, Unauthorized

from api.errors.errors import *

ppna_bp = Blueprint('ppna', __name__)

@ppna_bp.route("/api/v1/ppna/points", methods=["GET"])
@jwt_required()
def get_ppna_points():

    current_user = get_jwt_identity() 
    user = UserService.get_user(current_user)
    geometry = user['datapoints']

    #solo como prueba, aca debeeria buscar los datos que estan dentro de la geometria del usuario 
    points = Ppna.get_points()

    if user:
        return jsonify({"datapoints":points}), 200
    else:
        raise NotFound("User not found.")


