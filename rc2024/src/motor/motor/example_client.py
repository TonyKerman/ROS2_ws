import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from rc2024_interfaces.action import MotorRotate
import time

class Example_Client(Node):
    def __init__(self,name):
        super().__init__(name)
        self.action_client_ = ActionClient(self, MotorRotate, 'motor_rotate')
        time.sleep(3)
        self.send_goal()

    def send_goal(self):
        goal_msg = MotorRotate.Goal()
        goal_msg.delta = 5.0
        self.action_client_.wait_for_server()
        self._send_goal_future = self.action_client_.send_goal_async(goal_msg,feedback_callback=self.feedback_callback) 
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
        self.get_logger().info(f'Result: {result.theta}')

    def feedback_callback(self, feedback_msg):
        """获取回调反馈"""
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Received feedback: {feedback.remaining}')
def main():
    rclpy.init() # 初始化rclpy
    node = Example_Client('example_client_node')  # 新建一个节点
    
    rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy