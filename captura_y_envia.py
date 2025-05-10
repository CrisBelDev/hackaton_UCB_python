import cv2
import time
import requests
import socket  # Para comunicación Bluetooth
from collections import Counter


IP_BACKEND_LOCAL_MACHINE = "127.0.0.1"
IP_BACKEND_LOCAL_REMOTE_MACHINE = "192.168.75.93"
IP_BACKEND = ""

validacion = False

if (validacion):
    IP_BACKEND = IP_BACKEND_LOCAL_MACHINE
else:
    IP_BACKEND = IP_BACKEND_LOCAL_REMOTE_MACHINE




#API_ANALIZAR = f"http://{IP_BACKEND}:8000/api/analizar"
# Endpoints
API_ANALIZAR = f"http://{IP_BACKEND}:8000/analizar"
API_GUARDAR = f"http://{IP_BACKEND}:8000/guardar_emocion"
API_PROCESAR_BMP = f"http://{IP_BACKEND}:8000/datosmart"

# Configuración de Bluetooth
ESP32_MAC = "A0:B7:65:28:C4:DE"  # Cambia esto por la dirección MAC de tu ESP32
ESP32_PORT = 1  # Canal predeterminado para RFCOMM

try:
    # Crear socket Bluetooth
    bt_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    bt_socket.connect((ESP32_MAC, ESP32_PORT))
    print("✅ Conexión Bluetooth establecida")
except Exception as e:
    print(f"❌ No se pudo conectar al Bluetooth: {e}")
    exit()

# Inicializar la cámara (0 es la cámara por defecto)
cam = cv2.VideoCapture(0)

# Verificar que la cámara se abrió correctamente
if not cam.isOpened():
    print("❌ No se pudo acceder a la cámara")
    exit()

# Variables para controlar tiempo y emociones
emociones = []
ritmoCardiaco = []
emocionRitmoCardiaco = ""
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

        # Solicitar datos de pulso al ESP32
        try:
            bt_socket.send(b"GET_PULSE\n")  # Enviar solicitud
            time.sleep(2)  # Ajustar tiempo de espera
            pulse_data = bt_socket.recv(1024).decode().strip()  # Leer respuesta
            if pulse_data:
                print(f"💓 Pulso recibido desde ESP32: {pulse_data}")
                ritmoCardiaco.append(pulse_data)
            else:
                print("⚠️ No se recibieron datos del ESP32")
        except Exception as e:
            print(f"❌ Error en comunicación Bluetooth: {e}")

        # Si han pasado 60 segundos, guardar la emoción dominante
        if time.time() - start_time >= 60:
            if ritmoCardiaco:
                # Enviar datos de pulso a la API
                try:
                    emocionRitmoCardiaco = requests.post(API_PROCESAR_BMP, json={"ritmoCardiaco": ritmoCardiaco})
                    print("📥 Datos de pulso guardados:", res.json())
                except Exception as e:
                    print("❌ Error al guardar datos de pulso:", e)

            if emociones:
                dominante = Counter(emociones).most_common(1)[0][0]
                data = emocionRitmoCardiaco.json()
                emocionCardio = data.get("emocion")
                print(f"💾 Emoción dominante biometrica en 60s: {dominante}")
                print(f"💾 Emoción dominante fisiologica en 60s: {emocionCardio}")

                # Enviar a la API de guardado
                try:
                    res = requests.post(API_GUARDAR, json={"emocion": dominante, "emocionCardio": emocionCardio})
                    print("📥 Emoción guardada:", res.json())
                except Exception as e:
                    print("❌ Error al guardar en BD:", e)


            # Reiniciar acumulador y tiempo
            emociones = []
            ritmoCardiaco = []
            start_time = time.time()

        # Esperar 5 segundos antes de la siguiente captura
        time.sleep(5)

except KeyboardInterrupt:
    print("🛑 Detenido por el usuario")

finally:
    cam.release()
    cv2.destroyAllWindows()
    bt_socket.close()