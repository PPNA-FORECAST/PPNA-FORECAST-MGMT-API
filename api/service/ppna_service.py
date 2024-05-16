from api.model.ppna import Ppna
from werkzeug.exceptions import NotFound, BadRequest, Unauthorized

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

        if not points_in_polygon:
            raise NotFound("No Points found in the User Geometry.")
        else:
            return points_in_polygon
        
    @staticmethod
    def get_area(geometry):	

        #geometry = Ppna.correct_coordinate_order(geometry) 
        geometry = Ppna.close_polygon(geometry)

        if not geometry:
            raise BadRequest("No se proporcionó la geometría del usuario")

        area = Ppna.get_area(geometry)

        return area
    
    @staticmethod
    def get_unique_points(geometry):
        
        geometry = Ppna.correct_coordinate_order(geometry)
        geometry = Ppna.close_polygon(geometry)
        
        if not geometry:
            raise BadRequest("No se proporcionó la geometría del usuario")

        if not isinstance(geometry, list):
            raise ValueError("Polygon coordinates must be a list")
        
        unique_points = Ppna.get_unique_points(geometry)
        unique_points = Ppna.correct_coordinate_order(unique_points)
        
        if not unique_points:
            raise NotFound("No Points found in the User Geometry.")
        else:
            return unique_points