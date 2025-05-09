from pydantic import BaseModel
from datetime import datetime

class Emocion(BaseModel):
    emocion: str
    timestamp: datetime
