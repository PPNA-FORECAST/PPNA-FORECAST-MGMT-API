from api.model.ppna import Ppna
from werkzeug.exceptions import NotFound, BadRequest, Unauthorized
import requests
import json
import os


class PpnaService:
    
    @staticmethod
    def get_points(geometry):	

        geometry = Ppna.correct_coordinate_order(geometry) 
        geometry = Ppna.close_polygon(geometry)

        if not geometry:
            raise BadRequest("No se proporcionó la geometría del usuario")

        if not isinstance(geometry, list):
            raise ValueError("Polygon coordinates must be a list")
        
        points_in_polygon = Ppna.get_points(geometry)

        points_in_polygon = Ppna.group_by_location(points_in_polygon)
        
        if not points_in_polygon:
            raise NotFound("No Points found in the User Geometry.")
        else:
            return points_in_polygon
        
    @staticmethod
    def get_area(geometry):	

        geometry = Ppna.correct_coordinate_order(geometry) 
        geometry = Ppna.close_polygon(geometry)

        if not geometry:
            raise BadRequest("No se proporcionó la geometría del usuario")

        area = Ppna.get_area(geometry)

        return area
    
    @staticmethod
    def get_locations(geometry):
        
        geometry = Ppna.correct_coordinate_order(geometry)
        geometry = Ppna.close_polygon(geometry)
        
        if not geometry:
            raise BadRequest("No se proporcionó la geometría del usuario")

        if not isinstance(geometry, list):
            raise ValueError("Polygon coordinates must be a list")
        
        locations = Ppna.get_locations(geometry)
        
        if not locations:
            raise NotFound("No Points found in the User Geometry.")
        else:
            return locations
        
    @staticmethod
    def get_forecast(points, token):
        
        url = os.environ.get('ML_API_URI')
  
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        print(json.dumps(points))
        response = requests.post(url, headers=headers, data=json.dumps(points))

        if response.status_code == 200:
            return response.json()
        else:
            raise BadRequest(f"Error en la solicitud: {response.text}")


