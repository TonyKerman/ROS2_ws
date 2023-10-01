from typing import Iterator, List
from rclpy.context import Context
from rclpy.node import Node
import rclpy
from rclpy.parameter import Parameter
from rclpy.timer import Timer
from sensor_msgs.msg import JointState
from .motor import Motor
from rcl_interfaces.msg import ParameterDescriptor



# class Motor_node(Node):
#     def __init__(self,name:str,reduction_ratio:float):
#         super().__init__(name)
#         #pid_parameter_descriptor = ParameterDescriptor()
#         #self.get_logger().info(f'{rclpy.Parameter.Type.DOUBLE_ARRAY.value}')
         
#         self.declare_parameter('pid_parameters',[1.0,0.0,0.0])
#         self.motor = Motor(self.get_parameter('pid_parameters').value)
#         self.declare_parameter('time_rate',1)
#         time_rate = self.get_parameter('time_rate').value
#         #self.get_logger().info(f'{time_rate}')
#         self.create_timer(1/time_rate,self.timer_callback)

    
#     def timer_callback(self):
#         new_pid_params = self.get_parameter('pid_parameters').value
#         if new_pid_params != self.pid_params:
#             self.get_logger().info(f'change pid parameters to{new_pid_params}')
#         self.motor.pid_parms.reset(new_pid_params)
    
#     def set_speed(speed)
#         pass

class Motor_node(Node):
    def __init__(self,name:str,reduction_ratio:float):
        super().__init__(name)
        #pid_parameter_descriptor = ParameterDescriptor()
        #self.get_logger().info(f'{rclpy.Parameter.Type.DOUBLE_ARRAY.value}')
        self.motor = Motor(name)
        self.declare_parameter('time_rate',1)
        joint_name = name+'_js'
        self.js_pub = self.create_publisher(JointState,joint_name,5)
        time_rate = self.get_parameter('time_rate').value
        #self.get_logger().info(f'{time_rate}')
        self.cnt = 0
        self.create_timer(1/time_rate,self.timer_callback)
        

    
    def timer_callback(self):
        cnt=cnt+1
        time_rate = self.get_parameter('time_rate').value
        self.motor.update(self.get_clock().now().to_msg(),cnt)
        self.js_pub.publish(self.motor.state)
        

         

        


def main():
    rclpy.init() # 初始化rclpy
    node = Motor_node('motor_node')  # 新建一个节点
    
    rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy

