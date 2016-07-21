//Integrating Arduino with Message Processor
//July 25th 2015

#include <TinyGPS++.h>
#include <SoftwareSerial.h>


static const short BAUD = 9600;

static const int RXPin = 4, TXPin = 3;
static const uint32_t GPSBaud = 9600;
//static const uint32_t GPSBaud = 4800;

static const char RELAY = 'R';
static const char BAROMETER = 'B';
static const char HUMIDITY = 'H';
//static const char GPSstamp = 'T';
//static const char GPSdata = 'G';
//static const char RELAY = 'R';

String getFloatString(float x, byte precision){
  int mag = 1;
  for(int i = 0; i < precision; ++i){
    mag *= 10;
  }
  String str = int(x) + ".";
  if(x >= 0)
    str += String(int((x - int(x)) * mag));
  else
    str += String(int((int(x) - x) * mag));
  return str;
}

TinyGPSPlus gps;
SoftwareSerial ss(RXPin, TXPin);

//Barometer Stuff

#include <SFE_BMP180.h>
#include <Wire.h>

SFE_BMP180 pressure;

double baseline; // baseline pressure

void GPStimestamp() {
  //Check for Python Parity

  String GPSstring = String(gps.date.month()) + " " + String(gps.date.day()) + " " + String(gps.time.hour()) + " " + String(gps.time.minute()) + " " + getFloatString(gps.speed.mps(),2) + " " + getFloatString(gps.altitude.meters(),2) + " " + getFloatString(gps.location.lat(), 6) + " " + getFloatString(gps.location.lng(), 6);

  sendData("gpsTimestamp", GPSstring);

  //
  //And that should be everything, right?  

}

void GPSdatagrab() {

  String GPSstring = getFloatString(gps.location.lat(), 6) + " " + getFloatString(gps.location.lng(), 6);

  sendData("gpsData", GPSstring);

}

int disable_barometer = 0; //Variable we'll use to keep us from trying to use the barometer if it fails to init.


//Barometer readings

double getPressure()
{
  char status;
  double T,P,p0,a;

  // You must first get a temperature measurement to perform a pressure reading.

  // Start a temperature measurement:
  // If request is successful, the number of ms to wait is returned.
  // If request is unsuccessful, 0 is returned.

  status = pressure.startTemperature();
  if (status != 0)
  {
    // Wait for the measurement to complete:

    delay(status);

    // Retrieve the completed temperature measurement:
    // Note that the measurement is stored in the variable T.
    // Use '&T' to provide the address of T to the function.
    // Function returns 1 if successful, 0 if failure.

    status = pressure.getTemperature(T);
    if (status != 0)
    {
      // Start a pressure measurement:
      // The parameter is the oversampling setting, from 0 to 3 (highest res, longest wait).
      // If request is successful, the number of ms to wait is returned.
      // If request is unsuccessful, 0 is returned.

      status = pressure.startPressure(3);
      if (status != 0)
      {
        // Wait for the measurement to complete:
        delay(status);

        // Retrieve the completed pressure measurement:
        // Note that the measurement is stored in the variable P.
        // Use '&P' to provide the address of P.
        // Note also that the function requires the previous temperature measurement (T).
        // (If temperature is stable, you can do one temperature measurement for a number of pressure measurements.)
        // Function returns 1 if successful, 0 if failure.

        status = pressure.getPressure(P,T);
        if (status != 0)
        {
          return(P);
        }
        else Serial.println("error retrieving pressure measurement\n");
      }
      else Serial.println("error starting pressure measurement\n");
    }
    else Serial.println("error retrieving temperature measurement\n");
  }
  else Serial.println("error starting temperature measurement\n");
}

//Function that uses the getPressure function.

void barometerREAD() {

  double a,P;

  // Get a new pressure reading:

  P = getPressure();

  // Show the relative altitude difference between
  // the new reading and the baseline reading:

  a = pressure.altitude(P,baseline);

  //note that since we established the baseline pressure in void setup(), the altitude reading will now be relative to that pressure.

  sendData("barometerData", getFloatString(a, 2));

}

//Humidity sensor stuff

int HIH4030_Pin = A1; //analog pin 1

float getHumidity(float degreesCelsius){
  //caculate relative humidity
  float supplyVolt = 5.0;

  // read the value from the sensor:
  int HIH4030_Value = analogRead(HIH4030_Pin);
  float voltage = HIH4030_Value/1023. * supplyVolt; // convert to voltage value

  // convert the voltage to a relative humidity
  // - the equation is derived from the HIH-4030/31 datasheet
  // - it is not calibrated to your individual sensor
  //  Table 2 of the sheet shows the may deviate from this line
  float sensorRH = 161.0 * voltage / supplyVolt - 25.8;
  float trueRH = sensorRH / (1.0546 - 0.0026 * degreesCelsius); //temperature adjustment 

  return trueRH;
}


//Function that uses getHumidity()

void humidityREAD() {

  float temperature = 25; //replace with a thermometer reading if you have it
  float relativeHumidity  = getHumidity(temperature);
  //sendData("humidityData", String(relativeHumidity, 2));
  sendData("humidityData", getFloatString(relativeHumidity, 2));

}

void sendResponse(String response){
  Serial.print(response);
  Serial.write('\0');
}

void sendData(String dataType, String data){
  sendResponse("ArduinoResponse " + dataType + " " + data);
}

void setup() {
  Serial.begin(BAUD);
  ss.begin(GPSBaud); //Needed for TinyGPS
  //pinMode(A0, INPUT);
  //pinMode(A1, INPUT);
  pinMode(HIH4030_Pin, INPUT);

  //Turning on the barometer

  if (pressure.begin()) {
    Serial.println("BMP180 init success");
    //Get the baseline pressure, we're assuming we init while on the ground.
    baseline = getPressure();
    Serial.println(baseline);

  } 
  else
  {
    // Oops, something went wrong, this is usually a connection problem,
    // see the comments at the top of this sketch for the proper connections.

    Serial.println("BMP180 init fail (disconnected?)\n\n");
    //while(1); // Pause forever.
    disable_barometer = 1; //Error code changed so now we won't be able to execute the barometer function.
  }
}


void interpretInput(char command) {
  switch(command){
  case RELAY:
    sendResponse("ArduinoResponse " + String(command));
    break;
  case BAROMETER:
  if (disable_barometer == 1)
     sendData("barometerData", "-999");
    else
    barometerREAD(); //function which sends barometer data over serial
    break;
  case HUMIDITY:
    humidityREAD();
    break;
  case GPSstamp:
    GPStimestamp();
    break;
  case GPSdata:
    GPSdatagrab();
    break;
  default:
    sendResponse("ArduinoError");
  }
}

void loop() {
  if(Serial.available() > 0){ //If there's anything coming in from Python.
    char c = Serial.read();
    interpretInput(c); //full of switch cases to interpret the serial stuff.
  }
}
