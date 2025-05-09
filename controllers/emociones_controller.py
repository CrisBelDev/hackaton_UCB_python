from fastapi.responses import JSONResponse
from fastapi import APIRouter, UploadFile, File
from services.emocion_service import analizar_emocion
from models.emocion_model import Emocion

emociones_router = APIRouter()

@emociones_router.post("/analizar", response_model=Emocion)
async def procesar_emocion(file: UploadFile = File(...)):
    try:
        
        resultado = await analizar_emocion(file)
        return Emocion(**resultado)  # Uso del modelo Pydantic
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

from services.emocion_service import obtener_emociones

async def listar_emociones():
    try:
        return await obtener_emociones()
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)