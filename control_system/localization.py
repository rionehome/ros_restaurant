import rclpy
from rclpy.node import Node

from rione_msgs.msg import Command

from time import sleep

from numpy import *

class Localization(Node):
    def __init__(self):
        super().__init__("Trun")

        self.publisher2cerebrum = self.create_publisher(
            Command,
            "/cerebrum/command",
            10
        )

        self.create_subscription(
            Command,
            "/control_system/command",
            self.receiveFlag,
            10
        )

        sleep(1)


    def receiveFlag(self, msg):
        if msg.flag == 1:
            if msg.command == "localization":
                print("Receive message from {0} with flag:{1} command:{2} content:{3}".format(
                        msg.sender, msg.flag, msg.command, msg.content
                    )
                )

                print("Start localization.", flush=True)

                self.sendFinishFlag(msg.sender, False, "localization", "none")
        

    def sendFinishFlag(self, topic, flag, command, content):

        if topic == "cerebrum":

            _message = Command()
            _message.flag = flag
            _message.command = command
            _message.content = content
            _message.sender = "control"

            self.publisher2cerebrum.publish(_message)


def main():
    rclpy.init()

    node = Localization()

    rclpy.spin(node)


if __name__ == "__main__":
    main()
