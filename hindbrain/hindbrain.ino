/*
 * Navig8r Hind brain
 * 
 * Runs hardware interfaces
 * Takes serial commands from the fore brain
 * 
 */sd

#include <Adafruit_NeoPixel.h>

// Pin definitions
#define FLASH_PIN_LEFT    2
#define FLASH_PIN_RIGHT   3
#define NEOPIXEL_PIN      6

// Forebrain definitions
#define NONE              0
#define LEFT              1
#define RIGHT             2

#define NEAR              50  // m
#define FAR               100 // m

bool enable_flash = false;
short direction = NONE;
int distance = 0;

// Flash definitions
// Assume 50% duty cycle
#define FLASH_MS_NEAR     2   // ms
#define FLASH_MS_FAR      0.5 // ms

unsigned long last_flash_pulse = 0;
bool flash_state = false;

// Neopixel definitions
#define PIXELS            16
#define NEOPIXEL_NEAR     100  // ms
#define NEOPIXEL_FAR      500  // ms
Adafruit_NeoPixel neopixel(PIXELS, NEOPIXEL_PIN, NEO_GRB+NEO_KHZ800);

short pixel_index = 0;
unsigned long last_pixel_pulse = 0;

void setup() {
  // Hardware setup
  pinMode(FLASH_PIN_LEFT);
  pinMode(FLASH_PIN_RIGHT);

  // Neopixel initialization
  neopixel.begin();
}

void loop() {
  // Read when available
  readForeBrain();

  // Non blocking functions
  updateFlash();
  updateNeoPixels;
}

void readForeBrain() {
  // TODO jackie's code here
  if (Serial.available() > 0) {
    // read the incoming byte:
    byte1 = Serial.read();

    // say what you got:
    Serial.print("Byte1: ");
    Serial.println(byte1, BIN);

    if (byte1 == 36){
      // byte2
      while (Serial.available() == 0){}
      byte2 = Serial.read();
      
      int left = byte2>>7;
      if (left == 1):
        direction = 1;
      
      int right = byte2>>6 & 01;
      if (right == 1):
        direction = 2;

      int flash = byte2>>5 & 001;
      if (flash == 1):
        enable_flash = true;
      Serial.print("flash: ");
      Serial.println(enable_flash);

      // byte3
      while (Serial.available() == 0){}
      
      byte3 = Serial.read();
      distance = (byte2 & 31) + byte3;
    }
  }
}


void updateFlash() {
  // Flash the specified flashlight at specified frequency
  unsigned long current_time = millis();
  int flash_time = 0;
  if (distance <= FAR) {
    flash_time = FLASH_MS_NEAR;
  } else if (distance <= NEAR) {
    flash_time = FLASH_MS_FAR;
  }
  if (flash_time != 0 && current_time > last_flash_pulse + flash_time) {
    flash_state = !flash_state;
    last_flash_pulse = current_time;
  }

  if (distance <= FAR && enable_flash) {
    if (direction == LEFT) {
      digitalWrite(FLASH_LEFT, flash_state);
      digitalWrite(FLASH_RIGHT, false);
    } else if (direction == RIGHT) {
      digitalWrite(FLASH_LEFT, false);
      digitalWrite(FLASH_RIGHT, flash_state);
    }
  }
}

void updateNeoPixels() {
  // Run chase pattern in specified direction and frequency
  
}
