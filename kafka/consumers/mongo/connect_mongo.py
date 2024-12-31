from pymongo import MongoClient  # Import MongoDB client


MONGO_URI = "mongodb://mongodb:mongodb@mongo:27017/"  # URI para conectar ao container MongoDB
MONGO_DATABASE = "kafka_data"
MONGO_COLLECTION = "processed_articles"

# MongoDB client setup
client = MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]
collection = db[MONGO_COLLECTION]
