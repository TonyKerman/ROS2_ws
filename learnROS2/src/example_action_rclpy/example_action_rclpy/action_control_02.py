import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
# 导入Action接口
from robot_control_interfaces.action import MoveRobot

class ActionControl02(Node):
    """Action客户端"""

    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info(f"节点已启动：{name}!")

def main(args=None):
    """主函数"""
    rclpy.init(args=args)
    action_robot_02 = ActionControl02("action_control_02")
    rclpy.spin(action_robot_02)
    rclpy.shutdown()
