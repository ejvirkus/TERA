#!/usr/bin/env python3
import serial
import time
import rospy
from std_msgs.msg import Int32
import struct
import numpy as np

info = [0, 0 ,0]

arduino = serial.Serial(port='/dev/ttyACM0', timeout=0.01, baudrate=115200)
time.sleep(2) #wait for arduino
print("Ready!")
def read():

    #print(f"steering: {data.data}")
    #send = data.data
    packed = struct.pack('<HHH', *info)
    #packed = info.astype('<u2').tostring()
    #print("struct")
    
    arduino.write(packed)
    time.sleep(0.4)
    arduino.flush()
    print("written")
    print(packed.hex())
    #time.sleep(0.1)
    return

def read_steering(data):
    info[0] = data.data

def read_throttle(data):
    info[1] = data.data

def read_brake(data):
    info[2] = data.data

#def listener():

while True:
    rospy.init_node('listener', anonymous=True)
    steering = rospy.Subscriber('steering', Int32, read_steering)
    throttle = rospy.Subscriber('throttle', Int32, read_throttle)
    brake = rospy.Subscriber('brake', Int32, read_brake)

    #ard = arduino.read()
    #print(ard)
    #print(arduino.read())
    read()
    #print("looped")
    
    #rospy.spin()

#if __name__ == '__main__':
#    listener()