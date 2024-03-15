#!/usr/bin/env python3

import rospy
#from std_msgs.msg import Int32
from geometry_msgs.msg import Point32
import time
import serial
from find_ports import find_ports
info = [0,0,0]

#Find the port for arduino:
port = find_ports('arduino')
#print(port)

arduino = serial.Serial(port=port, baudrate=115200, timeout=0.5)
print("Booting serial...")
time.sleep(3)
print("Done!")

def callback(data):
    #rospy.loginfo(rospy.get_caller_id() + "Steering %s", data.x)
    info[0] = data.x
    info[1] = data.y
    info[2] = data.z

def listener():
    while not rospy.is_shutdown():
        # Initialize the ROS node
        rospy.init_node('listener', anonymous=True)
        

        # Create publishers for the two integers on the "info" topic
        pub = rospy.Subscriber('info', Point32, callback)
        #info_publisher_2 = rospy.Publisher('info_2', Int32, queue_size=10)
        values = (f"{round(info[0])},{round(info[1])}")
        #print(values)
        inf = str(values)
        #print(info[0])
        arduino.write(bytes(inf, 'utf-8'))
        time.sleep(0.1)
        #print(arduino.readline().decode('utf-8'))
   

if __name__ == '__main__':
    try:
        listener()
    except KeyboardInterrupt:
        print("Closing serial...")
        arduino.close()
    #except rospy.ROSInterruptException:
        #print("Shutting down")
        #arduino.close()
        #pass
