#!/usr/bin/env python3

import rclpy
from geometry_msgs.msg import Point32
import time
import serial
from find_ports import find_ports

info = [0, 0, 0]

# Find the port for Arduino
port = find_ports('arduino')
arduino = serial.Serial(port=port, baudrate=115200, timeout=0.5)
print("Booting serial...")
time.sleep(3)
print("Done!")

def callback(data):
    global info
    info[0] = data.x
    info[1] = data.y
    info[2] = data.z

def listener():
    rclpy.init()
    node = rclpy.create_node('listener')

    # Create a subscriber for the "info" topic
    sub = node.create_subscription(Point32, 'info', callback, 10)

    while rclpy.ok():
        # Send data to Arduino
        values = (f"{round(info[0])},{round(info[1])}")
        inf = str(values)
        arduino.write(bytes(inf, 'utf-8'))
        time.sleep(0.1)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    try:
        listener()
    except KeyboardInterrupt:
        print("Closing serial...")
        arduino.close()