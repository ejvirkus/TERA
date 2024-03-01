#!/usr/bin/env python3

import rospy
import time
import serial
from std_msgs.msg import Int32
from sensor_msgs.msg import LaserScan

arduino = serial.Serial(port='/dev/ttyACM0', baudrate= 115200, timeout=1)


def send_to_arduino(data):
    arduino.write(data.encode())
    #print("Sent!")
    time.sleep(0.05)

def read_arduino():
    #print('reading')
    info = arduino.readline()
    if info:
        info = info.decode()
        print("Received: ", info)
    else:
        print("No info received\n")

def scan_callback(scan_msg):
    ranges = scan_msg.ranges

    # Extract a specific range of data
    start_mid = 100
    end_mid = 128
    extracted_data = ranges[start_mid:end_mid]

    # Find the minimum value in the extracted data
    min_distance = min(extracted_data)

    # Determine action based on the minimum value
    if min_distance < 1:
        no = '1'
    else:
        no = '0'

    send_to_arduino(no)
    read_arduino()

    #pub = rospy.Publisher('brake', Int32, queue_size=1)
    #pub.publish(no)
    #print(no)


def scan_subscriber():
    rospy.init_node('scan_subscriber', anonymous=True)
    rospy.Subscriber('/scan', LaserScan, scan_callback)
    
    rospy.spin()

if __name__ == '__main__':
    try:
        scan_subscriber()
        
    except rospy.ROSInterruptException:
        print("Failed")
        pass
