import rclpy
from rclpy.node import Node

from rione_msgs.msg import Command
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan

from time import sleep

from numpy import *

class Turn(Node):
    def __init__(self):
        super().__init__("Trun")

        self.publisher2cerebrum = self.create_publisher(
            Command,
            "/cerebrum/command",
            10
        )

        self.publisher2sound = self.create_publisher(
            Command,
            "/sound_system/command",
            10
        )

        self.create_subscription(
            Command,
            "/control_system/command",
            self.receiveFlag,
            10
        )

        self.laser_subscription = self.create_subscription(
            LaserScan,
            "/scan",
            self.scan,
            10
        )


        sleep(1)

    def receiveFlag(self, msg):
        if msg.flag == 1:
            if msg.command == "get_distance":
                print("Receive message from {0} with flag:{1} command:{2} content:{3}".format(
                        msg.sender, msg.flag, msg.command, msg.content
                    )
                )

                right = round(sum(self.laser[85*2:95*2])/20, 2)
                left = round(sum(self.laser[265*2:275*2])/20, 2)

                print("right :{0} left:{1}".format(right, left), flush=True)

                if right == 0 or right > left:
                    self.sendFinishFlag("sound", False, "speak", "I stay right side because right distance is longer than left distance.".format(right, left))
                elif left == 0 or left > right:
                    self.sendFinishFlag("sound", False, "speak", "I stay left side because right distance is shorter than left distance.".format(right, left))

    def sendFinishFlag(self, topic, flag, command, content):

        if topic == "sound":
            _message = Command()
            _message.flag = flag
            _message.command = command
            _message.content = content
            _message.sender = "control"

            print(_message, flush=True)

            self.publisher2sound.publish(_message)

    def scan(self, msg):
        self.laser = msg.ranges


def main():
    rclpy.init()

    node = Turn()

    rclpy.spin(node)


if __name__ == "__main__":
    main()
