from fastapi.responses import JSONResponse
from fastapi import UploadFile, File
from services.emocion_service import analizar_emocion, obtener_emociones, procesar_ritmo
from models.emocion_model import Emocion

# Procesar imagen y devolver emoción detectada (sin guardar)
async def procesar_emocion(file: UploadFile = File(...)):
    try:
        resultado = await analizar_emocion(file)
        return Emocion(**resultado)  # Estructura según modelo Pydantic
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Obtener todas las emociones guardadas en MongoDB
async def listar_emociones():
    try:
        return await obtener_emociones()
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Procesar datos de ritmo cardíaco
async def procesar_ritmo_cardiaco(ritmo_cardiaco: list[int]):
    try:
        return await procesar_ritmo(ritmo_cardiaco)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)