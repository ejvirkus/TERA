#!/usr/bin/env python

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import serial
import pynmea2
import socket
import csv
from find_ports import find_ports

gps_port = find_ports('u-blox GNSS receiver')
baudrate = 9600
csv_file_path = 'gps_data.csv'  # Path to the CSV file

try:
    ser = serial.Serial(gps_port, baudrate, timeout=1)
    s = socket.socket()
    port = 8002
    s.connect(('213.168.5.170', port))
except serial.SerialException as e:
    print("Error: %s", e)

class GpsPublisher(Node):
    def __init__(self):
        super().__init__('gps_publisher')
        self.publisher = self.create_publisher(String,'gps_data', 10)
        self.rate = self.create_rate(10)  # 10 Hz
        #self.timer = self.create_timer(0.05, self.publish_gps_data)
        self._loop_rate = self.create_rate(1)
        
        self.csv_file = open(csv_file_path, 'w')  # Open CSV file for writing
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Latitude', 'Longitude', 'Altitude', 'Direction', 'Speed (km/h)'])  # Write header

        # Initialize variables to hold last received GPS data
        self.last_latitude = None
        self.last_longitude = None
        self.last_altitude = None
        self.last_speed = None

    def status_fix(self):
        try:
            socket_info = s.recv(1024)
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
            for _ in range(10):
                line = ser.readline().decode('utf-8')
                if line.startswith('$GNVTG'):
                    vtg_msg = pynmea2.parse(line)
                    speed = vtg_msg.spd_over_grnd_kmph  # Speed in km/h
                    break
                
            print(latitude, longitude, altitude, speed)
            return latitude, longitude, altitude, speed
        return None, None, None, None

    def publish_gps_data(self):
        self.status_fix()
        latitude, longitude, altitude, speed = self.get_gps_data()

        # If no new GPS data is received, use the last received data
        if latitude is None or longitude is None or altitude is None or speed is None:
            latitude = self.last_latitude
            longitude = self.last_longitude
            altitude = self.last_altitude
            speed = self.last_speed
        else:
            # Update last received data
            self.last_latitude = latitude
            self.last_longitude = longitude
            self.last_altitude = altitude
            self.last_speed = speed

        gps_data_str = "{},{},{},{}".format(latitude, longitude, altitude, speed)
        msg = String()
        msg.data = gps_data_str
        self.publisher.publish(msg)
        #self.get_logger().info(msg.data)

        # Write data to CSV file
        self.csv_writer.writerow([latitude, longitude, altitude, speed])
        self.csv_file.flush()  # Ensure data is written to the file immediately
        #self.rate.sleep()
        self._loop_rate.sleep()

def main(args=None):
    rclpy.init(args=args)
    gps_publisher=GpsPublisher()
    rclpy.spin(gps_publisher)
    gps_publisher.csv_file.close()
    gps_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
