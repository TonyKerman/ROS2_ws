from typing import Iterator
import rclpy
from rclpy.node import Node
from rclpy.timer import Timer
# 1.导入消息类型JointState
from sensor_msgs.msg import JointState
from geometry_msgs.msg import TransformStamped
from std_msgs.msg import Float32MultiArray
from tf2_ros import StaticTransformBroadcaster
from queue import Queue
from scipy.spatial.transform import Rotation
import numpy as np
import time
from std_msgs.msg import Float32


class ArmDisplayNode(Node):
    def __init__(self,name):
        super().__init__(name)
        self.create_subscription(JointState,'joint_states',self.joint_sub_callback,3)
        self.joint_state_pub = self.create_publisher(JointState,'joint_cmd',3)
        self.joint_queue = Queue(3)
        #self.servo_open = Float32()

        static_tf_publisher = StaticTransformBroadcaster(self)
        R = Rotation.from_euler('xyz',(np.pi/2,0,0))
        static_tf_publisher.sendTransform(
            self.quat_to_TF('world','base_link', 0, 0, 0, R.as_quat()))
        self.create_timer(0.5,self.timer_callback)
        
    def timer_callback(self):
        pass

    def joint_sub_callback(self,msg):
        self.get_logger().info(f'received:{msg.position}')
        joint_cmd  = JointState()
        joint_cmd.position=msg.position
        self.joint_state_pub.publish(joint_cmd)
        #self.joint_queue.put(msg)
 
    def quat_to_TF(self, A: str, B: str, tx: float, ty: float, tz: float, q: list):
        if len(q) != 4:
            raise IndexError('Quaternion must be a list of 4 elements')
        T = TransformStamped()
        T.header.stamp = self.get_clock().now().to_msg()
        T.header.frame_id = A
        T.child_frame_id = B
        T.transform.translation.x = float(tx)
        T.transform.translation.y = float(ty)
        T.transform.translation.z = float(tz)
        T.transform.rotation.x = q[0]
        T.transform.rotation.y = q[1]
        T.transform.rotation.z = q[2]
        T.transform.rotation.w = q[3]
        return T


   

def main(args=None):
    rclpy.init(args=args) # 初始化rclpy
    node = ArmDisplayNode("R1_Arm")  # 新建一个节点dd
    rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy