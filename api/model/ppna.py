from werkzeug.exceptions import NotFound, Forbidden, Conflict, Unauthorized, BadRequest
from pymongo.errors import OperationFailure
from config import db 
from area import area


class Ppna:

    @staticmethod
    def get_points(geometry):

        ppna_collection = db["ppna"]
        ppna_collection.create_index([("location", "2dsphere")], unique=False)

        # Create a GEOJson polygon with the user data
        polygon_geojson = {
            "type": "Polygon",
            "coordinates": [geometry],
        }
        # Get points inside polygon
        try:
            points_in_polygon = list(
                ppna_collection.find(
                    {"location": {"$geoWithin": {"$geometry": polygon_geojson}}},
                    {"_id": 0, "ppna": 1, "temp": 1, "ppt": 1, "date": 1, "latitude": 1, "longitude": 1}
                )
            )
            
            #Check how to sort the points to be util for the model
            #points_in_polygon_sorted = sorted(points_in_polygon, key=lambda x: datetime.strptime(x.get('date'), '%Y-%m-%d'))

            return points_in_polygon
            
        except OperationFailure as e:
            # Handle specific errors from MongoDB
            print(f"Error de operación: {e}")
            raise
    
        except Exception as e:
            print(f"Error inesperado: {e}")
            raise

    #calculate the area of the polygon in square meters
    def get_area(geometry):     
        polygon_geojson = Ppna.points_to_geoJson(geometry)
        geometry_area = area(polygon_geojson)
        return geometry_area

    # Necesary because GeoJson use a closed polygon
    def close_polygon(geometry):
        if geometry[0] != geometry[-1]: 
            geometry.append(geometry[0])  # Adds first coordinate to last to close the polygon
        return geometry

    # Change coordinate order [latitude, longitude] to [longitude, latitude] (necesary because the frontend use one format and backend the other)
    def correct_coordinate_order(geometry):
        return [[point[1], point[0]] for point in geometry]

    #recieve a list of latitude and longitude and return geoJson
    def points_to_geoJson(geometry):

        polygon_geojson = {
            "type": "Polygon",
            "coordinates": [geometry],
        }

        return polygon_geojson
    
    @staticmethod
    def get_locations(geometry):
        
        ppna_collection = db["ppna"]
        ppna_collection.create_index([("location", "2dsphere")], unique=False)

        # Create a GEOJson polygon with the user data
        polygon_geojson = {
            "type": "Polygon",
            "coordinates": [geometry],
        }

        # Get unique latitude and longitude points inside polygon
        try:
            points_in_polygon = list(
                ppna_collection.find(
                    {"location": {"$geoWithin": {"$geometry": polygon_geojson}}},
                    {"_id": 0, "latitude": 1, "longitude": 1}
                )
            )

            # Filter out duplicate points
            unique_points_set = set()
            unique_points = []
            for point in points_in_polygon:
                point_tuple = (point["latitude"], point["longitude"])
                if point_tuple not in unique_points_set:
                    unique_points_set.add(point_tuple)
                    unique_points.append({"latitude": point["latitude"], "longitude": point["longitude"]})
    
            return unique_points

        except OperationFailure as e:
            # Handle specific errors from MongoDB
            print(f"Error de operación: {e}")
            raise

        except Exception as e:
            print(f"Error inesperado: {e}")
            raise

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