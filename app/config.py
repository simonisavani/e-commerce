import os
from pymongo import MongoClient

CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_URL": "redis://localhost:6379/0"
}
CELERY_BROKER_URL = 'redis://localhost:6379/0'
# Load Environment Variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/ecom_db")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey")

# MongoDB Connection
client = MongoClient(MONGO_URI)
db = client.ecom_db
