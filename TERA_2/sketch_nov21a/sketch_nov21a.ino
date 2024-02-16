#include <Stepper.h>
#include <IBusBM.h>
#include <ros.h>
#include <std_msgs/Int32.h>

#include "Receiver.h"
#include "Steering_encoder.h"
#include "Drive_selector.h"
#include "Steering.h"

ros::NodeHandle nh;

ReceiverData receiver;
Steering_encoder_data encoder(30, 28, 32);
Drive_selector_switch drive_select;
Steering steering;


int32_t wheel = 267;
int32_t fwd = 0;
int32_t ebrake = 0;

//--------------ROS CALLBACK FUNCTIONS---------------
//Steering
void messageCb(const std_msgs::Int32& steering){
  wheel = steering.data;
  wheel = map(wheel, 0, 655, 170, 365);
}
//Throttle/Forward movement
void movingCb(const std_msgs::Int32& moving){
  fwd = moving.data;
  //throttle = map (throttle, 255, 0, 0, 255);
}
void lidarCb(const std_msgs::Int32& brake){
  ebrake = brake.data;
}

//-----------------------FUNCTION CALLOUTS------------------------------
ros::Subscriber<std_msgs::Int32> sub("brake", &lidarCb);
//ros::Subscriber<std_msgs::Int32> sub3("steering", &messageCb);
//ros::Subscriber<std_msgs::Int32> sub2("moving", &movingCb);


void setup()
{
  Serial.begin(115200);
  nh.getHardware()->setBaud(115200);
  Serial.setTimeout(10);
  nh.initNode();
  nh.subscribe(sub);
  //nh.subscribe(sub2);
  //nh.subscribe(sub3);

  pinMode(LED_BUILTIN, OUTPUT);
}


void loop()
{
  nh.spinOnce();

  if(ebrake > 0){
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
 
  }
  else{
    digitalWrite(LED_BUILTIN, LOW);
    
  }
 
    //Serial.println("Received from Jetson Nano: ");
    //Serial.println(receivedData);

  int value1 = 268;
  //Read info from receiver-------------------------------
  value1 = receiver.readChannel(0, 365, 170, 0); //Oli 365, 170
  int value2 = receiver.readChannel(1, 255, -255, 0);
  int value3 = receiver.readChannel(2, 255, -255, 0);
  int value4 = receiver.readChannel(3, 255, -255, 0);
  int value5 = receiver.readSwitch(4, 1);
  int value6 = receiver.readChannel(5, 1, 3, 2);
  int value8 = receiver.readSwitch(7, 1);
  // Reciver data print
  //Serial.print(receiver.readChannelRaw(0));
  //Serial.println(value8);
  //Serial.print("\n");


  //Encoder data print ----------------------------
  int encoder_data = (encoder.readEncoder());
  //Serial.print(encoder_data);
  //Serial.print("\n");

  //Drive selector data ---------------------------
  int Drive_number = drive_select.Drive_mode(value3, value6, fwd, value5, value8, ebrake);
  //Serial.print(Drive_number);
  //Serial.println("\n");

  //Steering data ---------------------------
  steering.Left_Right(value1, value5, encoder_data , wheel);


}
