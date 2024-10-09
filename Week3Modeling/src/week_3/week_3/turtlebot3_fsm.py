import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist, Vector3

class TurtleController(Node): 
    def __init__(self):
        self.FORWARD_MSG = Twist(linear = Vector3(x = 1.0,
                                             y = 0.0,
                                             z = 0.0),
                            angular = Vector3(x = 0.0,
                                              y = 0.0,
                                              z = 0.0))
        
        self.TURN_MSG = Twist(linear = Vector3(x = 0.0,
                                          y = 0.0,
                                          z = 0.0),
                         angular = Vector3(x = 0.0,
                                           y = 0.0,
                                           z = 1.5))
         
        super().__init__('turtlebot3_fsm')

        # Declare a publisher of type Twist, with topic name '/turtle1/cmd_vel' and queue_size of 10.
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        # Setup a periodic callback
        timer_period = 2  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.state = "FORWARD"

    def timer_callback(self):
        match self.state:
            case "FORWARD":
                self.publisher.publish(self.FORWARD_MSG)
                self.get_logger().info(f"Publishing: Twist - linear: ({self.FORWARD_MSG.linear.x}, {self.FORWARD_MSG.linear.y}, {self.FORWARD_MSG.linear.z}), angular: ({self.FORWARD_MSG.angular.x}, {self.FORWARD_MSG.angular.y}, {self.FORWARD_MSG.angular.z})")
                self.state = "TURN"
            case "TURN":
                self.publisher.publish(self.TURN_MSG)
                self.get_logger().info(f"Publishing: Twist - linear: ({self.TURN_MSG.linear.x}, {self.TURN_MSG.linear.y}, {self.TURN_MSG.linear.z}), angular: ({self.TURN_MSG.angular.x}, {self.TURN_MSG.angular.y}, {self.TURN_MSG.angular.z})")
                self.state = "FORWARD"
            case _:
                pass

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

       
        

    