from typing import Iterator, List
#from rclpy.context import Context
from rclpy.node import Node
#from rclpy.parameter import Parameter
#from rclpy.timer import Timer
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle
import rclpy
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import Pose2D
from builtin_interfaces.msg import Time
#from rcl_interfaces.msg import ParameterDescriptor
import time
from threading import Lock
from rc2024_interfaces.action import ChassisMoveTo
import numpy as np
import math
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
        self.create_publisher(Float64MultiArray,"chassis_mv_cmd",3)
        self.create_subscription(Pose2D,"chassis_actual_pose",self.get_pose_callback)
        self.chassis_moveto_server = ActionServer(
            self, ChassisMoveTo, 'chassis_move_to', self.chassis_moveto_execute
            # ,callback_group=MutuallyExclusiveCallbackGroup()
        )
        self.Mutex = Lock()
        self.P = Pose2D() #actual_pose
        self.planner = planner(num)
    
    def get_pose_callback(self,msg):
        with self.Mutex:
            self.P.x = msg.x
            self.P.y = msg.y
            self.P.theta = msg.theta

    def execute_callback(self, goal_handle: ServerGoalHandle):
        Pr_list = zip(goal_handle.request.xr,goal_handle.request.yr,goal_handle.request.wr)
        feedback_msg = ChassisMoveTo.Feedback()
        dt = 0.01 #10ms
        total_time = 0
        for i,Pr in enumerate(Pr_list):
            Pe = Pose2D()
            feedback_msg.data = float(i/len(Pr_list))
            goal_handle.publish_feedback(feedback_msg)
            while rclpy.ok():
                with self.Mutex:
                    Pe.x = (Pr.x-self.P.x)*math.cos(self.P.theta)+(Pr.y-self.P.y)*math.sin(self.P.theta)
                    Pe.y = (Pr.y-self.P.y)*math.cos(self.P.theta)-(Pr.x-self.P.x)*math.sin(self.P.theta)
                    Pe.theta = Pr.theta-self.P.theta
                # 执行
                pass
                if 0:
                    continue

                if goal_handle.is_cancel_requested:
                    #self.get_logger().info('cancel!')
                    result = ChassisMoveTo.Result()
                    result.time = -1.
                    return result
                
                total_time+=dt
                time.sleep(dt)

        goal_handle.succeed()
        result = ChassisMoveTo.Result()
        result.time = total_time
        return result
    
        
