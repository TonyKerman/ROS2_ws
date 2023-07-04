import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16MultiArray
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

from struct import pack,calcsize
#http://wed.xjx100.cn/news/7599.html?action=onClick
servos_bis = [800, 1155, 400, 700]
angle = [1,1,1,1]

class Controller(Node):
    def __init__(self):
        super().__init__("Controller")
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer,self)
        self.serialMsg_publisher = self.create_publisher(Int16MultiArray,'serial_Msg',3)

    def timer_callback(self):
        try:
            now = rclpy.time.Time()
            #trans = self.tf_buffer.lookup_transform('world','S4',now)
            msg =Int16MultiArray()
            msg.data =[round(angle[i]/0.24+servos_bis[i]) for i in range(len(angle))]
            self.serialMsg_publisher.publish(msg)
            #print(trans)
        except TransformException as ex:
            print(f'can not find{ex}')


    


def main(args=None):
    rclpy.init(args=args)
    controller = Controller()
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()



