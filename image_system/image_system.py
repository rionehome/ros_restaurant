import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import Image

from cv_bridge import CvBridge

from time import sleep


class ImageSystem(Node):
    def __init__(self):
        super(ImageSystem, self).__init__('ImageSystem')

        self.senses_publisher = self.create_publisher(
                String,
                'cerebrum/command',
                10
        )

        self.create_subscription(
                String,
                '/image_system/command',
                self.command_callback,
                10
        )

        self.create_subscription(
                Image,
                '/camera/color/image_raw',
                self.get_image,
                10
        )

        self.message = None
        self.command = None
        self._trans_message = String()

        self.bridge = CvBridge()

        sleep(1)


    # recieve a command
    def command_callback(self, msg):
        
        self.command = msg.data
        command = msg.data.split(',')


    # detect waving customer's hand.
    def detect_wavehand(self):
        pass
    
    # get Realsense's data.
    def get_Realsense(self, msg):
        pass
        

    def get_image(self, msg):
        pass

def main():
    rclpy.init()
    node = ImageSystem()
    rclpy.spin(node)


if __name__ == "__main__":
    main()
