import rclpy
from rclpy.node import Node

from rione_msgs.msg import Command

from time import sleep

class restaurant(Node):
    def __init__(self):
        super().__init__("restaurant")

        self.publisher2control = self.create_publisher(Command, "/control_system/command", 10)
        self.publisher2sound   = self.create_publisher(Command, "/sound_system/command",   10)
        self.publisher2image   = self.create_publisher(Command, "/image_system/command",   10)

        self.create_subscription(Command, "/cerebrum/command", self.receive, 10)

        self.timer = self.create_timer(2.0, self.state)

        self.data = Command()

        self.msg = Command()

        sleep(1)

        self.tasks = {
            "1": ["cerebrum",  "sleep",          "none"],
            "2": ["control",   "get_distance",   "none"],
            "3": ["sound",     "angular",        "none"],
        }

        self.executing = "1"
        self.did = "0"

        print("[*] START RESTAURANT", flush=True)

    def state(self):
        for number, task in self.tasks.items():
            self.executing = number
            if self.executing != self.did:
                self.send_with_content(task[0], task[1], task[2])
            self.did = self.executing
            break

    def receive(self, msg):
        print("Receive message from {0} with flag:{1} command:{2} content:{3}".format(
                msg.sender, msg.flag, msg.command, msg.content
            ),
            flush=True
        )

        self.msg = msg

        flag = self.msg.flag

        number = 0
        tasks = None

        for number, task in self.tasks.items():
            break

        if self.msg.command == task[1]:
            self.tasks.pop(self.executing)

    def send_with_content(self, topic, command, content):

        msg = Command()
        msg.flag    = True
        msg.command = command
        msg.content = content
        msg.sender  = "cerebrum"

        print("Send messege to {0} with flag:{1} command:{2} content:{3} sender:{4}".format(
                topic, msg.flag, msg.command, msg.content, msg.sender
            ),
            flush=True
        )

        if topic == "control":
            self.publisher2control.publish(msg)

        elif topic == "sound":
            self.publisher2sound.publish(msg)

        elif topic == "image":
            self.publisher2image.publish(msg)

        elif topic == "cerebrum":
            if command == "sleep":
                self._sleep()

        else:
            print("[!] Error : No Topic Name {0}".format(topic), flush=True)

    def _sleep(self):
        sleep(10)
        self.tasks.pop(self.executing)

def main():
    rclpy.init()

    node = restaurant()

    rclpy.spin(node)

if __name__ == "__main__":
    main()
