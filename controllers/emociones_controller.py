# controller/emociones_controller.py
from fastapi.responses import JSONResponse
from fastapi import UploadFile, File
from services.emocion_service import analizar_emocion, obtener_emociones
from models.emocion_model import Emocion
from fastapi import Request


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


async def procesar_datosmart(request: Request):
    try:
        # Leer los datos enviados en el cuerpo de la solicitud
        datos = await request.json()
        
        # Imprimir los datos en la consola (o usar un logger)
        print("Datos recibidos:", datos)
        
        # Por ahora, solo devolveremos un mensaje de éxito
        return JSONResponse(content={"status": "Datos del reloj procesados correctamente", "datos_recibidos": datos}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)