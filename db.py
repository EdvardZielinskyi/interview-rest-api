import os

from pymongo import MongoClient
from dotenv import load_dotenv
import app


load_dotenv()
client = MongoClient(os.environ.get("MONGODB_URI"))
app.db = client.interview_db
interview_collection = app.db.interviews