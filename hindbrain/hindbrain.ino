/*
   Navig8r Hind brain

   Runs hardware interfaces
   Takes serial commands from the fore brain

*/

#include <Adafruit_NeoPixel.h>

// Pin definitions
#define FLASH_PIN_LEFT    2
#define FLASH_PIN_RIGHT   3
#define NEOPIXEL_PIN      6

// Forebrain definitions
#define NONE              0
#define LEFT              1
#define RIGHT             2

#define NEAR              1  // m
#define FAR               2  // m
#define OUT_OF_RANGE      0

bool enable_flash = false;
short direction = NONE;
int distance = 0;

// Flash definitions
// Assume 50% duty cycle
#define FLASH_MS          500   // ms

unsigned long last_flash_pulse = 0;
bool flash_state = false;

// Neopixel definitions
#define PIXELS            16
#define NEOPIXEL_NEAR     75  // ms
#define NEOPIXEL_FAR      200  // ms

#define ON_COLOR_R        25
#define ON_COLOR_G        25
#define ON_COLOR_B        0
#define OFF_COLOR_R       7
#define OFF_COLOR_G       5
#define OFF_COLOR_B       7

Adafruit_NeoPixel neopixel(PIXELS, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);

short pixel_index = 0;
unsigned long last_pixel_pulse = 0;

void setup() {
  Serial.begin(9600);
  // Hardware setup
  pinMode(FLASH_PIN_LEFT, OUTPUT);
  pinMode(FLASH_PIN_RIGHT, OUTPUT);

  // Neopixel initialization
  neopixel.begin();
}

void loop() {
  // Read when available
  readForeBrain();

  // Non blocking functions
  updateFlash();
  updateNeoPixels();
  delay(10);
  digitalWrite(13, direction == LEFT);
}

void readForeBrain() {
  if (Serial.available() > 0) {
    // read the incoming byte:
    byte byte1 = Serial.read();

    // say what you got:
    //    Serial.print("Byte1: ");
    //    Serial.println(byte1, BIN);

    if (byte1 == 36) {
      // byte2
      while (Serial.available() == 0) {}
      int byte2 = Serial.read();

      if (byte2 == 90) {
        direction = NONE;
      } else if (byte2 == 76) {
        direction = LEFT;
      } else if (byte2 == 82) {
        direction = RIGHT;
      }

      // byte3
      while (Serial.available() == 0) {}

      byte byte3 = Serial.read();
      enable_flash = (byte3 == 70);

      // byte4
      while (Serial.available() == 0) {}
      byte byte4 = Serial.read();
      if (byte4 == 78) {
        distance = NEAR;
      } else if (byte4 == 70) {
        distance = FAR;
      } else {
        distance = OUT_OF_RANGE;
      }
    }
  }
}


void updateFlash() {
  // Flash the specified flashlight at specified frequency
  unsigned long current_time = millis();
  if (distance == NEAR && current_time > last_flash_pulse + FLASH_MS) {
    flash_state = !flash_state;
    last_flash_pulse = current_time;
  } else if (distance == FAR) {
    flash_state = true;
  } else {
    flash_state = false;
  }

  if (!enable_flash) {
    digitalWrite(FLASH_PIN_LEFT, LOW);
    digitalWrite(FLASH_PIN_RIGHT, LOW);
  } else if (distance != OUT_OF_RANGE) {
    if (direction == LEFT) {
      digitalWrite(FLASH_PIN_LEFT, flash_state);
      digitalWrite(FLASH_PIN_RIGHT, false);
    } else if (direction == RIGHT) {
      digitalWrite(FLASH_PIN_LEFT, false);
      digitalWrite(FLASH_PIN_RIGHT, flash_state);
    }
  }
}

void updateNeoPixels() {
  // Run chase pattern in specified direction and frequency
  unsigned long current_time = millis();
  int neopixel_time = 0;
  if (distance == FAR) {
    neopixel_time = NEOPIXEL_FAR;
  } else if (distance == NEAR) {
    neopixel_time = NEOPIXEL_NEAR;
  }
  if (neopixel_time != 0 && current_time > last_pixel_pulse + neopixel_time) {
    pixel_index = ((pixel_index + 1) % (PIXELS / 2));
    last_pixel_pulse = current_time;
  }

  if (direction == LEFT) {
    for (int i = 0; i < PIXELS; i++) {
      if ((i >= PIXELS / 2 - (pixel_index+1)) && (i < PIXELS / 2)) {
        neopixel.setPixelColor(i, neopixel.Color(ON_COLOR_R, ON_COLOR_G, ON_COLOR_B));
      } else {
        neopixel.setPixelColor(i, neopixel.Color(OFF_COLOR_R, OFF_COLOR_G, OFF_COLOR_B));
      }
    }
  } else if (direction == RIGHT) {
    for (int i = 0; i < PIXELS; i++) {
      if ((i <= PIXELS / 2 + pixel_index) && (i >= PIXELS / 2)) {
        neopixel.setPixelColor(i, neopixel.Color(ON_COLOR_R, ON_COLOR_G, ON_COLOR_B));
      } else {
        neopixel.setPixelColor(i, neopixel.Color(OFF_COLOR_R, OFF_COLOR_G, OFF_COLOR_B));
      }
    }
  } else {
    for (int i = 0; i < PIXELS; i++) {
      neopixel.setPixelColor(i, neopixel.Color(OFF_COLOR_R, OFF_COLOR_G, OFF_COLOR_B));
    }
  }

  neopixel.show();
}
