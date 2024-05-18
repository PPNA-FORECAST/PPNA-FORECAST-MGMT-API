from werkzeug.exceptions import NotFound, Forbidden, Conflict, Unauthorized, BadRequest
from config import db 

class User:

    def __init__(self, email, password, geometry):
        self.email = email
        self.password = password
        self.geometry = geometry

    def save(self):
        user_collection = db["user"]
        existing_user = user_collection.find_one({"email": self.email})
        if existing_user:
            raise Conflict("User already exists.")
        else:
            user_collection.insert_one(self.__dict__)

    @staticmethod
    def find_by_email(email):
        user_collection = db["user"]
        return user_collection.find_one({"email": email})
    
    def __repr__(self):
        return f'{{"username": "{self.username}", "email": "{self.email}"}}'

    def json(self):
        return{'username': self.username, 'email': self.email}
   