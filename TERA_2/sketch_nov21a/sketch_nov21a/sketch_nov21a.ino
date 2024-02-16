#include <Stepper.h>
#include <IBusBM.h>

#include "Receiver.h"
#include "Steering_encoder.h"
#include "Drive_selector.h"
#include "Steering.h"

ReceiverData receiver;
Steering_encoder_data encoder(30, 28, 32);
Drive_selector_switch drive_select;
Steering steering;


int32_t wheel = 267;
int32_t fwd = 0;
bool ebrake = 1;
String received;


void setup() {
  Serial.begin(115200);
  Serial.setTimeout(20);
}

void loop() {
  
  // Reading info from Jetson:
  if (Serial.available()){
    received = Serial.readString();
    ebrake = received.toInt();
    Serial.println(ebrake);
  }

  //Defining RC remote info ranges
  int value1 = 268;
  //Read info from receiver-------------------------------
  value1 = receiver.readChannel(0, 365, 170, 0); //Oli 365, 170
  int value2 = receiver.readChannel(1, 255, -255, 0);
  int value3 = receiver.readChannel(2, 255, -255, 0);
  int value4 = receiver.readChannel(3, 255, -255, 0);
  int value5 = receiver.readSwitch(4, 1);
  int value6 = receiver.readChannel(5, 1, 3, 2);
  int value8 = receiver.readSwitch(7, 1);
  /*
   * value1 = Steering 
   * value2 = Right joy up/down (Empty)
   * value3 = Throttle
   * value4 = Left joy left/right (Empty)
   * value5 = RC/TO switch
   * value6 = Transfer box (FWD/AWD/RWD)
   * value8 = Safety switch
   */

  //Reading encoder info
  int encoder_data = (encoder.readEncoder());

  //Drive function call
  drive_select.Drive_mode(value3, value6, fwd, value5, value8, ebrake);

  //Steering function call
  steering.Left_Right(value1, value5, encoder_data , wheel);
  
}
