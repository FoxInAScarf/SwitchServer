void setup() {
  
  Serial.begin(9600);

  pinMode(8, OUTPUT);

}

void loop() {

  while (Serial.available() == 0) {}
  String request = Serial.readString();
  request.trim();

  if (request == "status") {

    Serial.println("arduino4060");
    return;
    
  }

  if (request == "wakeup") {

    digitalWrite(8, HIGH);
    delay(500);
    digitalWrite(8, LOW);
    
  }

  if (request == "flushPower") {

    digitalWrite(8, HIGH);
    delay(20000);
    digitalWrite(8, LOW);
    
  }

}
