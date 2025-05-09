import cv2
import time
import requests
from collections import Counter

# Endpoints
API_ANALIZAR = "http://127.0.0.1:8000/analizar"
API_GUARDAR = "http://127.0.0.1:8000/guardar_emocion"

# Inicializar la cámara (0 es la cámara por defecto)
cam = cv2.VideoCapture(0)

# Verificar que la cámara se abrió correctamente
if not cam.isOpened():
    print("❌ No se pudo acceder a la cámara")
    exit()

# Variables para controlar tiempo y emociones
emociones = []
start_time = time.time()

try:
    while True:
        # Leer un frame de la cámara
        ret, frame = cam.read()
        if not ret:
            print("❌ No se pudo capturar imagen")
            break

        # Guardar imagen temporalmente
        img_path = "temp.jpg"
        cv2.imwrite(img_path, frame)

        # Enviar imagen a la API para análisis (sin guardar en Mongo)
        with open(img_path, "rb") as f:
            files = {"file": ("temp.jpg", f, "image/jpeg")}
            try:
                response = requests.post(API_ANALIZAR, files=files)
                data = response.json()
                emocion = data.get("emocion")
                if emocion:
                    emociones.append(emocion)
                    print(f"🧠 Emoción detectada: {emocion}")
                else:
                    print("⚠️ No se detectó emoción válida")
            except Exception as e:
                print("❌ Error al conectar con la API:", e)

        # Si han pasado 60 segundos, guardar la emoción dominante
        if time.time() - start_time >= 60:
            if emociones:
                dominante = Counter(emociones).most_common(1)[0][0]
                print(f"💾 Emoción dominante en 60s: {dominante}")

                # Enviar a la API de guardado
                try:
                    res = requests.post(API_GUARDAR, json={"emocion": dominante})
                    print("📥 Emoción guardada:", res.json())
                except Exception as e:
                    print("❌ Error al guardar en BD:", e)

            # Reiniciar acumulador y tiempo
            emociones = []
            start_time = time.time()

        # Esperar 5 segundos antes de la siguiente captura
        time.sleep(5)

except KeyboardInterrupt:
    print("🛑 Detenido por el usuario")

finally:
    cam.release()
    cv2.destroyAllWindows()
