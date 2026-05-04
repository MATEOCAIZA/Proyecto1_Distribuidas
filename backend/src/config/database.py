from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["chatapp"]

# Colecciones
rooms_collection    = db["rooms"]
messages_collection = db["messages"]
