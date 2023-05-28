import rclpy
from rclpy.node import Node
from std_msgs.msg import String,Float32MultiArray


class SerialHandler(Node):

    def __init__(self):
        super().__init__('serial_handler')

        '''
        格式:
            元素0:类型 ('33'代表是mpu数据)
            元素1:剩余长度
            元素[2:]:内容(数据1高八位+数据1低八位+数据2高八位+......)
        '''
        self.subscription = self.create_subscription(
            String,
            'serial_data',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.publisher = self.create_publisher(
            Float32MultiArray,
            'pose_angles',
            10
        )
    
    def mDecode_MpuMsg(self, data):
        l = [rawData[i:i+2] for i in range(0,len(rawData),2)]
        header = '33'
        if l[0] == header:
            l = l[2:]
            val =[]
            for i in range(0,len(l),2):
                val.append(int(l[i]+l[i+1],16))
            return val
        return 0
    
    def listener_callback(self, msg):
        
        if(res):
            self.get_logger().info('Serial Data recived: "%s"' % str(res))
            arr_f = Float32MultiArray()
            # arr_f.data =angles
            # self.publisher.publish(arr_f)
            # self.get_logger().info('Servo Pos published: "%s"' % str(angles))

    

        return 0

def main(args =None):
    rclpy.init(args=args)
    serial_handler = SerialHandler()
    rclpy.spin(serial_handler)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    serial_handler.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()