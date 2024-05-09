from werkzeug.exceptions import NotFound, Forbidden, Conflict, Unauthorized, BadRequest
from pymongo.errors import OperationFailure
from config import db 

class Ppna:

    """
    def __init__(self, email, password, datapoints):
        self.email = email
        self.password = password
        self.datapoints = datapoints

    def save(self):
        users_collection = db["users"]
        existing_user = users_collection.find_one({"email": self.email})
        if existing_user:
            raise Conflict("User already exists.")
        else:
            users_collection.insert_one(self.__dict__)
    
    def get_points():
        ppna_collection = db["ppna"]
        ppna_point = ppna_collection.count_documents({})

        return ppna_point
    """
    @staticmethod
    def get_points(polygon_coordinates):

        ppna_collection = db["ppna"]
        ppna_collection.create_index([("location", "2dsphere")], unique=False)

        # Create a GEOJson polygon with the user data
        polygon_geojson = {
            "type": "Polygon",
            "coordinates": [polygon_coordinates],
        }

        print("Coordinates:", polygon_coordinates)
        print("Polygon GEOJson:", polygon_geojson)
        # all_points = list(ppna_collection.find({}))
        # print("Todos los puntos:", all_points)  
        # if len(all_points) == 0:
        #     print("La colección está vacía.")

        # Get points inside polygon
        try:
        # Obtener puntos dentro del polígono
            points_in_polygon = list(
                ppna_collection.find(
                    {"location": {"$geoWithin": {"$geometry": polygon_geojson}}}
            )
        )
            print("Puntos en el polígono:", points_in_polygon)
            return points_in_polygon
    
        except OperationFailure as e:
            # Handle specific errors from MongoDB
            print(f"Error de operación: {e}")
            raise
    
        except Exception as e:
            print(f"Error inesperado: {e}")
            raise

    def close_polygon(points):
        if points[0] != points[-1]: 
            points.append(points[0])  # Adds first coordinate to last to close the polygon
        return points

    def correct_coordinate_order(coordinates):
    # Change coordinate order [latitude, longitude] to [longitude, latitude]
        return [[point[1], point[0]] for point in coordinates]
