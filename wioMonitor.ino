#include <TFT_eSPI.h> // Librería para la pantalla de la Wio Terminal

TFT_eSPI tft = TFT_eSPI(); // Inicialización de la pantalla

// Variables para graficar
int x = 0;
int lastX = 0;
int lastY = 0;

// Variables para almacenar datos recibidos
int ritmoCardiaco = 0;
String emocion = "";

void setup() {
  tft.begin();
  tft.setRotation(3); // Ajustar la orientación de la pantalla
  tft.fillScreen(TFT_BLACK);
  tft.setTextSize(2);
  tft.setTextColor(TFT_WHITE, TFT_BLACK);

  Serial.begin(9600); // Configurar el puerto serial para recibir datos
}

void loop() {
  // Leer datos del puerto serial
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n'); // Leer hasta el carácter de nueva línea
    int commaIndex = data.indexOf(',');
    if (commaIndex > 0) {
      // Separar ritmo cardíaco y emoción
      ritmoCardiaco = data.substring(0, commaIndex).toInt();
      emocion = data.substring(commaIndex + 1);
    }
  }

  // Graficar ritmo cardíaco
  if (x > 127) {
    tft.fillScreen(TFT_BLACK);
    x = 0;
    lastX = 0;
  }

  int y = 60 - (ritmoCardiaco / 2); // Escalar el ritmo cardíaco para el gráfico
  tft.drawLine(lastX, lastY, x, y, TFT_WHITE);
  lastY = y;
  lastX = x;

  // Mostrar ritmo cardíaco y emoción en la pantalla
  tft.fillRect(0, 70, 128, 16, TFT_BLACK);
  tft.setCursor(0, 70);
  tft.print("RC: ");
  tft.print(ritmoCardiaco);
  tft.print(" BPM");

  tft.fillRect(0, 90, 128, 16, TFT_BLACK);
  tft.setCursor(0, 90);
  tft.print("Emocion: ");
  tft.print(emocion);

  x++;
  delay(200); // Frecuencia de actualización
}