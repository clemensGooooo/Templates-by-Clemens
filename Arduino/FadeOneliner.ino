void setup() {
  pinMode(10, OUTPUT);
}

void loop() {
  
  analogWrite(10, millis() % 2048 / 1024 ? millis() % 2048 % 1024 / 4 : 255 - millis() % 2048 % 1024 /4);
  delay(1);
}
