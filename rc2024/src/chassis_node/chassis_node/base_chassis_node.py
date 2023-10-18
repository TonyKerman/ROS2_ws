from typing import Iterator, List
#from rclpy.context import Context
from rclpy.node import Node
#from rclpy.parameter import Parameter
#from rclpy.timer import Timer
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle
import rclpy
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion
#from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from builtin_interfaces.msg import Time
#from rcl_interfaces.msg import ParameterDescriptor
#import time
#from threading import Lock
from rc2024_interfaces.action import ChassisMove
import numpy as np
class BlinkPlanner():
    def __init__(self,num:int):
        self.goal = np.zeros(num)
        self.val = np.zeros(num)
    def get_feedback(self,x):
        self.val = np.array(list(x))
    def set_goal(self,goal):
        self.goal = np.array(list(goal))
    def close_goal(self,err):
        err = np.array(list(err))
        return np.abs(self.val-self.goal)-err<0
        
    def run(self):
        return self.goal
    

# class Chassis():
#     def __init__(self):
       
        
#     def set_pos(self,time:Time,point:Point,quaternion:Quaternion):
#         self.pose.header.stamp = time
#         self.pose.pose.position = point
#         self.pose.pose.orientation = quaternion

class Chassis_node(Node):
    def __init__(self,name:str,num:int=3,planner:type[BlinkPlanner]=BlinkPlanner):
        super().__init__(name)
        self.create_publisher(Float64MultiArray,"mv_cmd",3)
        self.action_server_ = ActionServer(
            self, ChassisMove, 'chassis_move', self.execute_callback
            # ,callback_group=MutuallyExclusiveCallbackGroup()
        )

        self.pose = PoseStamped()
        self.planner = planner(num)
    
    def execute_callback(self, goal_handle: ServerGoalHandle):
        pass    
        
    
        
