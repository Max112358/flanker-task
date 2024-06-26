const int sensorPin = A0;  // Analog pin connected to the phototransistor
const int leftButtonPin = 8;
const int rightButtonPin = 11;

bool armed = false;
bool leftButtonPressed = false;
bool rightButtonPressed = false;
int triggerThreshold = 35;

int leftButtonState = 0;
int rightButtonState = 0;

int sensorValue = 0;
int lastSensorValue = 0;

volatile unsigned long photoDetectorTriggeredAt = 0;
volatile unsigned long reactionTime = 0;

void setup() {
  Serial.begin(9600);  // Initialize serial communication for debugging

  pinMode(leftButtonPin, INPUT_PULLUP);
  pinMode(rightButtonPin, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(leftButtonPin), handleButtonPressLeft, FALLING);
  attachInterrupt(digitalPinToInterrupt(rightButtonPin), handleButtonPressRight, FALLING);
}

void loop() {
  sensorValue = analogRead(sensorPin);  // Read the analog value

  //int leftButtonValue = digitalRead(leftButtonPin);  // Read the analog value
  //Serial.println(leftButtonValue);

  // Detect a significant drop in light level
  if (sensorValue < lastSensorValue - triggerThreshold) {
    armed = true;
    photoDetectorTriggeredAt = micros();  // Get the current time in microseconds
    //Serial.println("armed");
  }

  // Update the previous state
  lastSensorValue = sensorValue;

  if (leftButtonPressed) {
    leftButtonPressed = false;
    Serial.println("left");
    //Serial.print("reactionTime: ");
    Serial.println(reactionTime);
  }

  if (rightButtonPressed) {
    rightButtonPressed = false;
    Serial.println("right");
    //Serial.print("reactionTime: ");
    Serial.println(reactionTime);
  }

  delay(100);  // Delay for a short while to avoid overwhelming the serial output
}

void handleButtonPressLeft() {
  if (armed) {
    unsigned long currentPressTime = micros();  // Get the current time in microseconds
    reactionTime = currentPressTime - photoDetectorTriggeredAt;
    leftButtonPressed = true;
    armed = false;
  }
}

void handleButtonPressRight() {
  if (armed) {
    unsigned long currentPressTime = micros();  // Get the current time in microseconds
    reactionTime = currentPressTime - photoDetectorTriggeredAt;
    rightButtonPressed = true;
    armed = false;
  }
}
