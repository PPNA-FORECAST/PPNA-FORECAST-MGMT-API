from pymongo.errors import PyMongoError
from pymongo import MongoClient

### Mongo DB Configuration
MONGO_HOST = 'mongodb'
MONGO_PORT = 27017
MONGO_DB = 'ppna_forecast_db'

client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
db = client[MONGO_DB]


