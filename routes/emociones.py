# routes/emociones.py
from fastapi import Request

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
<<<<<<< HEAD
from controllers.emociones_controller import procesar_emocion, listar_emociones, procesar_datosmart
from database.mongo import emotion_col
=======
from controllers.emociones_controller import procesar_emocion, listar_emociones, procesar_ritmo_cardiaco	
from database.mongo import emotion_col, pulse_col  # Asegúrate de tener una colección para los datos de pulso
>>>>>>> b09e32d21b10781e50f777d3c3d176f8920849f0
from datetime import datetime

emociones_router = APIRouter()

# Endpoint para analizar emoción desde imagen (NO guarda en BD)
@emociones_router.post("/analizar")
async def analizar(file: UploadFile = File(...)):
    return await procesar_emocion(file)

# Modelo de entrada para los datos de ritmo cardíaco
class RitmoCardiacoEntrada(BaseModel):
    ritmoCardiaco: list[int]  # Lista de enteros que representan los datos de pulso

# Endpoint para procesar y guardar datos de ritmo cardíaco
@emociones_router.post("/datosmart")
async def procesar_datos_ritmo(data: RitmoCardiacoEntrada):
    try:
        resultado = await procesar_ritmo_cardiaco(data.ritmoCardiaco)
        return resultado
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)



# Endpoint para obtener todas las emociones guardadas
@emociones_router.get("/emociones")
async def obtener_emociones():
    return await listar_emociones()


# Endpoint para obtener los datos del reloj
@emociones_router.post("/datosmart")
async def registrar_datosmart(request: Request):
    return await procesar_datosmart(request)

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