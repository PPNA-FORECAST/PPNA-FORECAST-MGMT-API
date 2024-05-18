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
        forecast = PpnaService.get_forecast(points_in_polygon)

        if not forecast:
            raise NotFound("No Points found in the User Geometry.")
        else:
            return forecast
        
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
        

     
    #como todavia no tenemos la api del modelo voy a hacer que este servicio simule el \
    #comportamiento. Basicamente toma un input de puntos con todas las caracteristicas (ppna,
    #temp, ppt, ...) y devuelve {location:[lat:xx,long:yy,sample:[date:a, ppna:1], ..], ..} para cada punto 
    @staticmethod
    def get_forecast(points):

        points_dict = {}

        # Procesar cada punto y agruparlo según las coordenadas
        for point in points:
            coords = (point["latitude"], point["longitude"])
            if coords not in points_dict:
                points_dict[coords] = {"lat": point["latitude"], "long": point["longitude"], "data": []}
            points_dict[coords]["data"].append({"date": point["date"], "ppna": point["ppna"]})

        # Convertir el diccionario en el formato deseado
        formatted_points = [{"location": {"lat": coord[0], "long": coord[1], "sample": points_dict[coord]["data"]}} for coord in points_dict]

        return formatted_points

        