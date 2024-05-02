import hashlib
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import jsonify 
from werkzeug.exceptions import NotFound, Forbidden, Conflict, Unauthorized, BadRequest


from api.model.user import User

class UserService:
	@staticmethod
	def create_user(email, password, datapoints):
		encrypted_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
		new_user = User(email, encrypted_password, datapoints)
		new_user.save()
		return new_user

	@staticmethod
	def login_user(email, password):
		
		user_from_db = User.find_by_email(email)

		if user_from_db:
			encrypted_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
			if encrypted_password == user_from_db['password']:
				access_token = create_access_token(identity=user_from_db['email']) # create jwt token
				return access_token

		raise Unauthorized('The email or password is incorrect')
	
	@staticmethod
	def get_user(email):
		
		user_from_db = User.find_by_email(email)

		if user_from_db:
			return user_from_db
		else:
			raise NotFound('Profile not found')

