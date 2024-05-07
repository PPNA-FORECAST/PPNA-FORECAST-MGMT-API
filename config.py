from pymongo.errors import PyMongoError
from pymongo import MongoClient
from dotenv import load_dotenv
import os

### Environment variables 
load_dotenv()

### Mongo DB Configuration
MONGO_HOST = 'db'
MONGO_PORT = 27017
MONGO_DB = os.environ.get('MONGO_DATABASE')
MONGO_USERNAME = os.environ.get('MONGO_ROOT_USERNAME')
MONGO_PASSWORD = os.environ.get('MONGO_ROOT_PASSWORD')

client = MongoClient(host=MONGO_HOST, port=MONGO_PORT, username=MONGO_USERNAME, password=MONGO_PASSWORD)
db = client[MONGO_DB]