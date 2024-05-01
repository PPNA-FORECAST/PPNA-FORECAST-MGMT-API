from werkzeug.exceptions import NotFound, Forbidden, Conflict, Unauthorized, BadRequest
from config import db 

class User:

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

    @staticmethod
    def find_by_email(email):
        users_collection = db["users"]
        return users_collection.find_one({"email": email})
    
    def __repr__(self):
        return f'{{"username": "{self.username}", "email": "{self.email}"}}'

    def json(self):
        return{'username': self.username, 'email': self.email}
   