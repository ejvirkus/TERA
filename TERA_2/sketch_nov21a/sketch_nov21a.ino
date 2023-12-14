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

union{
    char bytes[6];
    struct{  // The struct and bytes[] share same memory location
        uint16_t logitech[3];
    }unpacked;
}packet;


uint16_t wheel = 328;
uint16_t throttle = 255;
unsigned char high;
unsigned char low;
unsigned char hight;
unsigned char lowt;

uint16_t readPacket(){
  if(Serial.available() > 5);
    
      Serial.println("got 5 packs ");
      //wheel
      Serial.readBytes(packet.bytes, 6);
      //Serial.readBytes(reinterpret_cast<char*>(&low), 1);
      //wheel = (high << 8) | low ;
      
      
      //Clears serial buffer
      for(int i = 0; i < 5; i++){
        char _ = Serial.read();
      }
      /*
      //throttle
      Serial.readBytes(reinterpret_cast<char*>(&hight), 1);
      Serial.readBytes(reinterpret_cast<char*>(&lowt), 1);
      
      throttle = (hight << 8) | lowt;
      */
    
}

void setup()
{
  Serial.begin(115200);
  //packet.unpacked.wheel = 328;
  Serial.setTimeout(10);
}


void loop()
{
  //readPacket();
  if(Serial.available() > 5);
    
      //Serial.println("got 5 packs ");
      
      Serial.readBytes(packet.bytes, 6);
      //Serial.readBytes(reinterpret_cast<char*>(&low), 1);
      //wheel = (high << 8) | low ;
      
      
      //Clears serial buffer
      for(int i = 0; i < 5; i++){
        char _ = Serial.read();
      }  
  
  //Serial.println(packet.unpacked.logitech[0]);

  //Serial.println(packet.unpacked.logitech[1]);
  
  //Serial.println(packet.unpacked.logitech[2]);
 
    //Serial.println("Received from Jetson Nano: ");
    //Serial.println(receivedData);


  //Read info from receiver-------------------------------
  int value1 = receiver.readChannel(0, 365, 170, 0); //Oli 365, 170
  int value2 = receiver.readChannel(1, 255, -255, 0);
  int value3 = receiver.readChannel(2, 255, -255, 0);
  int value4 = receiver.readChannel(3, 255, -255, 0);
  int value5 = receiver.readSwitch(4, 1);
  int value6 = receiver.readChannel(5, 1, 3, 2);
  // Reciver data print
  //Serial.print(receiver.readChannelRaw(0));
  //Serial.println(value1);
  //Serial.print("\n");


  //Encoder data print ----------------------------
  int encoder_data = (encoder.readEncoder());
  //Serial.print(encoder_data);
  //Serial.print("\n");

  //Drive selector data ---------------------------
  int Drive_number = drive_select.Drive_mode(value3, value6, packet.unpacked.logitech[1], value5);
  //Serial.print(Drive_number);
  //Serial.println("\n");

  //Steering data ---------------------------
  steering.Left_Right(value1, value5, encoder_data , packet.unpacked.logitech[0]);

  

}
