#!/usr/bin/env python

import rospy
from std_msgs.msg import String

import serial
import pynmea2
import time
import socket
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
        self.csv_writer.writerow(['Latitude', 'Longitude', 'Altitude', 'Direction', 'Speed (km/h)'])  # Write header

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
            gga_msg = pynmea2.parse(line)
            latitude = gga_msg.latitude
            longitude = gga_msg.longitude
            altitude = gga_msg.altitude
            speed = None
            

            # Find corresponding speed message
            while True:
                line = ser.readline().decode('utf-8')
                if line.startswith('$GNVTG'):
                    vtg_msg = pynmea2.parse(line)
                    speed = vtg_msg.spd_over_grnd_kmph  # Speed in km/h
                    break
                
                elif line.startswith('$GPGSV'):
                    gnss_msg = pynmea2.parse(line)
                    direction = gnss_msg.azimuth
                    break
                
            print(latitude, longitude, altitude, speed, direction)
            return latitude, longitude, altitude, speed, direction
        return None, None, None, None, None

    def publish_gps_data(self):
        while not rospy.is_shutdown():
            self.status_fix()
            latitude, longitude, altitude, speed, direction = self.get_gps_data()
            #if latitude is not None and longitude is not None and speed is not None:
            gps_data_str = "{},{},{},{},{}".format(latitude, longitude, altitude, speed, direction)
            self.publisher.publish(gps_data_str)
            rospy.loginfo(gps_data_str)
            
            # Write data to CSV file
            self.csv_writer.writerow([latitude, longitude, altitude, speed, direction])
            self.csv_file.flush()  # Ensure data is written to the file immediately

            self.rate.sleep()  # Enforce the publishing rate

if __name__ == '__main__':
    try:
        gps_publisher = GpsPublisher()
        gps_publisher.publish_gps_data()
    except KeyboardInterrupt:
        csv_file_path.close()
