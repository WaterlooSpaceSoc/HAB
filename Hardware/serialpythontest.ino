//
//WORKING WAY TO GET SERIAL DATA READ INTO PYTHON, JULY 21st 2015
//




void setup() {
  
  Serial.begin(9600);
  pinMode(A0, INPUT);
  
}

void loop() {
  
  
  int x = 0;
  
  while (x < 100){
    
  float serval = 0.00;
  
  serval = analogRead(A0);
  Serial.print("V");
  Serial.print(serval);
  Serial.println("E");
  delay(100);
x = x + 1;  
}
  
}
