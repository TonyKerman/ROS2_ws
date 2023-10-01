from std_msgs.msg import Header
import rclpy
from rclpy.node import Node

class _Time_base_node(Node):
    def __init__(self,name,rate):
        super().__init__(name)
        self.timer = self.create_timer(1/rate,self.timer_callback)
        self.get_logger().info('timer online\n')
        self.timepub = self.create_publisher(Header,'time_base_stamp',1)
            
    def timer_callback(self):
        timestamp = Header()
        timestamp.stamp = self.get_clock().now().to_msg()
        self.timepub.publish(timestamp)



def main(args=None):
    rclpy.init(args=args) # 初始化rclpy
    node = _Time_base_node("time_base_node",10)  # 新建一个节点
    
    rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy

