//Detecting Humidity with the HIH-4030 Humidity Sensor (Sparkfun breakout)


//From the bildr article http://bildr.org/2012/11/hih4030-arduino/

//Original Code by Samantha Marcano, April 2nd 2015
//Moved to GitHub June 30th

int HIH4030_Pin = A0; //analog pin 0

void setup(){
  Serial.begin(9600);
}

void loop(){

  //To properly caculate relative humidity, we need the temperature.
  float temperature = 25; //replace with a thermometer reading if you have it
  //DR: Will be replacing with temperature readings from the BMP sensor once integrated into hardware setup.
  float relativeHumidity  = getHumidity(temperature);

  Serial.println(relativeHumidity);

  delay(1000); //just here to slow it down so you can read it
}


float getHumidity(float degreesCelsius){
  //caculate relative humidity
  float supplyVolt = 5.0; //If changing to 3.3V, would need to change here.

  // read the value from the sensor:
  int HIH4030_Value = analogRead(HIH4030_Pin);
  float voltage = HIH4030_Value/1023. * supplyVolt; // convert to voltage value

  // convert the voltage to a relative humidity
  // - the equation is derived from the HIH-4030/31 datasheet
  // - it is not calibrated to your individual sensor
  //  Table 2 of the sheet shows the may deviate from this line
  float sensorRH = 161.0 * voltage / supplyVolt - 25.8;
  float trueRH = sensorRH / (1.0546 - 0.0026 * degreesCelsius); //temperature adjustment 
  
  //DR: Using the datasheet (as recommended in bldr article)
  
  float sensorRHoffset = (voltage - 0.958)/0.0307;
  float adjustedtrueRH = sensorRHoffset / (1.0546 - 0.0026 * degreesCelsius);
  
  
  //

//  return trueRH;

  return adjustedtrueRH //DR: Haven't actually tested with hardware yet (June 30th, 2015)
  
}
