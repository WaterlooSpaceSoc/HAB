static const short BAUD = 9600;

static const char RELAY = 'R';

void setup() {
  Serial.begin(BAUD);
}

void loop() {
  if(Serial.available() > 0){
    char c = Serial.read();
    interpretInput(c);
  }
}

void interpretInput(char command) {
  switch(command){
    case RELAY:
      sendResponse("ArduinoResponse " + String(command));
      break;
    default:
      sendResponse("ArduinoError");
  }
}

void sendResponse(String response){
  Serial.print(response);
  Serial.write('\0');
}

void sendData(String dataType, String data){
  sendResponse("ArduinoResponse " + dataType + " " + data)
}

// Data Scripts Go Under here

