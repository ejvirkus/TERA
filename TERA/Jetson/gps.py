#!/usr/bin/env python

import rospy
from std_msgs.msg import String

import serial
import pynmea2
import time
import csv
from find_ports import find_ports

gps_port = find_ports('u-blox GNSS receiver')
baudrate = 9600
csv_file_path = 'gps_data.csv'  # Path to the CSV file

try:
    ser = serial.Serial(gps_port, baudrate, timeout=1)
except serial.SerialException as e:
    rospy.logerr("Error: %s", e)

class GpsPublisher:
    def __init__(self):
        rospy.init_node('gps_publisher', anonymous=True)
        self.publisher = rospy.Publisher('gps_data', String, queue_size=10)
        self.rate = rospy.Rate(10)  # 10 Hz
        
        self.csv_file = open(csv_file_path, 'w')  # Open CSV file for writing
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Latitude', 'Longitude', 'Speed (km/h)'])  # Write header

    def get_gps_data(self):
        line = ser.readline().decode('utf-8')
        if line.startswith('$GNGGA'):
            gga_msg = pynmea2.parse(line)
            latitude = gga_msg.latitude
            longitude = gga_msg.longitude
            speed = None

            # Find corresponding speed message
            while True:
                line = ser.readline().decode('utf-8')
                if line.startswith('$GNVTG'):
                    vtg_msg = pynmea2.parse(line)
                    speed = vtg_msg.spd_over_grnd_kmph  # Speed in km/h
                    break
            print(latitude, longitude, speed)
            return latitude, longitude, speed
        return None, None, None

    def publish_gps_data(self):
        while not rospy.is_shutdown():
            latitude, longitude, speed = self.get_gps_data()
            #if latitude is not None and longitude is not None and speed is not None:
            gps_data_str = "{},{},{}".format(latitude, longitude, speed)
            self.publisher.publish(gps_data_str)
            rospy.loginfo(gps_data_str)
            
            # Write data to CSV file
            self.csv_writer.writerow([latitude, longitude, speed])
            self.csv_file.flush()  # Ensure data is written to the file immediately

            self.rate.sleep()  # Enforce the publishing rate

if __name__ == '__main__':
    try:
        gps_publisher = GpsPublisher()
        gps_publisher.publish_gps_data()
    except KeyboardInterrupt:
        csv_file_path.close()
