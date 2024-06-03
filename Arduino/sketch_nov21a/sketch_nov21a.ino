#include <Stepper.h>
#include <IBusBM.h>
//For ros:
//#include <ros.h>

//#include <geometry_msgs/Point32.h>

#include "Receiver.h"
#include "Steering_encoder.h"
#include "Drive_selector.h"
#include "Steering.h"



ReceiverData receiver;
Steering_encoder_data encoder(30, 28, 32);
Drive_selector_switch drive_select;
Steering steering;


#define HALL1 3
#define HALL2 4
#define HALL3 5

struct sendata {
  volatile int val;
};

struct receive { //data to receive
  volatile int x;
  volatile int y;
};
struct sendata values;
struct receive bytes;
const int total_bytes=2*sizeof(int);
int i;
byte buf[total_bytes];

int FL_ticks = 0;
String prev_FL = "000";


int wheel = 267;
int moving = 0;
int32_t ebrake = 0;


//For ROS 
//ros::NodeHandle nh;

//-----------CALLBACK FUNCTIONS---------------
/*
void messageCb(const geometry_msgs::Point32& info){
  wheel = info.x;
  moving = info.y;
  //Serial.println(wheel);

}
*/
//-----------------------FUNCTION CALLOUTS------------------------------

//ros::Subscriber<geometry_msgs::Point32> sub("info", &messageCb);

//---------------------ROS PUBLISHER--------------

//geometry_msgs::Point32 output;
//ros::Publisher pub("arduino", &output);

void setup() {
  Serial.begin(115200);
  
  pinMode(HALL1, INPUT);
  pinMode(HALL2, INPUT);
  pinMode(HALL3, INPUT);
  Serial.setTimeout(2);

  //nh.getHardware()->setBaud(115200);
  //nh.initNode();
  //nh.subscribe(sub);
  //init publisher:
  //nh.advertise(pub);
}


void loop()
{
  
  //INFO FROM JETSON
  if (Serial.available() >= total_bytes){
    i = 0;
    while(i < total_bytes){
      buf[i] = Serial.read();
      i++;
    }
    memmove(&bytes,buf,sizeof(bytes));
    //int val = int(trunc(bytes.value));
    wheel = bytes.x;
    moving = bytes.y;
    values.val = moving;
    Serial.write((const uint8_t*)&values, sizeof(values));
    

  }
  
  
  //Hall sensor info:

  String FL = String(digitalRead(HALL1)) + String(digitalRead(HALL2)) + String(digitalRead(HALL3));
  
  if(prev_FL != FL){
    FL_ticks += 1;
    prev_FL = FL;
    //Serial.print(FL_ticks);
    //Serial.print(" ");
    //Serial.println(FL);
  }
  
  
 
    //Serial.println("Received from Jetson Nano: ");
    //Serial.println(receivedData);

  int value1 = 267;
  int value5 = 1;
  //Read info from receiver-------------------------------
  value1 = receiver.readChannel(0, 365, 170, 0); //Oli 365, 170
  int value2 = receiver.readChannel(1, 255, -255, 0);
  int value3 = receiver.readChannel(2, 255, -255, 0);
  int value4 = receiver.readChannel(3, 255, -255, 0);
  value5 = receiver.readSwitch(4, 1);
  int value6 = receiver.readChannel(5, 1, 3, 2);
  int value8 = receiver.readSwitch(7, 1);
  // Reciver data print
  //Serial.print(receiver.readChannelRaw(0));
  //Serial.println(value5);
  //Serial.print("\n");


  //Encoder data print ----------------------------
  int encoder_data = (encoder.readEncoder());
  //Serial.print(encoder_data);
  //Serial.print("\n");

  //Drive selector data ---------------------------
  int Drive_number = drive_select.Drive_mode(value3, value6, moving, value5, value8, ebrake);
  //Serial.print(Drive_number);
  //Serial.println("\n");

  //Steering data ---------------------------
  steering.Left_Right(value1, value5, encoder_data , wheel);

}
