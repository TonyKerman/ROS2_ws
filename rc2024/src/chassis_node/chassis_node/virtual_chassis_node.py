from rclpy.action.server import ServerGoalHandle
from .base_chassis_node import BlinkPlanner
from .base_chassis_node import Chassis_node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import TransformStamped,Transform
import rclpy
from tf2_ros import TransformBroadcaster
from time import sleep
from threading import Lock
from rc2024_interfaces.action import ChassisMove
import numpy as np
from geometry_msgs.msg import Quaternion,Pose2D,Pose
import tf2_geometry_msgs as tf
from typing import Iterable
from scipy.spatial.transform import Rotation


class Virtualodem():
    def __init__(self) -> None:
        self.pose2d = np.zeros(3)
        #self.pose = Pose()
        self.transform = Transform()
        self._update_transfrom()
        #self.orientation = np.array([1.,0.,0.,0.])
        
    def change_pose(self,dp:np.ndarray):
        self.pose2d+=dp
        self._update_transfrom()
        
    def _update_transfrom(self):
        R = Rotation.from_euler('z',self.pose2d[2])
        quat = R.as_quat()
        self.transform.translation.x=self.pose2d[0]
        self.transform.translation.y=self.pose2d[1]
        self.transform.translation.z=0.
        self.transform.rotation.w=quat[3]
        self.transform.rotation.x=quat[0]
        self.transform.rotation.y=quat[1]
        self.transform.rotation.z=quat[2]

class VirtualChassis():
    def __init__(self,odem:type(Virtualodem)) -> None:
        self.odem = odem()
        self.last_cmd = np.zeros(3)
    def move(self,cmd:np.ndarray):
        self.odem.change_pose(self.last_cmd)
        self.last_cmd = cmd/3
    def moveto(self,cmd:np.ndarray):
        return self.move(cmd-self.odem.pose2d)
         
class VirtualChassis_node(Chassis_node):
    def __init__(self, name: str,num:int=3):
        super().__init__(name,num)
        self.timer_rate = 2
        #
        self.chassis = VirtualChassis(Virtualodem)
        self.tf_publisher = TransformBroadcaster(self)
        self.pos = TransformStamped()
        self.pos.header.frame_id = 'map'
        self.pos.child_frame_id = 'base_link'
        
        #
    def execute_callback(self, goal_handle: ServerGoalHandle):
        goal = np.array([goal_handle.request.dx,
                      goal_handle.request.dy,
                      goal_handle.request.omega])

        total_time = 0
        self.planner.set_goal(goal)
        while rclpy.ok():
            goal = self.planner.run()
            #self.get_logger().info(f'goal:{goal}')
            #
            pos = self.chassis.odem.pose2d 
            self.planner.get_feedback(pos)
            self.chassis.moveto(goal)
            self.pos.header.stamp = self.get_clock().now().to_msg()
            self.pos.transform=self.chassis.odem.transform
            self.tf_publisher.sendTransform(self.pos)
            #
            
            if np.all(self.planner.close_goal((0.1,0.1,0.1))):
                goal_handle.succeed()
                result = ChassisMove.Result()
                result.time = total_time
                #self.get_logger().info('success!')
                return result
            if goal_handle.is_cancel_requested:
                #self.get_logger().info('cancel!')
                result = ChassisMove.Result()
                result.time = total_time
                return result
            #

            self.get_logger().info(f'running{pos}')
            sleep(1/self.timer_rate)
            total_time += 1/self.timer_rate


            

def main():
    rclpy.init() # 初始化rclpy
    node = VirtualChassis_node('VirtualChassis_node')  # 新建一个节点
    rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy