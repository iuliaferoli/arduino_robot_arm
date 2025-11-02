#include <Servo.h>

Servo myServo;

int const potPin = A0;
int potVal;
int angle;

void setup() {

  //connecting the servomotor to pin ~9
  myServo.attach(9); 

  //for debugging
  Serial.begin(9600);

}

void loop() {

  //read from the dial
  potVal = analogRead(potPin);
  Serial.print("potVal: ");
  Serial.print(potVal);

  //convert the dial to values for the motor
  angle = map(potVal, 0, 1023, 0, 179);
  Serial.print(", angle:");
  Serial.print(angle);

  //move to motor angle
  myServo.write(angle);
  delay(15);

}
