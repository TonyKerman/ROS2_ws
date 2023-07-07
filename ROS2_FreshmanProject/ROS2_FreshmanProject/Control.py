import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16MultiArray
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

from struct import pack,calcsize
#http://wed.xjx100.cn/news/7599.html?action=onClick
servos_bis = [775, 1155, 400, 700]


class Controller(Node):
    def __init__(self):
        super().__init__("controller")
        self.timer = self.create_timer(0.2, self.timer_callback)
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer,self)
        self.serialMsg_publisher = self.create_publisher(Int16MultiArray,'serial_Msg',3)
        self.declare_parameter("target_angles",[0,0,0,0])
        self.target_angles = [0,0,0,0]
        self.a = 0
        self.s = 0

    def timer_callback(self):
        try:
            now = rclpy.time.Time()
            #trans = self.tf_buffer.lookup_transform('world','S4',now)
            msg =Int16MultiArray()
            msg.data =[round(self.target_angles[i]/0.24+servos_bis[i]) 
                       for i in range(len(self.target_angles))]
            self.serialMsg_publisher.publish(msg)
            print(msg.data)
        except TransformException as ex:
            print(f'can not find{ex}')
        #self.target_angles = self.get_parameter("target_angles").value
        if self.s == 0:
            if self.a>-150:
                self.a-=5
            else:
                self.s = 1
        else:
            if self.a<-30:
                self.a+=5
            else:
                self.s = 0
        
        self.target_angles = [0,-45,0,self.a]

    


def main(args=None):
    rclpy.init(args=args)
    controller = Controller()
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()



