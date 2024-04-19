import hashlib
import datetime
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from werkzeug.exceptions import NotFound
from api.errors.errors import *

app = Flask(__name__)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'aa2233'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)


#database connect
MONGO_HOST = 'mongodb'
MONGO_PORT = 27017
MONGO_DB = 'ppna_forecast_db'
MONGO_USER = 'root'
MONGO_PASS = 'root'

client = MongoClient(host=MONGO_HOST,
                     port=MONGO_PORT)

db = client[MONGO_DB]

users_collection = db["users"]

#Register error handler functions for HTTP errors
app.register_error_handler(404, handle_not_found_error)


@app.route("/")
def home():
	return "Mensaje de bienvenida de la api"

@app.route("/api/v1/users", methods=["POST"])
def register():
	new_user = request.get_json() # store the json body request
	new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest() # encrpt passwords
	doc = users_collection.find_one({"username": new_user["username"]}) # check if user exist
	if not doc:
		users_collection.insert_one(new_user)
		return jsonify({'msg': 'User created successfully'}), 201
	else:
		return jsonify({'msg': 'Username already exists'}), 409

@app.route("/api/v1/login", methods=["POST"])
def login():
	login_details = request.get_json() # store the json body request
	user_from_db = users_collection.find_one({'username': login_details['username']})  # search for user in database

	if user_from_db:
		encrpted_password = hashlib.sha256(login_details['password'].encode("utf-8")).hexdigest()
		if encrpted_password == user_from_db['password']:
			access_token = create_access_token(identity=user_from_db['username']) # create jwt token
			return jsonify(access_token=access_token), 200

	return jsonify({'msg': 'The username or password is incorrect'}), 401

@app.route("/api/v1/user", methods=["GET"])
@jwt_required
def profile():
	current_user = get_jwt_identity() # Get the identity of the current user
	user_from_db = users_collection.find_one({'username' : current_user})
	if user_from_db:
		del user_from_db['_id'], user_from_db['password'] # delete data we don't want to return
		return jsonify({'profile' : user_from_db }), 200
	else:
		return jsonify({'msg': 'Profile not found'}), 404

@app.route("/api/v1/user/<username>", methods=["DELETE"]) #Deletes a user
@jwt_required
def delete_user(username):
    current_user = get_jwt_identity()
    user_from_db = users_collection.find_one({'username': current_user})
    if not user_from_db or user_from_db['role'] != 'admin':
        return jsonify({'msg': 'You are not authorized to perform this action'}), 403
    else:
        try:
            user_to_delete = users_collection.find_one({"username": username}) # Check if user to be deleted is in the database
            if not user_to_delete:
                raise NotFound('User not found')  # Raise a NotFound exception
            users_collection.delete_one({"username": username})
            return jsonify({'msg': 'User successfully deleted!'}), 200
        except NotFound as e:
            return handle_not_found_error(e)
        
@app.route("/api/v1/user/<username>/password", methods=["PATCH"]) # Updates user password
@jwt_required
def update_password(username):
    current_user = get_jwt_identity()
    if current_user != username: # If the user trying to change the password is not themselves, they must have admin privileges
        user_from_db = users_collection.find_one({'username': current_user})
        if not user_from_db or user_from_db['role'] != 'admin':
            return jsonify({'msg': 'You are not authorized to perform this action'}), 401

    update_data = request.get_json()
    new_password = update_data.get('password') # Get new password data from the request
    if not new_password:
        return jsonify({'msg': 'New password required'}), 400

    user_to_update = users_collection.find_one({"username": username}) # Find user in database
    if not user_to_update:
        return jsonify({'msg': 'User not found'}), 404
    users_collection.update_one({"username": username}, {"$set": {"password": hashlib.sha256(new_password.encode("utf-8")).hexdigest()}})
    return jsonify({'msg': 'Password successfully updated!'}), 200




if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True) #check 0.0.0.0