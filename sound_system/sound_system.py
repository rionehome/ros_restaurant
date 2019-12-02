import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from module import module_distance
from module import module_angular
from module import module_pico
from module import module_restaurant

from rione_msgs.msg import Command

class SoundSystem(Node):
    def __init__(self):
        super(SoundSystem, self).__init__('SoundSystem')

        self.command = None

        self.create_subscription(
            Command,
            'sound_system/command',
            self.command_callback,
            10
        )

        self.senses_publisher = self.create_publisher(
            Command,
            'cerebrum/command',
            10
        )

        self.angular_publisher = self.create_publisher(
            Command,
            'control_system/command',
            10
        )

    # recieve a command {Command, Content}
    def command_callback(self, msg):

        # Speak a content
        if 'speak' == msg.command:
            if module_pico.speak(msg.content) == 1:
                self.cerebrum_publisher(0,"speak")

        # Detect right or left
        if 'distance' == msg.command:
            content = msg.content
            self.cerebrum_publisher(False,"get_distance", "none")
            #if module_distance.distance(content) == 1:
            #    self.cerebrum_publisher(0,"distance")

        # Sound localization
        if 'angular' == msg.command:
            self.angular = module_angular.angular()
            if self.temp_angular > 0:
                self.turnnig_publisher(
                    1,"angular",int(self.angular))

        # Start restaurant, content is first or end
        when = ""
        if 'restaurant' == msg.command:
            when = msg.content
            answer = module_restaurant.restaurant(when)
            if str(when) == "first":
                if str(answer) == "restart":
                    self.cerebrum_publisher(0,"restaurant_first","restart")
                else:
                    # content is food's name
                    self.cerebrum_publisher(0,"restaurant_first",str(answer))
            elif str(when) == "mid":
                if answer == 1:
                    self.cerebrum_publisher(0,"restaurant_mid")
            elif str(when) == "end":
                if answer == 1:
                    self.cerebrum_publisher(0,"restaurant_end")

    # Publish a result of an action
    def cerebrum_publisher(self, flag, command, content=""):

        _trans_message = Command()
        _trans_message.flag = flag
        _trans_message.command = command
        _trans_message.content = content
        _trans_message.sender = "sound"

        self.senses_publisher.publish(_trans_message)
        # self.destroy_publisher(self.senses_publisher)

    # Publish a result of an action
    def turnnig_publisher(self, flag, command, content):
        _trans_message = Command()
        _trans_message.flag = flag
        _trans_message.command = command
        _trans_message.content = content
        _trans_message.sender = "sound"

        print()

        self.angular_publisher.publish(_trans_message)
        # self.destroy_publisher(self.senses_publisher)

def main():
    rclpy.init()
    node = SoundSystem()
    rclpy.spin(node)


if __name__ == '__main__':
    main()
