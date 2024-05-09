import jsonschema
from api.schema.user_schema import *
from api.service.user_service import UserService
from flask import Blueprint, request, jsonify
from api.model.ppna import Ppna
from flask_jwt_extended import jwt_required, get_jwt_identity
from jsonschema.exceptions import ValidationError
from werkzeug.exceptions import NotFound, BadRequest, Unauthorized
from shapely.geometry import Point, Polygon
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
    geometry = Ppna.close_polygon(geometry)

    if not geometry:
        raise BadRequest("No se proporcionó la geometría del usuario")

    if not isinstance(geometry, list):
        raise ValueError("Polygon coordinates must be a list")
    
    points_in_polygon = Ppna.get_points(geometry)  

    return jsonify({"locations": points_in_polygon}), 200









# def get_ppna_points():
#     # Obtener la identidad del usuario y sus puntos
#     current_user = get_jwt_identity() 
#     user = UserService.get_user(current_user)

#     if not user:
#         raise NotFound("User not found.")  # If user doesn't exist, raise a 404
    
#     geometry = user.get("datapoints", []) # Get user polygon

#     if not geometry or len(geometry) < 3: # The 3 point minimum is previously validated but it is a countermeassure
#         raise BadRequest("Invalid geometry. A valid polygon requires at least 3 points.")

#     # Obtener todos los puntos para verificar si están dentro del polígono
#     all_points = Ppna.get_points()  # Supongamos que esta función devuelve una lista de puntos
#     # Aplicar la función para obtener los puntos dentro del polígono
#     inside_points = points_in_polygon(all_points, geometry)

#     return jsonify({"locations": inside_points}), 200





# def get_ppna_points():

#     current_user = get_jwt_identity() 
#     user = UserService.get_user(current_user)
#     geometry = user['datapoints']

#     #solo como prueba, aca debeeria buscar los datos que estan dentro de la geometria del usuario 
#     points = Ppna.get_points()

#     if user:
#         return jsonify({"locations":points}), 200
#     else:
#         raise NotFound("User not found.")




# def points_in_polygon(points, polygon_coords):
#     """
#     Return a list of points that are inside the given polygon.
#     """
#     polygon = Polygon(polygon_coords)  # Create a Polygon object from the given coordinates
#     inside_points = []

#     for point_coords in points:
#         point = Point(point_coords)  # Create a Point object from the given coordinates
#         if polygon.contains(point) or polygon.touches(point):  # Check if the point is inside the polygon or at its edge
#             inside_points.append(point_coords)

#     print(inside_points)
#     return inside_points  # Return the list of points inside the polygon
