/* Sweep
For use with audio activated animatronics
5v 386 pro mini board
*/

#include <Servo.h>
Servo myservo;  // create servo object to control a servo

bool pin4, pin5, pin6, pin7, pin8; 
int servoVal;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("Starting");
  myservo.attach(9);
  pinMode(4, INPUT);
  pinMode(5, INPUT);
  pinMode(6, INPUT);
  pinMode(7, INPUT);
  pinMode(8, INPUT);
  digitalWrite(4,HIGH);
  digitalWrite(5,HIGH);
  digitalWrite(6,HIGH);
  digitalWrite(7,HIGH);
  digitalWrite(8,HIGH);
}

void loop() {
  pin4 = digitalRead(4);
  pin5 = digitalRead(5);
  pin6 = digitalRead(6);
  pin7 = digitalRead(7);
  pin8 = digitalRead(8);
  Serial.print(pin4);
  Serial.print(" ");
  Serial.print(pin5);
  Serial.print(" ");
  Serial.print(pin6);
  Serial.print(" ");
  Serial.print(pin7);
  Serial.print(" ");
  Serial.println(pin8);
  if(!pin8) {
    servoVal=45;
    myservo.write(servoVal);
//    Serial.print(" pin8 ");
  }
  else if(!pin7) {
    servoVal=40;
    myservo.write(servoVal);
//    Serial.print(" pin7 ");
  }
  else if(!pin6) {
    servoVal=35;
    myservo.write(servoVal);
//    Serial.print(" pin6 ");
  }
  else if(!pin5) {
    servoVal=30;
    myservo.write(servoVal);
//    Serial.print(" pin5 ");
  }
  else if(!pin4) {
    servoVal=25;
    myservo.write(servoVal);
//    Serial.print(" pin4 ");
  }

  else {
    servoVal=0;
    myservo.write(servoVal);
//    Serial.print(" nothing ");
  }
//  Serial.println();
delay(5);
}
