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

        points_in_polygon = PpnaService.group_by_location(points_in_polygon)

        print(points_in_polygon)
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
        

     
    #Toma un input de puntos con todas las caracteristicas (ppna, temp, ppt, ...) y
    # devuelve {location:[lat:xx,long:yy,sample:[date:a, ppna:1], ..], ..} para cada punto. 
    @staticmethod
    def group_by_location(points):
        points_dict = {}

        # Procesar cada punto y agruparlo según las coordenadas
        for point in points:
            coords = (point["latitude"], point["longitude"])
            if coords not in points_dict:
                points_dict[coords] = {"latitude": point["latitude"], "longitude": point["longitude"], "data": []}
            points_dict[coords]["data"].append({"date": point["date"], "temp":point["temp"], "ppt":point["ppt"], "ppna": point["ppna"]})

        # Convertir el diccionario en el formato deseado
        formatted_points = [{"location": {"latitude": coord[0], "longitude": coord[1], "sample": points_dict[coord]["data"]}} for coord in points_dict]
        
        return formatted_points
