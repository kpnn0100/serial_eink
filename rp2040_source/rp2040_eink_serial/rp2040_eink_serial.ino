//#include <SPI.h>
#include "epd2in9_V2.h"
#include "epdpaint.h"
#include "imagedata.h"
#include "dos_protocol.h"
#define COLORED     0
#define UNCOLORED   1

/**
  * Due to RAM not enough in Arduino UNO, a frame buffer is not allowed.
  * In this case, a smaller image buffer is allocated and you have to 
  * update a partial display several times.
  * 1 byte = 8 pixels, therefore you have to set 8*N pixels at a time.
  */
unsigned char image[1024];
const int buffer_size = EPD_WIDTH*EPD_HEIGHT/8;
unsigned char input_image_data[buffer_size];
Paint paint(image, 0, 0);    // width should be the multiple of 8 
Epd epd;
unsigned long time_start_ms;
unsigned long time_now_s;
byte screenSize[] = {EPD_WIDTH >> 8,EPD_WIDTH & 0x00ff, EPD_HEIGHT>> 8,EPD_HEIGHT & 0x00ff};
void setup() {
  // put your setup code here, to run once:
  Serial.begin(4000000);
  Serial.println("init");
  if (epd.Init() != 0) {
      Serial.print("e-Paper init failed ");
      return;
  }
  epd.SetFrameMemory_Base(IMAGE_DATA);
  epd.DisplayFrame();

  time_start_ms = millis();
}
void sendResponse(byte cmdType, byte cmdCode, uint16_t len, byte *data) {
  Serial.write(cmdType);
  Serial.write(cmdCode);  // Response has no specific command code
  Serial.write(len>>8);  // Response data length is 0
  Serial.write(len & 0x00ff);
  Serial.write(data, len );
}
void handleRequest(byte commandType, byte commandCode, int dataLength, byte* data) {
  switch (commandCode) {
    case CMD_CODE_SCREEN_INFO:
      // Process screen information request
      // For demonstration, assume a vertical orientation, width = 128, height = 64

      sendResponse(CMD_TYPE_RESPONSE,CMD_CODE_SCREEN_INFO,0x04,screenSize);  // Success
      break;

    case CMD_CODE_CHANGE_IMAGE:
    {
      int min_length = buffer_size;
      if (dataLength<buffer_size) min_length = dataLength;
      memcpy(input_image_data,data,min_length);
      epd.SetFrameMemory_Partial(input_image_data,0,0,EPD_WIDTH,EPD_HEIGHT);
      sendResponse(CMD_TYPE_RESPONSE,CMD_CODE_CHANGE_IMAGE, 0x01, {0x00});
      break;
    }

    case CMD_CODE_DISPLAY_IMAGE:
    {
      epd.DisplayFrame_Partial();
      sendResponse(CMD_TYPE_RESPONSE,CMD_CODE_DISPLAY_IMAGE, 0x01, {0x00});
      break;
    }
    default:
      break;
  }
}
void loop() {
    if (Serial.available() >= 3) {  // Ensure at least one complete message is available
    byte commandType = Serial.read();
    byte commandCode = Serial.read();
    byte dataLengthBytes[2];
    Serial.readBytes(dataLengthBytes, 2);
    int dataLength = (dataLengthBytes[0] << 8) | dataLengthBytes[1];

    byte data[dataLength];
    Serial.readBytes(data, dataLength);
    if (commandType == CMD_TYPE_REQUEST) {
      handleRequest(commandType, commandCode, dataLength, data);
    }
  }
  // delay(300);
}
