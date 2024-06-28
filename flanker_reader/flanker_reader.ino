const int sensorPin = A0;  // Analog pin connected to the phototransistor
const int leftButtonPin = 8; //use this for uno r4 wifi
const int rightButtonPin = 11; //use this for uno r4 wifi

//const int leftButtonPin = 2; //use this for pro micro
//const int rightButtonPin = 3; //use this for pro micro

bool armed = false;
bool leftButtonPressed = false;
bool rightButtonPressed = false;
int triggerThreshold = 40;

int leftButtonState = 0;
int rightButtonState = 0;

const int sensorValueArrayLength = 300;
int sensorValues[sensorValueArrayLength]; // Array to store the last 10 sensor values
int sensorIndex = 0;  // Index for the circular buffer

volatile unsigned long photoDetectorTriggeredAt = 0;
volatile unsigned long reactionTime = 0;

void setup() {
  Serial.begin(9600);  // Initialize serial communication for debugging

  pinMode(leftButtonPin, INPUT_PULLUP);
  pinMode(rightButtonPin, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(leftButtonPin), handleButtonPressLeft, FALLING);
  attachInterrupt(digitalPinToInterrupt(rightButtonPin), handleButtonPressRight, FALLING);

  // Initialize the sensorValues array with the initial sensor reading
  int initialSensorValue = analogRead(sensorPin);
  for (int i = 0; i < sensorValueArrayLength; i++) {
    sensorValues[i] = initialSensorValue;
  }
}

void loop() {
  int sensorValue = analogRead(sensorPin);  // Read the analog value

  // Check if the new value is threshold less than the oldest value in the buffer
  if (sensorValue < sensorValues[sensorIndex] - triggerThreshold) {
    armed = true;
    photoDetectorTriggeredAt = micros();  // Get the current time in microseconds
    //Serial.println("armed");
    for (int i = 0; i < sensorValueArrayLength; i++) {
      sensorValues[i] = sensorValue;
    }
    delay(10);  // Delay for a short while to avoid overwhelming the serial output
  }

  // Update the circular buffer with the new sensor value
  sensorValues[sensorIndex] = sensorValue;
  sensorIndex = (sensorIndex + 1) % sensorValueArrayLength;  // Increment index and wrap around using modulo

  if (leftButtonPressed) {
    leftButtonPressed = false;
    Serial.println("left");
    //Serial.print("reactionTime: ");
    Serial.println(reactionTime);
    delay(100);  // Delay for a short while to avoid overwhelming the serial output
  }

  if (rightButtonPressed) {
    rightButtonPressed = false;
    Serial.println("right");
    //Serial.print("reactionTime: ");
    Serial.println(reactionTime);
    delay(100);  // Delay for a short while to avoid overwhelming the serial output
  }

  //Serial.println(sensorValue);
  //delay(10);  // Delay for a short while to avoid overwhelming the serial output
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
