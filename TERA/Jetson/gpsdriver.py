#!/usr/bin/env python

import rospy
from std_msgs.msg import String

import pandas as pd
import serial
import pynmea2 as pm
import time
import socket
import csv
from find_ports import find_ports

data = pd.read_csv("C:\Users\emilj\OneDrive\Documents\GitHub\TERA\gps_ENU.csv", header=0, usecols=['X', 'Y'])

lat0, lon0, alt0 = 58.3428685594, 25.5692475361, 91.357

gps_port = find_ports('u-blox GNSS receiver')
baudrate = 9600
csv_file_path = 'gps_data.csv'  # Path to the CSV file

try:
    ser = serial.Serial(gps_port, baudrate, timeout=1)
except serial.SerialException as e:
    rospy.logerr("Error: %s", e)

class Wayfinder:
    def __init__(self):
        self.rate = rospy.Rate(10)

    def gps_base_tcp(self):
        s = socket.socket()
        port = 8002
        s.connect(('213.168.5.170', port))
        return s.recv(1024)

    def status_fix(self):
        try:
            socket_info = self.gps_base_tcp()
            ser.write(socket_info)
        except Exception as e:
            self.get_logger().error(f"Error writing to u-blox device: {e}")

        def get_gps_data(self):
            line = ser.readline().decode('utf-8')
            if line.startswith('$GNGGA'):
                gga_msg = pm.parse(line)
                latitude = gga_msg.latitude
                longitude = gga_msg.longitude
                altitude = gga_msg.altitude
                X, Y, Z = pm.geodetic2enu(latitude, longitude, altitude, lat0, lon0, alt0)
                return X, Y