// Pin definitions
const int sensorPin = A0;  // Analog pin connected to the phototransistor

void setup() {
  // Start serial communication at 9600 baud rate
  Serial.begin(9600);
  
}

void loop() {
 
int initialSensorValue = analogRead(sensorPin);
Serial.println(initialSensorValue);

  // Small delay to avoid spamming the serial monitor
  delay(100);
}
