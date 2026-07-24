#include <Servo.h>

Servo myServo;

const int motorPin1 = 11;
const int motorPin2 = 10;
const int servoPin  = 9;

unsigned long lastCommandTime = 0;
bool motorRunning = false;

void setup() {
  Serial.begin(115200);
  myServo.attach(servoPin);
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('$');
    cmd.trim();

    if (cmd.startsWith("f:")) {
      int speed = cmd.substring(2).toInt();
      analogWrite(motorPin1, speed);
      analogWrite(motorPin2, 0);
      motorRunning = true;
    }
    else if (cmd.startsWith("b:")) {
      int speed = cmd.substring(2).toInt();
      analogWrite(motorPin1, 0);
      analogWrite(motorPin2, speed);
      motorRunning = true;
    }
    else if (cmd.startsWith("s:")) {
      analogWrite(motorPin1, 0);
      analogWrite(motorPin2, 0);
      motorRunning = false;
    }
    else if (cmd.startsWith("a:")) {
      int angle = cmd.substring(2).toInt();
      myServo.write(angle);
    }

    lastCommandTime = millis();
  }

  if (motorRunning && (millis() - lastCommandTime > 500)) {
    analogWrite(motorPin1, 0);
    analogWrite(motorPin2, 0);
    motorRunning = false;
  }
}
