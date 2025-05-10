# services/emocion_service
import cv2
import numpy as np
import mediapipe as mp
from deepface import DeepFace
from database.mongo import emotion_col


from datetime import datetime

from openai import OpenAI  # Asegúrate de instalar el SDK: `pip install openai`
from database.mongo import pulse_col

# Configuración del cliente de DeepSeek
client = OpenAI(api_key="sk-1e216daa06464bd584d0f3367144ef2b", base_url="https://api.deepseek.com")

async def procesar_ritmo(ritmo_cardiaco):
    try:
        # Calcular el promedio del ritmo cardíaco
        promedio = sum(ritmo_cardiaco) / len(ritmo_cardiaco)

        # Crear el prompt para DeepSeek
        prompt = f"El ritmo cardíaco promedio es {promedio}. Devuelve el estado de ánimo que representa este valor en una sola palabra."

        # Hacer la solicitud a DeepSeek
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Eres un asistente útil que analiza estados de ánimo."},
                {"role": "user", "content": prompt},
            ],
            stream=False
        )

        # Extraer el estado de ánimo de la respuesta
        estado_animo = response.choices[0].message.content.strip() if response.choices else "Desconocido"

        # Retornar solo el estado de ánimo
        return {
		"emocion": estado_animo,
	    }
    except Exception as e:
        raise Exception(f"Error al procesar los datos de ritmo cardíaco: {str(e)}")

async def analizar_emocion(file):
    contents = await file.read()
    np_img = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    # Detección de rostro con MediaPipe (modelo más preciso)
    mp_face = mp.solutions.face_detection
    with mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.5) as detector:
        results = detector.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if not results.detections:
            return {"error": "No se detectó rostro"}

        # Extraer la primera detección
        detection = results.detections[0]
        bbox = detection.location_data.relative_bounding_box
        h, w, _ = img.shape
        x = int(bbox.xmin * w)
        y = int(bbox.ymin * h)
        width = int(bbox.width * w)
        height = int(bbox.height * h)

        # Validar que esté dentro del rango de la imagen
        x = max(0, x)
        y = max(0, y)
        x2 = min(w, x + width)
        y2 = min(h, y + height)

        # Recortar el rostro
        face_img = img[y:y2, x:x2]

    # Enviar solo el rostro recortado a DeepFace
    try:
        result = DeepFace.analyze(img_path=face_img, actions=['emotion'], enforce_detection=False)
        emocion = result[0]['dominant_emotion']
    except Exception as e:
        return {"error": f"Fallo en DeepFace: {str(e)}"}

    return {
		"emocion": emocion,
		"timestamp": str(datetime.utcnow())
	}


async def obtener_emociones():
    emociones = []
    for doc in emotion_col.find():
        doc["_id"] = str(doc["_id"])
        doc["timestamp"] = str(doc["timestamp"])
        emociones.append(doc)
    return emociones
