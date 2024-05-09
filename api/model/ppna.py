from werkzeug.exceptions import NotFound, Forbidden, Conflict, Unauthorized, BadRequest
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
        ppna_collection.create_index([("location", "2dsphere")])

        # Create a GEOJson polygon with the user data
        polygon_geojson = {
            "type": "Polygon",
            "coordinates": [polygon_coordinates],
        }

        all_points = list(ppna_collection.find({}))
        print("Todos los puntos:", all_points)  # Verificar si la lista está vacía o tiene puntos

        # Ahora puedes continuar con tu lógica de filtrado
        if len(all_points) == 0:
            print("La colección está vacía.")
        # Get points inside polygon
        points_in_polygon = list(
            ppna_collection.find(
                {"location": {"$geoWithin": {"$geometry": polygon_geojson}}}
            )
        )
        print("Points in polygon:", points_in_polygon) # Para chequear si está cargando bien los puntos
        return points_in_polygon

    def close_polygon(points):
        if points[0] != points[-1]: 
            points.append(points[0])  # Adds first coordinate to last to close the polygon
        return points
