#include <Servo.h>

Servo myServo3;
Servo myServo5;

int const potPin0 = A0;
int const potPin1 = A1;
int potVal0;
int angle0;
int potVal1;
int angle1;

void setup() {

  myServo3.attach(3); 
  myServo5.attach(5);

  //for debugging
  Serial.begin(9600);

}

void loop() {

  //read from the dial and convert to angle for each motor independetly:

  potVal0 = analogRead(potPin0);
  angle0 = map(potVal0, 0, 1023, 0, 179);

  potVal1 = analogRead(potPin1);
  angle1 = map(potVal1, 0, 1023, 0, 179);


  myServo3.write(angle0);
  myServo5.write(angle1);
  delay(15);

}
