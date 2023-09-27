//         Potentiometer               LED
// connect VIN  PIN  A0    and    GROUND 10

int sensorValue = 0;
int led = 10; // only PWM pins
int mode = 2;  // mode one will change the blinking rate of the led, mode two will change the brightness


void setup() {
  Serial.begin(9600);
  pinMode(A0, INPUT);
  pinMode(led, OUTPUT);
}

void loop() {
  sensorValue = analogRead(A0);
  if (mode == 1) {
    delay(sensorValue / 4);
    digitalWrite(led, HIGH);

    delay(sensorValue / 4);
    digitalWrite(led, LOW);
  } else {
    analogWrite(led, sensorValue / 4);
  }
  // Serial.println(sensorValue);
}
