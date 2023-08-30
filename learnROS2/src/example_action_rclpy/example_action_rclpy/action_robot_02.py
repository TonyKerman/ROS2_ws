#!/usr/bin/env python3

import time
# 导入rclpy相关库
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle
# 导入接口
from robot_control_interfaces.action import MoveRobot
# 导入机器人类
from example_action_rclpy.robot import Robot
#from rclpy.executors import MultiThreadedExecutor
#from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

class ActionRobot02(Node):
    """机器人端Action服务"""

    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info(f"节点已启动：{name}!")
        
def main(args=None):
    """主函数"""
    rclpy.init(args=args)
    action_robot_02 = ActionRobot02("action_robot_02")
    # 采用多线程执行器解决rate死锁问题
    # executor = MultiThreadedExecutor()
    # executor.add_node(action_robot_02)
    # executor.spin()
    rclpy.spin(action_robot_02)
    rclpy.shutdown()
