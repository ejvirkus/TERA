#!/usr/bin/env python3

import rospy
#from std_msgs.msg import Int32
from geometry_msgs.msg import Point32

def publish_info():
    # Initialize the ROS node
    rospy.init_node('info_publisher', anonymous=True)

    # Create publishers for the two integers on the "info" topic
    pub = rospy.Publisher('info_1', Point32, queue_size=10)
    #info_publisher_2 = rospy.Publisher('info_2', Int32, queue_size=10)

    # Create a Point32 message
    info_msg = Point32()

    # Rate at which to publish messages (in Hz)
    rate = rospy.Rate(10)  # 1 Hz

    while not rospy.is_shutdown():
        # Publish the first integer
        info_1 = 42  # Change this value as needed
        info_msg.x =info_1
        
        # Publish the second integer
        info_2 = 99  # Change this value as needed
        info_msg.y = info_2

        pub.publish(info_msg)
        # Log information for debugging
        #rospy.loginfo("Published: info_1=%s, info_2=%s", info_1, info_2)

        # Wait for the next iteration
        rate.sleep()

if __name__ == '__main__':
    try:
        publish_info()
    except rospy.ROSInterruptException:
        pass
