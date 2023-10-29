import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from rc2024_interfaces.action import ChassisMove
import time
import random
import numpy as np
from rc2024_interfaces.action import SeizeAndKick
class Example_Client(Node):
    def __init__(self,name):
        super().__init__(name)
        self.action_client_ = ActionClient(self, SeizeAndKick, 'kick_ball')


    def send_goal(self):
        goal_msg = SeizeAndKick.Goal()
        self.action_client_.wait_for_server()
        self._send_goal_future = self.action_client_.send_goal_async(goal=goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)
        
    def goal_response_callback(self, future):
        """收到目标处理结果"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return
        self.get_logger().info('Goal accepted :)')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        """获取结果反馈"""
        result = future.result().result
        self.state = 'stop'
        self.get_logger().info(f'Result{result}')

    def feedback_callback(self, feedback_msg):
        """获取回调反馈"""
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Received feedback: {feedback}')
def main():
    rclpy.init() # 初始化rclpy
    node = Example_Client('example_client_node')  # 新建一个节点
    node.send_goal()
    while rclpy.ok():
        rclpy.spin_once(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy