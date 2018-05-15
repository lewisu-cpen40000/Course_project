#include <SparkFunDS1307RTC.h>
#include "SparkFun_Si7021_Breakout_Library.h"
#include <Wire.h>

float humidity = 0;
int soilPin = A0;
int soilPower = 7;
float tempf = 0;
int pumpPin = 9;
int state = 0;
int flag = 0;
int soilMoisture = 0;

int thresholdUp = 400;
int thresholdDown = 250;

Weather sensor;
void setup() {
  // sets the pins as outputs:
  pinMode(pumpPin, OUTPUT);
  digitalWrite(pumpPin, LOW);
  pinMode(soilPower, OUTPUT);
  digitalWrite(soilPower, LOW);
  int soilMoisture;
  Serial.begin(9600); // Default connection rate for my BT module
  rtc.begin();
  sensor.begin();
  
  Serial.println("**********************************************************");
  Serial.println("*\tIngellegent watering system ON                   *");
  Serial.println("*\tPress 1 to turn pump ON                          *");
  Serial.println("*\tPress 0 to turn pump OFF                         *");
  Serial.println("*\tScreen will refresh every 10 seconds to display  *");
  Serial.println("*\tinformation about the plant                      *");
  Serial.println("*                                        \t         *");
  Serial.println("*\tEnjoy Your plant experience                      *");
  Serial.println("**********************************************************\n");
}

void loop() {
  rtc.update();
  getWeather();
  if(rtc.second() %  10 == 0) // If the half-minute
  {
    printTime(); // Print the new time
    soilMoisture = readSoil();
    printInfo();
    delay(1000);
  }

  //if some data is sent, read it and save it in the state variable
  if (Serial.available() > 0) {
    state = Serial.read();
    flag = 0;
  }
  // if the state is 0 the led will turn off
  if (state == '0') {
    digitalWrite(pumpPin, LOW);
    if (flag == 0) {
      Serial.println("PUMP: off");
      flag = 1;
    }
  }
  // if the state is 1 the led will turn on
  else if (state == '1') {
    digitalWrite(pumpPin, HIGH);
    if (flag == 0) {
      Serial.println("PUMP: on");
      flag = 1;
    }
  }
}
void printTime()
{
  Serial.print(String(rtc.hour()) + ":"); // Print hour
  if (rtc.minute() < 10)
    Serial.print('0'); // Print leading '0' for minute
  Serial.print(String(rtc.minute()) + ":"); // Print minute
  if (rtc.second() < 10)
    Serial.print('0'); // Print leading '0' for second
  Serial.print(String(rtc.second())); // Print second

  if (rtc.is12Hour()) // If we're in 12-hour mode
  {
    // Use rtc.pm() to read the AM/PM state of the hour
    if (rtc.pm()) Serial.print(" PM"); // Returns true if PM
    else Serial.print(" AM");
  }

  Serial.print(" | ");
  Serial.print(rtc.dayStr()); // Print day string
  Serial.println("\n");
}

void getWeather()
{
  // Measure Relative Humidity from the HTU21D or Si7021
  humidity = sensor.getRH();

  // Measure Temperature from the HTU21D or Si7021
  tempf = sensor.getTempF();
  // Temperature is measured every time RH is requested.
  // It is faster, therefore, to read it from previous RH
  // measurement with getTemp() instead with readTemp()
}
void printInfo()
{
  //This function prints the weather data out to the default Serial Port
  String DisplayWords;
  Serial.print("\tCurrent Temp: ");
  Serial.print(tempf);
  Serial.println("F ");

  Serial.print("\tHumidity: ");
  Serial.print(humidity);
  Serial.println("% ");

  Serial.print("\tSoil Moisture: ");
  Serial.print(String(soilMoisture) + " units.");
  Serial.println();
  Serial.print("\tYour plant is ");

  if (soilMoisture <= thresholdDown) {
    // move cursor to beginning of second line on LCD
    DisplayWords = "Dry! Water it!";
    Serial.println(DisplayWords);
    if (checkPumpState() == 0) {
      Serial.println("\n\tYour pump is: OFF");
      Serial.println("\tPress 1 to turn on the pump");
      Serial.println("\tIt is recommended you turn it ON");
    }
    else {
      Serial.println("\n\tYour pump is: ON");
      Serial.println("\tPress 0 to turn it OFF");
      Serial.println("\tIt is recommended you keep it ON until saturated");
    }
  } else if (soilMoisture >= thresholdUp) {
    DisplayWords = "Wet, Leave it!";
    Serial.println(DisplayWords);
    if (checkPumpState() == 1) {
      Serial.println("\n\tYour pump is: ON");
      Serial.println("\tPress 0 to turn off the pump");
      Serial.println("\tIt is recommended you turn it OFF");
    }
    else {
      Serial.println("\n\tYour pump is: OFF");
      Serial.println("\tPress 1 to turn it on");
      Serial.println("\tIt is recommended you keep it OFF");
    }
  }
  Serial.println("*************************************************************\n");
}
int readSoil()
{
  digitalWrite(soilPower, HIGH);//turn D7 "On"
  delay(10);//wait 10 milliseconds
  int val = analogRead(soilPin);//Read the SIG value form sensor
  digitalWrite(soilPower, LOW);//turn D7 "Off"
  return val;//send current moisture value
}
int checkPumpState() {
  int pump = digitalRead(pumpPin);
  if (pump == 1) {
    return 1;
  }
  else {
    return 0;
  }
}

