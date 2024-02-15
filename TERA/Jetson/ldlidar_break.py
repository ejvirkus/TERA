#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32
from sensor_msgs.msg import LaserScan

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
        no = 100
    else:
        no = 0

    pub = rospy.Publisher('brake', Int32, queue_size=1)
    pub.publish(no)
    print(no)


def scan_subscriber():
    rospy.init_node('scan_subscriber', anonymous=True)
    rospy.Subscriber('/scan', LaserScan, scan_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        scan_subscriber()
    except rospy.ROSInterruptException:
        pass
