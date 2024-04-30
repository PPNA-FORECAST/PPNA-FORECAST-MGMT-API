####### IMPORTS ####### 
import os
import hashlib
import datetime

#FLASK 
from flask import Flask, request, jsonify, Flask, redirect, url_for, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from requests_oauthlib import OAuth2Session

#MONGO 
from pymongo import MongoClient
from pymongo.errors import PyMongoError

#ERRORS 
from werkzeug.exceptions import NotFound, Forbidden, Conflict, Unauthorized, BadRequest
from flask_cors import CORS
from api.errors.errors import *
#######################


######## APLICATION ###### 
app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}}) # Allows request from different origins (API and app are not running on the same domain or port)


### Security Configuration (put in another place) ###

#JWT
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'aa2233'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

#OAUTH
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['SECRET_KEY'] = 'your_secret_key'
client_id = '1040272532907-0e5c0mgge5t76m6n2srf40p1tqg52brv.apps.googleusercontent.com'
client_secret = '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'
authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
token_url = 'https://accounts.google.com/o/oauth2/token'
redirect_uri = 'http://127.0.0.1:5000/api/v1/login/callback'
scope = ['profile', 'email', 'openid']
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' #para que me deje usarlo sin HTTPS (no produccion)

#DATABASE
MONGO_HOST = 'mongodb'
MONGO_PORT = 27017
MONGO_DB = 'ppna_forecast_db'
MONGO_USER = 'root'
MONGO_PASS = 'root'

client = MongoClient(host=MONGO_HOST,
                     port=MONGO_PORT)

db = client[MONGO_DB]

users_collection = db["users"]

#ERRORS
app.register_error_handler(409, handle_conflict_error)
app.register_error_handler(404, handle_not_found_error)
app.register_error_handler(403, handle_forbidden_error)
app.register_error_handler(401, handle_unauthorized_error)
app.register_error_handler(400, handle_bad_request_error)


#ENDPOINTS
@app.route("/")
def home():
	return "Mensaje de bienvenida de la api"


@app.route("/api/v1/users", methods=["POST"])
def create_user():
    user_data = request.get_json()  # Get the JSON data from the request

    # Check for required fields
    required_fields = ["username", "user_email", "password", "datapoints"]
    missing_fields = [field for field in required_fields if field not in user_data]

    if missing_fields:
        raise BadRequest(f"Missing fields: {', '.join(missing_fields)}") # Raise a BadRequest (400) exception

    username = user_data["username"]
    user_email = user_data["user_email"]
    password = user_data["password"]
    datapoints = user_data["datapoints"]

    # Validate the data points format (ensure it's a list of coordinates)
    if not isinstance(datapoints, list):
        raise BadRequest("Invalid format for 'datapoints', expected a list of coordinates.") # Raise a BadRequest (400) exception

    # Check if user already exists
    existing_user = users_collection.find_one({"username": username})
    if existing_user:
        raise Conflict("Username already exists.") # Raise a Conflict (409) exception

    # Encrypt the password
    encrypted_password = hashlib.sha256(password.encode("utf-8")).hexdigest()

    # Insert the new user into the database
    new_user = {
        "username": username,
        "user_email": user_email,
        "password": encrypted_password,
        "datapoints": datapoints
    }

    users_collection.insert_one(new_user)

    return jsonify({"msg": "User created successfully"}), 201


# @app.route("/api/v1/users", methods=["POST"]) ENDPOINT REPLACED BY THE ONE ABOVE
# def register():
# 	new_user = request.get_json() # store the json body request
# 	new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest() # encript passwords
# 	doc = users_collection.find_one({"username": new_user["username"]}) # check if user exists
# 	if not doc:
# 		users_collection.insert_one(new_user)
# 		return jsonify({'msg': 'User created successfully'}), 201
# 	else:
# 		raise Conflict('Username already exists')  # Raise a Conflict (409) exception

"""
@app.route("/api/v1/login", methods=["POST"])
def login():
	login_details = request.get_json() # store the json body request
	user_from_db = users_collection.find_one({'user_email': login_details['user_email']})  # search for user in database

	if user_from_db:
		encrpted_password = hashlib.sha256(login_details['password'].encode("utf-8")).hexdigest()
		if encrpted_password == user_from_db['password']:
			access_token = create_access_token(identity=user_from_db['user_email']) # create jwt token
			return jsonify(access_token=access_token), 200

	return Unauthorized('The email or password is incorrect')  # Raise a Unauthorized (401) exception
"""
class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user

@app.route('/api/v1/login')
def login():
    google = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = google.authorization_url(authorization_base_url, access_type='offline', prompt='select_account')
    session['oauth_state'] = state
    #print (state)
    return redirect(authorization_url)

# @app.route('/api/v1/login/callback')
# def callback():
#     google = OAuth2Session(client_id, state=session['oauth_state'], redirect_uri=redirect_uri)
#     token = google.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)
#     #print(token)
#     session['google_token'] = token
#     return redirect(url_for('.home'))

@app.route('/api/v1/login/callback')
def callback():
    google = OAuth2Session(client_id, state=session['oauth_state'], redirect_uri=redirect_uri)
    #token = google.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)

    # Obtener datos del usuario autorizado
    user_info = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
    user_email = user_info['email']

    # Crear un JWT o similar para devolver al frontend
    access_token = create_access_token(identity=user_email)  # Create JWT

    # Retornar el JWT al frontend
    return jsonify({'access_token': access_token})  # Retornar el token en formato JSON

@app.route("/api/v1/user", methods=["GET"])
@jwt_required
def profile():
	current_user = get_jwt_identity() # Get the identity of the current user
	user_from_db = users_collection.find_one({'username' : current_user})
	if user_from_db:
		del user_from_db['_id'], user_from_db['password'] # delete data we don't want to return
		return jsonify({'profile' : user_from_db }), 200
	else:
		raise NotFound('Profile not found')

@app.route('/api/v1/logout')
@login_required
def logout():
    session.pop('google_token', None)
    return redirect(url_for('.index'))


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True) #check 0.0.0.0