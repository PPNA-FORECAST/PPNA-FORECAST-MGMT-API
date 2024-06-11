import hashlib
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import jsonify 
from werkzeug.exceptions import NotFound, Forbidden, Conflict, Unauthorized, BadRequest


from api.model.user import User

class UserService:
	@staticmethod
	def create_user(username, email, password, geometry):
		encrypted_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
		new_user = User(username, email, encrypted_password, geometry)
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

	@staticmethod
	def get_user_attributes(email):
		user = UserService.get_user(email)
		
		username = user['username']
		mail = user['email']
		
		geometry = []
		for point in user['geometry']:
			if point and len(point) == 2: # Validate if the point is not empty
				processed_point = {"latitude": point[0], "longitude": point[1]}
				geometry.append(processed_point)
				
		return username, mail, geometry

