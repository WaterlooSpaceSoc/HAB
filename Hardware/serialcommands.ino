#include <TinyGPS++.h>
#include <SoftwareSerial.h>

static const int RXPin = 4, TXPin = 3;
static const uint32_t GPSBaud = 9600;

TinyGPSPlus gps;
SoftwareSerial ss(RXPin, TXPin);

void setup() {
  Serial.begin(9600);
  ss.begin(GPSBaud);

  Serial.println(F("FullExample.ino"));
  Serial.println(F("An extensive example of many interesting TinyGPS++ features"));
  Serial.print(F("Testing TinyGPS++ library v. ")); Serial.println(TinyGPSPlus::libraryVersion());
  Serial.println(F("by Mikal Hart"));
  Serial.println();



}

void loop() {
  printGPSdata();
  delay(10000);
}

void printGPSdata() {
  Serial.print("Month: ");
  Serial.println(gps.date.month());
  Serial.print("Day: ");
  Serial.println(gps.date.day());
  Serial.print("Hour: ");
  Serial.println(gps.time.hour());
  Serial.print("Minutes: ");
  Serial.println(gps.time.minute());
  Serial.print("Speed(mps): ");
  Serial.println(gps.speed.mps());
  Serial.print("Altitude: ");
  Serial.println(gps.altitude.meters()); // Altitude in meters (double)
  Serial.print("Latitude: ");
  Serial.println(gps.location.lat(), 6); // Latitude in degrees (double)
  Serial.print("Longitude: ");
  Serial.println(gps.location.lng(), 6);
}


void serialEvent(){
  char command[] = "";
  while(Serial.available()){
    char commandchar = (char) Serial.read();
    command += commandchar;
  }
  if(command == "gps"){
    printGPSdata();
  }
  else if( command == "somethingelse"){
    //do something else
  }
}

