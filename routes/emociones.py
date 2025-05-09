from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from controllers.emociones_controller import procesar_emocion, listar_emociones
from database.mongo import emotion_col
from datetime import datetime

emociones_router = APIRouter()

# Endpoint para analizar emoción desde imagen (NO guarda en BD)
@emociones_router.post("/analizar")
async def analizar(file: UploadFile = File(...)):
    return await procesar_emocion(file)

# Endpoint para obtener todas las emociones guardadas
@emociones_router.get("/emociones")
async def obtener_emociones():
    return await listar_emociones()

# Modelo de entrada para guardar emoción
class EmocionEntrada(BaseModel):
    emocion: str

# Nuevo endpoint: guardar emoción dominante manualmente
@emociones_router.post("/guardar_emocion")
async def guardar_emocion(data: EmocionEntrada):
    try:
        doc = {
            "emocion": data.emocion,
            "timestamp": datetime.utcnow()
        }
        emotion_col.insert_one(doc)
        return {"status": "guardado", "emocion": data.emocion}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
