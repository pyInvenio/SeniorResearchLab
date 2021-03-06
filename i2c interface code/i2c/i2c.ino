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

String[] splitCommand(String text, char splitChar) {
    int splitCount = countSplitCharacters(text, splitChar);
    String returnValue[splitCount];
    int index = -1;
    int index2;

    for(int i = 0; i < splitCount - 1; i++) {
        index = text.indexOf(splitChar, index + 1);
        index2 = text.indexOf(splitChar, index + 1);

        if(index2 < 0) index2 = text.length() - 1;
        returnValue[i] = text.substring(index, index2);
    }

    return returnValue;
}

int countSplitCharacters(String text, char splitChar) {
    int returnValue = 0;
    int index = -1;

    while (index > -1) {
        index = text.indexOf(splitChar, index + 1);

        if(index > -1) returnValue+=1;
    }

    return returnValue;
}

void receiveEvent(int howMany) {
  while (Wire.available()) { // loop through all but the last
    String c = Wire.read(); // receive byte as a character
    String arr[countSplitCharacters(c, '$')] = splitCommand(c, '$');
    Serial.print(arr);
//    if(method == "1"){
//      
//    }
//    else if(method == "2"){
//      
//    }
//    else if(method == "3") {
//      
//    }
//    else if(method == "4"){
//      
//    }
//    else{
//      Serial.println("Error");
//    }
//    
//    
//    myservo.write(c);
  }
}

void loop() {
   delay(100);
}
