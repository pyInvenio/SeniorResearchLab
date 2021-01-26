/* Servo motor with Arduino example code. Position and sweep. More info: https://www.makerguides.com/ */
// Include the servo library:
#include <Servo.h>

// Include the Wire library for I2C
#include <Wire.h>


// Create a new servo object:
Servo myservo;
// Define the servo pin:
#define servoPin 9
// Create a variable to store the servo position:
int angle = 0;

// LED on pin 13
const int ledPin = 13; 


void setup() {
  // Attach the Servo variable to a pin:
  myservo.attach(servoPin);

  // Join I2C bus as slave with address 8
  Wire.begin(0x8);
  
  // Call receiveEvent when data received                
  Wire.onReceive(receiveEvent);
  
  // Setup pin 13 as output and turn LED off
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  myservo.write(90);
}

void receiveEvent(int howMany) {
  while (Wire.available()) { // loop through all but the last
    int c = Wire.read(); // receive byte as a character
    myservo.write(c);
  }
}

void loop() {
   delay(100);
}
