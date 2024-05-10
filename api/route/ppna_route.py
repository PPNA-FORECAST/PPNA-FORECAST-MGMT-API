from api.schema.user_schema import *
from api.service.user_service import UserService
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.model.ppna import Ppna
from werkzeug.exceptions import NotFound
from pymongo import MongoClient


from api.errors.errors import *

ppna_bp = Blueprint('ppna', __name__)

@ppna_bp.route("/api/v1/ppna/points", methods=["GET"])
@jwt_required()
def get_ppna_points():
    current_user = get_jwt_identity()
    user = UserService.get_user(current_user)
    
    if not user:
        raise NotFound("User not found.")
    
    geometry = user.get("datapoints")  # User polygon
    
    points = Ppna.get_points(geometry)

    return jsonify({"locations": points}), 200
