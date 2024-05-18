from api.schema.user_schema import *
from api.service.user_service import UserService
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.service.ppna_service import PpnaService
from werkzeug.exceptions import NotFound
from pymongo import MongoClient
from api.model.ppna import Ppna


from api.errors.errors import *

ppna_bp = Blueprint('ppna', __name__)

# Get a user regitrated and return the ppna history and ppna forecast: 
# {points:[lat:mm, long:xx,date:yy, ppna:xx], ...} 
@ppna_bp.route("/api/v1/ppna/points", methods=["GET"])
@jwt_required()
def get_ppna_points():
    current_user = get_jwt_identity()
    user = UserService.get_user(current_user)
    
    if not user:
        raise NotFound("User not found.")
    
    geometry = user.get("geometry")  # User polygon
    
    points = PpnaService.get_points(geometry)
    
    return jsonify({"points": points}), 200


#Get a geography and return all the locations inside the geography and the total area of the geography. 
#{area:xx , locations: [latitude:mm, longitude:xx], ...}  and the total area 
@ppna_bp.route("/api/v1/ppna/locations", methods=["GET"])
def calculate_polygon():

    data = request.json

    if not data or not isinstance(data, list):
        return jsonify({"error": "Invalid input data. A list of coordinates is expected."}), 400

    
    polygon_area = PpnaService.get_area(data)
    locations = PpnaService.get_locations(data)

    return jsonify({"area": polygon_area, "locations": locations }), 200