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
    """ 
    def get_points():
        ppna_collection = db["ppna"]
        ppna_point = ppna_collection.count_documents({})

        return ppna_point
