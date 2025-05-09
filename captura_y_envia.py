import cv2
import time
import requests

# URL de tu API
API_URL = "http://127.0.0.1:8000/analizar"

# Inicializar la cámara (0 es la cámara por defecto)
cam = cv2.VideoCapture(0)

# Verifica si la cámara se abrió correctamente
if not cam.isOpened():
    print("❌ No se pudo acceder a la cámara")
    exit()

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

        # Enviar a la API
        with open(img_path, "rb") as f:
            files = {"file": ("temp.jpg", f, "image/jpeg")}
            try:
                response = requests.post(API_URL, files=files)
                print("✅ Respuesta de la API:", response.json())
            except Exception as e:
                print("❌ Error al conectar con la API:", e)

        # Esperar 5 segundos antes de la siguiente captura
        time.sleep(5)

except KeyboardInterrupt:
    print("🛑 Detenido por el usuario")

finally:
    cam.release()
    cv2.destroyAllWindows()
