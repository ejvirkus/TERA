import rclpy
from rclpy.node import Node
import serial
import struct
import time

from std_msgs.msg import String
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'tera_teleop',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        info = msg.data.split(",")
        print(info)
        sent = arduino.write(struct.pack("2f", info[0], info[1]))
        time.sleep(0.01)
        #self.get_logger().info('I heard: "%s"' % msg.data)



def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
