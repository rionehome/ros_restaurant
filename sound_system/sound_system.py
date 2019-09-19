import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from module import module_angular
from module import module_speak
from module import module_restaurant

from std_msgs.msg import String
from time import sleep

class SoundSystem(Node):
    def __init__(self):
        super(SoundSystem, self).__init__('SoundSystem')

        self.command = None

        self.create_subscription(
            String, 'sound_system/command',
            self.command_callback
        )

    # recieve a command {Command, Content}
    def command_callback(self, msg):

        self.command = msg.data
        command = msg.data.split(',')

        # Speak a content
        if 'speak' == command[0].replace('Command:', ''):
            if module_speak.speak(command[1].replace('Content:', '')) == 1:
                self.cerebrum_publisher('Return:1,Content:None')

        # Sound localization
        if 'angular' == command[0].replace('Command:', ''):
            self.angular = module_angular.angular()
            if self.temp_angular > 0:
                # "Return:1,Content:angular"
                self.cerebrum_publisher(
                    'Return:1,Content:'+str(self.angular))

        # Start restaurant, content is first or end
        when = ""
        if 'restaurant' == command[0].replace('Command:', ''):
            when = command[1].replace('Content:', '')
            answer = module_restaurant.restaurant(when)
            if str(when) == "first":
                if str(answer) == "restart":
                    self.cerebrum_publisher('Retern:0,Content:restart')
                else:
                    # content is food's name
                    self.cerebrum_publisher('Retern:0,Content:'+str(answer))
            elif str(when) == "end":
                if answer == 1:
                    self.cerebrum_publisher('Retern:0,Content:None')

    # Publish a result of an action
    def cerebrum_publisher(self, message):
        self.senses_publisher = self.create_publisher(
            String, 'cerebrum/command'
        )

        sleep(2)

        _trans_message = String()
        _trans_message.data = message

        self.senses_publisher.publish(_trans_message)
        # self.destroy_publisher(self.senses_publisher)


def main():
    rclpy.init()
    node = SoundSystem()
    rclpy.spin(node)


if __name__ == '__main__':
    main()
