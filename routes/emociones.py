from fastapi import APIRouter, UploadFile, File
from controllers.emociones_controller import procesar_emocion, listar_emociones

emociones_router = APIRouter()

@emociones_router.post("/analizar")
async def analizar(file: UploadFile = File(...)):
    return await procesar_emocion(file)



@emociones_router.get("/emociones")
async def obtener_emociones():
    return await listar_emociones()