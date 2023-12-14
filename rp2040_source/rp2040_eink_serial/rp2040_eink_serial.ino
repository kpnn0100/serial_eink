//#include <SPI.h>
#include "epd2in9_V2.h"
#include "epdpaint.h"
#include "imagedata.h"

#define COLORED     0
#define UNCOLORED   1

/**
  * Due to RAM not enough in Arduino UNO, a frame buffer is not allowed.
  * In this case, a smaller image buffer is allocated and you have to 
  * update a partial display several times.
  * 1 byte = 8 pixels, therefore you have to set 8*N pixels at a time.
  */
unsigned char image[1024];
Paint paint(image, 0, 0);    // width should be the multiple of 8 
Epd epd;
unsigned long time_start_ms;
unsigned long time_now_s;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("init");
  if (epd.Init() != 0) {
      Serial.print("e-Paper init failed ");
      return;
  }
   epd.ClearFrameMemory(0xFF);   // bit set = white, bit reset = black
  epd.DisplayFrame();
  epd.SetFrameMemory_Base(IMAGE_DATA);
  epd.DisplayFrame();

  time_start_ms = millis();
}

void loop() {
  Serial.print
  
  // delay(300);
}
