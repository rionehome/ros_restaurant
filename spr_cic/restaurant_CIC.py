import rclpy
from rclpy.node import Node

from rione_msgs.msg import Command

from time import sleep

class CIC(Node):
    def __init__(self):
        super().__init__("CIC")

        self.publisher2control = self.create_publisher(Command, "/control_system/command", 10)
        self.publisher2sound   = self.create_publisher(Command, "/sound_system/command",   10)
        self.publisher2image   = self.create_publisher(Command, "/image_system/command",   10)

        self.create_subscription(Command, "/cerebrum/command", self.receive, 10)

        self.timer = self.create_timer(2.0, self.state)

        self.data = Command()

        sleep(1)

        self.tasks = {
            "1": ["sound",   "count",   "None"],
            "2": ["control", "turn",    180   ],
            "3": ["image",   "capture", "None"],
            "4": ["sound",   "QandA",   5     ],
            "5": ["sound",   "angular", "None"],
            "6": ["sound",   "angular", "None"],
            "7": ["sound",   "angular", "None"],
            "8": ["sound",   "angular", "None"],
            "9": ["sound",   "angular", "None"],
        }

        self.executing = "1"
        self.did = "0"

        print("[*] START SPR", flush=True)

    def state(self):
        for number, task in self.tasks.items():
            self.executing = number
            if self.executing != self.did:
                self.send_with_content(task[0], task[1], task[2])
            self.did = self.executing
            break

    def receive(self, msg):
        print(msg)
        flag = msg.flag

        number = 0
        tasks = None

        for number, task in self.tasks.items():
            break

        if msg.command == task[1]:
            print(self.tasks.pop(self.executing), flush=True)

    def send_with_content(self, topic, command, content):

        msg = Command()
        msg.flag    = True
        msg.command = command
        msg.content = content
        msg.sender  = "cerebrum"

        if topic == "control":
            self.publisher2control.publish(msg)

        elif topic == "sound":
            self.publisher2sound.publish(msg)

        elif topic == "image":
            self.publisher2image.publish(msg)

        else:
            print("[!] Error : No Topic Name {0}".format(topic), flush=True)

def main():
    rclpy.init()

    node = CIC()

    rclpy.spin(node)

if __name__ == "__main__":
    main()
