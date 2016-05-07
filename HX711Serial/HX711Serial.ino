#include "HX711.h"
#include <LiquidCrystal.h>

// HX711.DOUT	- pin #A1
// HX711.PD_SCK	- pin #A0

// LCD.RS - pin 8
// LCD.En - pin 9
// LCD.D4 - pin 4
// LCD.D5 - pin 5
// LCD.D6 - pin 6
// LCD.D7 - pin 7

LiquidCrystal lcd(8, 9, 4, 5, 6, 7);
HX711 scale(A3, A2);		// parameter "gain" is ommited; the default value 128 is used by the library

float x = 5.11415525114155;

void setup() {
  Serial.begin(38400);
  lcd.begin(16, 2);
  Serial.println("HX711 Demo");

  Serial.println("Before setting up the scale:");
  Serial.print("read: \t\t");
  Serial.println(scale.read());			// print a raw reading from the ADC

  Serial.print("read average: \t\t");
  Serial.println(scale.read_average(20));  	// print the average of 20 readings from the ADC

  Serial.print("get value: \t\t");
  Serial.println(scale.get_value(5));		// print the average of 5 readings from the ADC minus the tare weight (not set yet)

  Serial.print("get units: \t\t");
  Serial.println(scale.get_units(5), 1);	// print the average of 5 readings from the ADC minus tare weight (not set) divided 
						// by the SCALE parameter (not set yet)  

  scale.set_scale(2280.f);                      // this value is obtained by calibrating the scale with known weights; see the README for details
  scale.tare();				        // reset the scale to 0

  Serial.println("After setting up the scale:");

  Serial.print("read: \t\t");
  Serial.println(scale.read());                 // print a raw reading from the ADC

  Serial.print("read average: \t\t");
  Serial.println(scale.read_average(20));       // print the average of 20 readings from the ADC

  Serial.print("get value: \t\t");
  Serial.println(scale.get_value(5));		// print the average of 5 readings from the ADC minus the tare weight, set with tare()

  Serial.print("get units: \t\t");
  Serial.println(scale.get_units(5), 1);        // print the average of 5 readings from the ADC minus tare weight, divided 
						// by the SCALE parameter set with set_scale

  Serial.println("Readings:");
}

void loop() {
  Serial.print("one reading:\t");
  Serial.print(scale.get_units()*x+0.2, 1);
  Serial.print("\t| average:\t");
  Serial.println(scale.get_units(10), 1);

  lcd.setCursor(0, 0);
  lcd.print(scale.get_units()*x+0.2, 1);
  lcd.print(" g");
  lcd.print("       ");
  
  scale.power_down();			        // put the ADC in sleep mode
  delay(500);
  scale.power_up();
}
