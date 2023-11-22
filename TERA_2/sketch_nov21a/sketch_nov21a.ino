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

void setup() 
{
  Serial.begin(9600);
}

void loop() 
{
//Read info from receiver-------------------------------
  int value1 = receiver.readChannel(0, 365, 170, 0);
  int value2 = receiver.readChannel(1, 255, -255, 0);
  int value3 = receiver.readChannel(2, 255, -255, 0);
  int value4 = receiver.readChannel(3, 255, -255, 0);
  int value5 = receiver.readSwitch(4, 1);
  int value6 = receiver.readChannel(5, 1, 3, 2);
// Reciver data print
  //Serial.print(value1);
  //Serial.print("\n");

//Encoder data print ----------------------------
  int encoder_data = (encoder.readEncoder());
  //Serial.print(encoder_data);
  //Serial.print("\n");

//Drive selector data ---------------------------  
  int Drive_number = drive_select.Drive_mode(value3, value6);
  //Serial.print(Drive_number);
  //Serial.println("\n");

//Steering data ---------------------------
  steering.Left_Right(value1, value5, encoder_data);
  
}
