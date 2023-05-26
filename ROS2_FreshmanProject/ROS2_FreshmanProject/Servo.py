import rclpy
from rclpy.node import Node
from std_msgs.msg import String,Float32MultiArray

class Servo():

    def __init__(self,bis:int):
        self.bis = bis
        self.pos = 0
        self.target = 0
        #self.minpos
        #self maxpos


class Servo_Controler(Node):

    def __init__(self,bis:int):
        super().__init__('Servo_Controler')

        
        self.subscription = self.create_subscription(
            String,
            'serial_data',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(
            Float32MultiArray,
            'servo_pos',
            10
        )
        def to_angle(self,pos,bis)->float:
            return (pos - bis)*0.24
        
        def listener_callback(self, msg):
            res =self.mDecode_ServoMsg(msg.data)
            if(res):
                self.get_logger().info('Serial Data recived: "%s"' % str(res))
                n =4
                bis = [800,1155,400,700]
                angles = [self.to_angle(res[i],bis[i]) for i in range(n)]
                arr_f = Float32MultiArray()
                arr_f.data =angles
                self.publisher.publish(arr_f)
                self.get_logger().info('Servo Pos published: "%s"' % str(angles))

        def mDecode_ServoMsg(self,rawData):
                l = [rawData[i:i+2] for i in range(0,len(rawData),2)]
                header = '11'
                if l[0] == header:
                    l = l[1:]
                    val =[]
                    for i in range(0,len(l),2):
                        val.append(int(l[i]+l[i+1],16))
                    return val
                return 0
        
def main(args =None):
    rclpy.init(args=args)
    servoControler = Servo_Controler()
    rclpy.spin(servoControler)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    servoControler.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()