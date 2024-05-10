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
            
            #view how to sort the points to be util for the model
            #points_in_polygon_sorted = sorted(points_in_polygon, key=lambda x: datetime.strptime(x.get('date'), '%Y-%m-%d'))

            return points_in_polygon
            
        except OperationFailure as e:
            # Handle specific errors from MongoDB
            print(f"Error de operación: {e}")
            raise
    
        except Exception as e:
            print(f"Error inesperado: {e}")
            raise

    #calculate the area of the polygon 
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