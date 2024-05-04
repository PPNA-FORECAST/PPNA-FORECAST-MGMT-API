import os
import datetime
from flask import Flask 
from flask_jwt_extended import JWTManager
from api.route.user_route import user_bp
from api.errors.errors import *
from dotenv import load_dotenv
from flask_cors import CORS


app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})  # Permitir solicitudes de cualquier origen
### Environment variables
load_dotenv()

### JWT 
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1) # define the life span of the token
jwt = JWTManager(app)

### Blueprints 
app.register_blueprint(user_bp)

### Errors
app.register_error_handler(400, handle_bad_request_error) 
app.register_error_handler(401, handle_unauthorized_error)
app.register_error_handler(403, handle_forbidden_error)
app.register_error_handler(404, handle_not_found_error)
app.register_error_handler(409, handle_conflict_error)
app.register_error_handler(500, handle_generic_error)




if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)
