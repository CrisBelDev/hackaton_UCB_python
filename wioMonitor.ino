#include <TFT_eSPI.h> // Librería para la pantalla de la Wio Terminal

#define HEARTBEAT_SENSOR_PIN A0 // Pin analógico para el sensor de ritmo cardíaco
#define TEMP_SENSOR_PIN A7      // Pin analógico para el sensor de temperatura
#define LED_PIN 1               // Pin digital para el LED

TFT_eSPI tft = TFT_eSPI(); // Inicialización de la pantalla

// Variables para el gráfico del ritmo cardíaco
int x = 0;
int lastx = 0;
int lasty = 0;

// Variables para el cálculo de BPM
int LastTime = 0;
bool BPMTiming = false;
bool BeatComplete = false;
int BPM = 0;

// Umbrales para detección de latidos
#define UpperThreshold 524
#define LowerThreshold 500

// Variables para el gráfico de temperatura
int tempX = 0;
int lastTempX = 0;
int lastTempY = 0;

// Variable para almacenar la temperatura
float tempC = 0.0;

void setup() {
  pinMode(LED_PIN, OUTPUT); // Configurar el pin del LED como salida
  tft.begin();
  tft.setRotation(3); // Ajustar la orientación de la pantalla
  tft.fillScreen(TFT_BLACK);
  tft.setTextSize(2);
  tft.setTextColor(TFT_WHITE, TFT_BLACK);

  Serial.begin(9600); // Configurar el puerto serial para depuración
}

void loop() {
  // --- Gráfico de ritmo cardíaco ---
  if (x > 127) {
    tft.fillScreen(TFT_BLACK);
    x = 0;
    lastx = x;
  }

  int value = analogRead(HEARTBEAT_SENSOR_PIN);
  int y = 60 - (value / 16);

  // Dibujar línea en la pantalla para el ritmo cardíaco
  tft.drawLine(lastx, lasty, x, y, TFT_WHITE);
  lasty = y;
  lastx = x;

  // Calcular BPM
  if (value > UpperThreshold) {
    digitalWrite(LED_PIN, HIGH); // Encender el LED cuando se detecta un latido
    if (BeatComplete) {
      BPM = millis() - LastTime;
      BPM = int(60 / (float(BPM) / 1000));
      BPMTiming = false;
      BeatComplete = false;
    }
    if (BPMTiming == false) {
      LastTime = millis();
      BPMTiming = true;
    }
  } else {
    digitalWrite(LED_PIN, LOW); // Apagar el LED si no hay latido
  }

  if ((value < LowerThreshold) && BPMTiming) {
    BeatComplete = true;
  }

  // Mostrar BPM en la pantalla
  tft.fillRect(0, 50, 128, 16, TFT_BLACK);
  tft.setCursor(0, 50);
  tft.print(BPM);
  tft.print(" BPM");

  x++;

  // --- Gráfico de temperatura ---
  if (tempX > 127) {
    tft.fillRect(0, 120, 128, 60, TFT_BLACK); // Limpiar área del gráfico de temperatura
    tempX = 0;
    lastTempX = tempX;
  }

  // Leer valor actual del sensor de temperatura
  int tempValue = analogRead(TEMP_SENSOR_PIN);

  // Calcular la temperatura en grados Celsius usando la fórmula para el LM35
  tempC = (5.0 * tempValue * 100.0) / 1024.0;

  // Convertir la temperatura en coordenadas para el gráfico
  int tempY = 180 - (int(tempC) * 2); // Escalar la temperatura para el gráfico

  // Dibujar línea en la pantalla para la temperatura
  tft.drawLine(lastTempX, lastTempY, tempX, tempY, TFT_RED);
  lastTempY = tempY;
  lastTempX = tempX;

  // Mostrar temperatura en la pantalla
  tft.fillRect(0, 100, 128, 16, TFT_BLACK);
  tft.setCursor(0, 100);
  tft.print(tempC, 1);
  tft.print(" C");

  // Enviar temperatura al puerto serial
  Serial.print("Temperatura: ");
  Serial.print(tempC);
  Serial.println(" C");

  tempX++;
  delay(200); // Frecuencia de muestreo: 20 Hz
}