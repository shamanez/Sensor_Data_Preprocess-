/*This code is developed by T.Beniel for Ardino Fio. Ports might have to be changed
for using any other boards
*/

#include <VL53L0X.h>    //VL53l0x TOF sensor library
#include "Wire.h"

extern "C" {
#include "utility/twi.h"
}

VL53L0X sensors[9];

const int xshut[]={12,11,10,9,8,7,6,5,4};      //shutdonwn pins of sensors
const int devAdrr[]={0x25,0x26,0x27,0x28,0x2a,0x2b,0x2c,0x2d,0x2e};   //Defined device addresses

void setup() {
  while (!Serial);
  delay(1000);

  Wire.begin();
  Serial.begin(115200);

  // wait until serial port opens for native USB devices
  while (! Serial) {
    delay(1);
  }

  for(int i=0;i<9;i++){
    pinMode(xshut[i],OUTPUT);
  }

  for(int i=0;i<9;i++){
    digitalWrite(xshut[i],LOW);
  }


  //Setting up device adresses in the initiation
  
  for(int i=0;i<9;i++){
    digitalWrite(xshut[i],HIGH);
    sensors[i].init();
    sensors[i].setTimeout(500);

    sensors[i].startContinuous();
    sensors[i].setAddress(devAdrr[i]);
  }
  
}

uint8_t f_num=0;    // frame number in of the data frame sending since 8 bit it will be  0 - 256
void loop() {
  f_num++;
  unsigned long start_time = millis();
  uint16_t messurements[9];
  for(int i=0;i<9;i++){
    Wire.beginTransmission(devAdrr[i]);
    messurements[i] = sensors[i].readRangeContinuousMillimeters();
    if(messurements[i] > 1000){
      messurements[i] = 1000;
    }
    if (sensors[i].timeoutOccurred()){
      //Serial.print(" TIMEOUT");  //if the laser isn't found, print TIMEOUT
      messurements[i] = 1000;
    }
    Wire.endTransmission(); //end transmission to laser1
    //Serial.print("sensor "); Serial.print(i+1); Serial.print(" reading: "); Serial.println(messurements[i]);
    delay(2);
  }
  for ( int i=0;i<9;i++){
   Serial.print(messurements[i]);
   Serial.print(" ");
   
  }
  Serial.println(f_num);
  //unsigned long end_time1 = millis();
  //Serial.print(" Elapsed Time: "); Serial.print(end_time1 - start_time);
  delay(2);
  //unsigned long end_time2 = millis();
  //Serial.print(" Round Time: "); Serial.println(end_time2 - start_time);
}

