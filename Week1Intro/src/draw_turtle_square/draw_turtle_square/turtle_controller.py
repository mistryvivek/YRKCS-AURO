#
# Copyright (c) 2024 University of York and others
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0.
# 
# SPDX-License-Identifier: EPL-2.0
#
# Contributors:
#   * Alan Millard - initial contributor
#   * Pedro Ribeiro - revised implementation
#   * Vivek Mistry - Modified to complete square.
#
# Run using:
#      ros2 run turtlesim turtlesim_node
#      ros2 run turtle_draws_square turtle_controller - to make movement.
#      ros2 run turtle_draws_square turtle_listeners - to see messages being sent.
#

import rclpy
from rclpy.node import Node
import time

from geometry_msgs.msg import Twist, Vector3

import random

class TurtleController(Node):

    def __init__(self):

        # We give a name to this node
        super().__init__('turtle_controller')

        # Declare a publisher of type Twist, with topic name '/turtle1/cmd_vel' and queue_size of 10.
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.angular_z = 0.0

        # Create a twist with two vectors, consisting of linear+angular parameters.
        msg = Twist(linear = Vector3(x = 0.0,
                                     y = 1.0,
                                     z = 0.0),
                    angular = Vector3(x = 0.0,
                                      y = 0.0,
                                      z = self.angular_z))

        # Publish the twist
        self.publisher.publish(msg)

        # Output logging info
        self.get_logger().info(f"Publishing: Twist - linear: ({msg.linear.x}, {msg.linear.y}, {msg.linear.z}), angular: ({msg.angular.x}, {msg.angular.y}, {msg.angular.z})")

        time.sleep(1)

        msg = Twist(linear = Vector3(x = 1.0,
                                     y = 0.0,
                                     z = 0.0),
                    angular = Vector3(x = 0.0,
                                      y = 0.0,
                                      z = self.angular_z))

         # Publish the twist
        self.publisher.publish(msg)

         # Output logging info
        self.get_logger().info(f"Publishing: Twist - linear: ({msg.linear.x}, {msg.linear.y}, {msg.linear.z}), angular: ({msg.angular.x}, {msg.angular.y}, {msg.angular.z})")

        time.sleep(1)

        msg = Twist(linear = Vector3(x = 0.0,
                                     y = -1.0,
                                     z = 0.0),
                    angular = Vector3(x = 0.0,
                                      y = 90.0,
                                      z = self.angular_z))

         # Publish the twist
        self.publisher.publish(msg)

        time.sleep(1)

        # Output logging info
        self.get_logger().info(f"Publishing: Twist - linear: ({msg.linear.x}, {msg.linear.y}, {msg.linear.z}), angular: ({msg.angular.x}, {msg.angular.y}, {msg.angular.z})")

        msg = Twist(linear = Vector3(x = -1.0,
                                     y = 0.0,
                                     z = 0.0),
                    angular = Vector3(x = 0.0,
                                      y = 0.0,
                                      z = self.angular_z))

         # Publish the twist
        self.publisher.publish(msg)

        # Output logging info
        self.get_logger().info(f"Publishing: Twist - linear: ({msg.linear.x}, {msg.linear.y}, {msg.linear.z}), angular: ({msg.angular.x}, {msg.angular.y}, {msg.angular.z})")

        time.sleep(1)

def main(args=None):
    rclpy.init(args=args)

    turtle_controller = TurtleController()

    rclpy.spin(turtle_controller)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    turtle_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
