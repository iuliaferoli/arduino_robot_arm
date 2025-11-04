#include <Servo.h>

Servo myServo3;
Servo myServo5;

int const potPin0 = A0;
int potVal0;
int potVal0_previous;
int angle0;


int const potPin1 = A1;
int potVal1;
int potVal1_previous;
int angle1;


const int buttonPinRelax = 13; 
int buttonStateRelax = 0; 

const int buttonPinMax = 12; 
int buttonStateMax = 0; 

void setup() {

  myServo3.attach(3); 
  myServo5.attach(5);

  //for debugging
  Serial.begin(9600);

  potVal0_previous = analogRead(potPin0);
  potVal1_previous = analogRead(potPin1);

}

int new_angle(int angle, int potValue, int potValue_previous) {
  potValue = map(potValue, 0, 1023, 0, 179);
  potValue_previous = map(potValue_previous, 0, 1023, 0, 179);

  int difference = potValue - potValue_previous;
  int new_angle = angle + difference;
  
  if (new_angle > 1023) {
    return 179;
  }
  if (new_angle < 0) {
    return 0;
  }
  return new_angle;
}

void loop() {

  buttonStateRelax = digitalRead(buttonPinRelax);
  buttonStateMax = digitalRead(buttonPinMax);

  if (buttonStateRelax == HIGH) {
    angle0 = 0;
    angle1 = 0;
    myServo3.write(0);
    myServo5.write(0);
  }
  if (buttonStateMax == HIGH) {
    angle0 = 179;
    angle1 = 179;
    myServo3.write(179);
    myServo5.write(179);
  }

  potVal0 = analogRead(potPin0);
  angle0 = new_angle(angle0, potVal0, potVal0_previous);
  myServo3.write(angle0);
  potVal0_previous = potVal0;


  potVal1 = analogRead(potPin1);
  angle1 = new_angle(angle1, potVal1, potVal1_previous);
  myServo5.write(angle1);
  potVal1_previous = potVal1;

  

}