from werkzeug.exceptions import NotFound, Forbidden, Conflict, Unauthorized, BadRequest
from pymongo.errors import OperationFailure
from config import db 

class Ppna:

    @staticmethod
    def get_points(polygon_coordinates):

        ppna_collection = db["ppna"]
        ppna_collection.create_index([("location", "2dsphere")], unique=False)

        # Create a GEOJson polygon with the user data
        polygon_geojson = {
            "type": "Polygon",
            "coordinates": [polygon_coordinates],
        }
        # Get points inside polygon
        try:
            points_in_polygon = list(
                ppna_collection.find(
                    {"location": {"$geoWithin": {"$geometry": polygon_geojson}}},
                    {"_id": 0, "ppna": 1, "temp": 1, "ppt": 1, "date": 1, "latitude": 1, "longitude": 1}
                )
            )
            return points_in_polygon
            
        except OperationFailure as e:
            # Handle specific errors from MongoDB
            print(f"Error de operación: {e}")
            raise
    
        except Exception as e:
            print(f"Error inesperado: {e}")
            raise

    # Necesary because GeoJson use a closed polygon
    def close_polygon(points):
        if points[0] != points[-1]: 
            points.append(points[0])  # Adds first coordinate to last to close the polygon
        return points

    # Change coordinate order [latitude, longitude] to [longitude, latitude] (necesary because the frontend use one format and backend the other)
    def correct_coordinate_order(coordinates):
        return [[point[1], point[0]] for point in coordinates]
