// Pin definitions
const int leftButtonPin = 2; //use this for pro micro
const int rightButtonPin = 3; //use this for pro micro

// Timer variables
unsigned long previousMillis = 0;
const long interval = 5000;  // 5 seconds interval

void setup() {
  // Start serial communication at 9600 baud rate
  Serial.begin(9600);
  
  // Set pin modes
  pinMode(leftButtonPin, INPUT_PULLUP);
  pinMode(rightButtonPin, INPUT_PULLUP);
}

void loop() {
  // Read the status of pin 2 and pin 3
  int pin2State = digitalRead(leftButtonPin);
  int pin3State = digitalRead(rightButtonPin);

  // Check if pin 2 is receiving a HIGH signal
  if (pin2State == LOW) {
    Serial.println("Receiving on pin 2");
  }

  // Check if pin 3 is receiving a HIGH signal
  if (pin3State == LOW) {
    Serial.println("Receiving on pin 3");
  }

  // Check if 5 seconds have passed to print a message
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    Serial.println("5 seconds have passed");
  }

  // Small delay to avoid spamming the serial monitor
  delay(100);
}
