#!/usr/bin/env python

import rospy
from std_msgs.msg import String

import pandas as pd
import serial
import pynmea2 as pm
import numpy as np
import math
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

        self.current_location = []
        self.target_location = []
        self.navigation_square = np.array([], [])
        self.allowed_error = 1
        self.min_dist = None

    def status_fix(self): # Getting a gps position fix from the base station
        try:
            socket_info = s.recv(1024)
            ser.write(socket_info)
        except Exception as e:
            self.get_logger().error(f"Error writing to u-blox device: {e}")

    def get_gps_data(self): # Finding the current location of the robot.
        line = ser.readline().decode('utf-8')
        if line.startswith('$GNGGA'):
            gga_msg = pm.parse(line)
            latitude = gga_msg.latitude
            longitude = gga_msg.longitude
            altitude = gga_msg.altitude
            X, Y = pm.geodetic2enu(latitude, longitude, altitude, self.lat0, self.lon0, self.alt0)
            return X, Y
            
    def get_navigation_square(self):  # Calculating the square in which the robot will not search for a target location.
        self.current_location = self.get_gps_data()
        self.navigation_square = np.array([self.get_gps_data - self.allowed_error], [self.get_gps_data + self.allowed_error])
        return self.navigation_square
    
    def get_target_location(self): # Acquiring the closest or next point to which to move
        if self.target_location == []: # If there is no target location, the program finds the closest point to the robot.
            for x in data.index:
                current_min_dist = math.dist(data.at[x], self.get_gps_data()) # Iterating through all points 

                if self.min_dist == None or current_min_dist < self.min_dist: # Assigning closest point
                    self.min_dist = current_min_dist
        else:
            pass
        return self.target_location

        
    
    ''' The robot will be placed anywhere near the recorded trace and must complete the track starting from the closest point.
        If the closest point is the finish, it must simply drive to the finish. The allowed error will be made smaller 
        and the endgoal is for it to have almost zero error.
    '''
    
    def wayfinding(self):
        while not rospy.is_shutdown():
            self.current_location = self.get_gps_data()