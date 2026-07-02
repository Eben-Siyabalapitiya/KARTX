#include <Adafruit_GFX.h>
#include <Adafruit_ST7735.h>
#include <SPI.h>

#define TFT_CS  15
#define TFT_DC   2
#define TFT_RST  4
#define SCREEN_W 160
#define SCREEN_H 128

Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_RST);

#define C_BG      0x0841
#define C_WHITE   0xFFFF
#define C_GREEN   0x07E0
#define C_CYAN    0x07FF
#define C_MGRAY   0x4208
#define C_DGRAY   0x2104

String inputString = "";

void drawBase() {
  tft.fillScreen(C_BG);

  // title
  tft.setTextColor(C_CYAN);
  tft.setTextSize(2);
  tft.setCursor(50, 8);
  tft.print("KART");

  // divider
  tft.drawFastHLine(0, 28, SCREEN_W, C_DGRAY);

  // labels
  tft.setTextSize(1);
  tft.setTextColor(C_MGRAY);
  tft.setCursor(8, 40);
  tft.print("Subtotal");
  tft.setCursor(8, 60);
  tft.print("HST 13%");
  tft.drawFastHLine(0, 78, SCREEN_W, C_DGRAY);
  tft.setCursor(8, 90);
  tft.setTextColor(C_WHITE);
  tft.print("TOTAL");
}

void updateValues(String subtotal, String tax, String total) {
  // clear value areas
  tft.fillRect(80, 36, 76, 12, C_BG);
  tft.fillRect(80, 56, 76, 12, C_BG);
  tft.fillRect(80, 86, 76, 16, C_BG);

  tft.setTextSize(1);
  tft.setTextColor(C_WHITE);
  tft.setCursor(82, 40);
  tft.print("$"); tft.print(subtotal);

  tft.setCursor(82, 60);
  tft.print("$"); tft.print(tax);

  tft.setTextSize(2);
  tft.setTextColor(C_GREEN);
  tft.setCursor(82, 88);
  tft.print("$"); tft.print(total);
}

void setup() {
  Serial.begin(9600);
  tft.initR(INITR_BLACKTAB);
  tft.setRotation(3);
  tft.fillScreen(C_BG);
  drawBase();
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      int first = inputString.indexOf(',');
      int second = inputString.lastIndexOf(',');
      String subtotal = inputString.substring(0, first);
      String tax = inputString.substring(first + 1, second);
      String total = inputString.substring(second + 1);
      updateValues(subtotal, tax, total);
      inputString = "";
    } else {
      inputString += c;
    }
  }
}