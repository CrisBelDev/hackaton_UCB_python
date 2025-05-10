#include "BluetoothSerial.h" // Biblioteca para Bluetooth en ESP32

BluetoothSerial SerialBT; // Objeto para comunicación Bluetooth

// Variables
int PulseSensorPurplePin = 4; // Pulse Sensor PURPLE WIRE connected to ANALOG PIN 0
int LED = 2;                  // The on-board Arduino LED

int pulse;
int Signal;                // holds the incoming raw data. Signal value can range from 0-1024
int Threshold = 1937;      // Determine which Signal to "count as a beat", and which to ignore

unsigned long previousMillis = 0;  // Variable para almacenar el tiempo anterior
const unsigned long interval = 5000;  // Intervalo de 5 segundos (en milisegundos)

void setup() {
  pinMode(LED, OUTPUT);         // pin that will blink to your heartbeat!
  SerialBT.begin("ESP32_Pulse"); // Configurar Bluetooth con el nombre "ESP32_Pulse"
  Serial.begin(115200);         // Configurar comunicación Serial
  
  Serial.println("Bluetooth iniciado. Esperando conexión...");
}

void loop() {
  Signal = analogRead(PulseSensorPurplePin); // Leer el valor del sensor de pulso

  if (Signal < Threshold) {
    digitalWrite(LED, LOW); // Apagar LED si la señal está por debajo del umbral
    pulse = pulse + 1;      // Incrementar el contador de pulsos
  } else {
    digitalWrite(LED, HIGH); // Encender LED si la señal está por encima del umbral
  }

  unsigned long currentMillis = millis(); // Obtener el tiempo actual

  // Verificar si han pasado 5 segundos
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis; // Actualizar el tiempo anterior
    Serial.print("Pulsos en 5 segundos: ");
    Serial.println(pulse * 2); // Mostrar el valor de "pulse" en el monitor serial
    pulse = 0;                 // Reiniciar la variable "pulse"
  }

  // Verificar si hay datos recibidos por Bluetooth
  if (SerialBT.available()) {
    String request = SerialBT.readString(); // Leer solicitud desde Bluetooth
    request.trim(); // Eliminar espacios en blanco

    if (request == "GET_PULSE") { 
        Serial.println("Solicitud GET_PULSE recibida");
        String pulseData = String(pulse * 2); // Crear la cadena
        pulseData.trim(); // Aplicar trim() a la cadena
        SerialBT.println(pulseData); // Enviar la cadena por Bluetooth
    }
  }

  delay(50);
}