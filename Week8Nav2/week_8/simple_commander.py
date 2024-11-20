# Based on: https://github.com/ros-planning/navigation2/blob/humble/nav2_simple_commander/nav2_simple_commander/example_nav_to_pose.py

import sys

import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from rclpy.duration import Duration
from sensor_msgs.msg import LaserScan
import random
from rclpy.qos import QoSPresetProfiles

from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

from enum import Enum

SCAN_THRESHOLD = 0.5 # Metres per second

SCAN_FRONT = 0

class State(Enum):
    SET_GOAL = 0
    NAVIGATING = 1

class SimpleCommander(Node):

    def __init__(self):
        super().__init__('simple_commander')

        self.state = State.SET_GOAL

        self.navigator = BasicNavigator()

        initial_pose = PoseStamped()
        initial_pose.header.frame_id = 'map'
        initial_pose.header.stamp = self.get_clock().now().to_msg()
        initial_pose.pose.position.x = -2.0
        initial_pose.pose.position.y = -0.5
        initial_pose.pose.orientation.z = 0.0
        initial_pose.pose.orientation.w = 1.0
        self.navigator.setInitialPose(initial_pose)

        self.scan_triggered = [False]

        self.navigator.waitUntilNav2Active()

        self.scan_subscriber = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            QoSPresetProfiles.SENSOR_DATA.value)

        self.timer_period = 0.1 # 100 milliseconds = 10 Hz
        self.timer = self.create_timer(self.timer_period, self.control_loop)
    
    def scan_callback(self, msg):
        # Group scan ranges into 4 segments
        # Front, left, and right segments are each 60 degrees
        # Back segment is 180 degrees
        front_ranges = msg.ranges[331:359] + msg.ranges[0:30] # 30 to 331 degrees (30 to -30 degrees)

        # Store True/False values for each sensor segment, based on whether the nearest detected obstacle is closer than SCAN_THRESHOLD
        self.scan_triggered[SCAN_FRONT] = min(front_ranges) < SCAN_THRESHOLD 


    def control_loop(self):
        self.get_logger().info(f"State: {self.state}")

        match self.state:

            case State.SET_GOAL:

                goal_pose = PoseStamped()
                goal_pose.header.frame_id = 'map'
                goal_pose.header.stamp = self.get_clock().now().to_msg()
                goal_pose.pose.position.x = random.uniform(-3.0, 3.0)
                goal_pose.pose.position.y = random.uniform(-3.0, 3.0)
                goal_pose.pose.orientation.w = 1.0

                self.get_logger().info(f"Coordinates navigating to: {goal_pose.pose.position.x}, {goal_pose.pose.position.y}")

                self.navigator.goToPose(goal_pose)

                self.state = State.NAVIGATING

            case State.NAVIGATING:
                if self.scan_triggered[SCAN_FRONT]:
                    self.state = State.SET_GOAL
                    return

                if not self.navigator.isTaskComplete():
                    feedback = self.navigator.getFeedback()
                    print('Estimated time of arrival: ' + '{0:.0f}'.format(Duration.from_msg(feedback.estimated_time_remaining).nanoseconds / 1e9) + ' seconds.')
                else:

                    result = self.navigator.getResult()

                    if result == TaskResult.SUCCEEDED:
                        print('Goal succeeded!')
                    elif result == TaskResult.CANCELED:
                        print('Goal was canceled!')
                    elif result == TaskResult.FAILED:
                        print('Goal failed!')
                    else:
                        print('Goal has an invalid return status!')

            case _:
                pass

    def destroy_node(self):
        self.get_logger().info(f"Shutting down")
        self.navigator.lifecycleShutdown()
        super().destroy_node()
        

def main(args=None):

    rclpy.init(args = args)

    node = SimpleCommander()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except ExternalShutdownException:
        sys.exit(1)
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()