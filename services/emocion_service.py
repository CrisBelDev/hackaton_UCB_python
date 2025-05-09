import cv2
import numpy as np
import mediapipe as mp
from deepface import DeepFace
from database.mongo import emotion_col
from datetime import datetime

async def analizar_emocion(file):
    contents = await file.read()
    np_img = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    # Detección de rostro con MediaPipe
    mp_face = mp.solutions.face_detection
    with mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5) as detector:
        results = detector.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if not results.detections:
            return {"error": "No se detectó rostro"}

    # Análisis con DeepFace
    result = DeepFace.analyze(img_path=img, actions=['emotion'], enforce_detection=False)
    emocion = result[0]['dominant_emotion']
    timestamp = datetime.utcnow()

    # Guardar en MongoDB
    emotion_col.insert_one({
        "emocion": emocion,
        "timestamp": timestamp
    })

    # Devolver la respuesta
    return {
        "emocion": emocion,
        "timestamp": str(timestamp)
    }


async def obtener_emociones():
    emociones = []
    for doc in emotion_col.find():  # <- cambio importante
        doc["_id"] = str(doc["_id"])
        doc["timestamp"] = str(doc["timestamp"])
        emociones.append(doc)
    return emociones
