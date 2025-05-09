from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['hackathon']
emotion_col = db['emociones']


# (Opcional) models/emocion_model.py
from pydantic import BaseModel

class Emocion(BaseModel):
    emocion: str
