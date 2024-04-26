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

gps_port = find_ports('u-blox GNSS receiver')
baudrate = 9600
csv_file_path = 'gps_data.csv'  # Path to the CSV file

try:
    ser = serial.Serial(gps_port, baudrate, timeout=1)
    s = socket.socket()
    port = 8002
    s.connect(('213.168.5.170', port))
except serial.SerialException as e:
    rospy.logerr("Error: %s", e)

class Wayfinder:
    def __init__(self):
        self.rate = rospy.Rate(10)
        self.lat0 = 58.3428685594
        self.lon0 = 25.5692475361
        self.alt0 = 91.357

        self.starting_point = []
        self.current_location = []
        self.target_location = []

    def status_fix(self):
        try:
            socket_info = s.recv(1024)
            ser.write(socket_info)
        except Exception as e:
            self.get_logger().error(f"Error writing to u-blox device: {e}")

    def get_gps_data(self): #Finding the current location of the robot.
        line = ser.readline().decode('utf-8')
        if line.startswith('$GNGGA'):
            gga_msg = pm.parse(line)
            latitude = gga_msg.latitude
            longitude = gga_msg.longitude
            altitude = gga_msg.altitude
            X, Y = pm.geodetic2enu(latitude, longitude, altitude, self.lat0, self.lon0, self.alt0)
            return X, Y
    
    def gps_trace_starting_point(self):
        for i in data.index:
            if data.at[i, 'X'] is not None: #Finding the first non-empty values and basing the starting point from them.
                self.starting_point = [data.at[i, 'X'], data.at[i, 'Y']]
                return self.starting_point
            
    def navigation_radius(self):
        self.current_location = self.get_gps_data()
        
    
    def wayfinding(self): #Comparing the current location of the robot to the target location. ENU values are in metres!
        while not rospy.is_shutdown():
            self.current_location = self.get_gps_data()
            
