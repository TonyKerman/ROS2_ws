from typing import Iterator, List
from rclpy.context import Context
from rclpy.node import Node
import rclpy

from rclpy.parameter import Parameter
from rclpy.timer import Timer
from sensor_msgs.msg import JointState
from .motor import Motor
from rcl_interfaces.msg import ParameterDescriptor
import time
from threading import Lock
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle
from rc2024_interfaces.action import MotorRotate
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
class BlinkPlanner():
    def __init__(self):
        self.goal = 0
        self.val = 0
    def feedback(self,x):
        self.val = x
    def set_goal(self,goal):
        self.goal = goal
    def close_goal(self,err):
        return abs(self.val-self.goal)<=err
    def run(self):
        return self.goal
    


class Motor_node(Node):
    def __init__(self,name:str):
        super().__init__(name)

        self.state = JointState()
        self.state.name =['joint1']
        self.js_feedback_sub = self.create_subscription(JointState,'joint_states',self.sub_callback,3)
        self.joint_cmd =JointState()
        self.joint_cmd.name= ['joint1']
        self.joint_cmd_pub = self.create_publisher(JointState,'joint_cmd',1)
        self.Mutex = Lock()
        self.planner = BlinkPlanner
        self.action_server_ = ActionServer(
            self, MotorRotate, 'motor_rotate', self.execute_callback
            # ,callback_group=MutuallyExclusiveCallbackGroup()
        )

    def execute_callback(self, goal_handle: ServerGoalHandle):
        self.planner.set_goal(goal_handle.requsest.delta)
        
        while rclpy.ok():
            with self.Mutex:
                self.planner.feedback(self.state.position)
            if self.planner.close_goal(self.planner.val,0.1):
                 goal_handle.succeed()
                 result = MotorRotate.Result()
                 result.theta = self.planner.val
                 return result
            if goal_handle.is_cancel_requested:
                result = MotorRotate.Result()
                result.theta = self.planner.val
                return result
            
            self.joint_cmd.position=[float(self.run())]
            self.joint_cmd_pub.publish(self.joint_cmd)
            time.sleep(0.1)


        
    
    def sub_callback(self,msg):
        for i,name in enumerate(msg.name):
            if name == self.state.name:
                with self.Mutex:
                    self.state.position = msg.position[i]
                    self.state.velocity =msg.velocity[i]
                    self.state.effort = msg.effort[i]
    # def timer_callback(self):
    #     self.motor.update(self.get_clock().now().to_msg())
    #     self.js_pub.publish(self.motor.state)
        


def main():
    rclpy.init() # 初始化rclpy
    node = Motor_node('motor_node')  # 新建一个节点
    
    rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy

