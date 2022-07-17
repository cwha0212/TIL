#!/usr/bin/env/ python3

import sys

from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class ParkingNode(Node):

	def __init__(self):
        super().__init__('parking_node')

        self.publisher = self.create_publisher(Twist, 'skidbot/cmd_vel', 10)

        self.subscriber = self.create_subscription(LaserScan, 'skidbot/scan', self.sub_callback, 10)
        self.subscriber  # prevent unused variable warning
        self.publisher  # prevent unused variable warning

        self.get_logger().info('==== Parking Node Started ====\n')

    def sub_callback(self, msg):
        twist_msg = Twist()
        distance_forward = msg.ranges[360]

        if distance_forward > 1.0:
            self.get_logger().info(f'Distance from Front Object : {distance_forward}')
            twist_msg.linear.x = 1.0
            self.publisher.publish(twist_msg)
			
        else:
            self.get_logger().info("==== Parking Done!!! ====\n")
            twist_msg.linear.x = 0
            self.publisher.publish(twist_msg)
			


def main(args=None):
    rclpy.init(args=args)

    parking_node = ParkingNode()

    try:
        rclpy.spin(parking_node)
    except KeyboardInterrupt:
        print("==== Server stopped cleanly ====")
    except BaseException:
        print("!! Exception in server:", file=sys.stderr)
        raise
    finally:
        rclpy.shutdown()


if __name__ == "__main__":
    main()