
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle
# 1.导入消息类型JointState
from sensor_msgs.msg import JointState
from geometry_msgs.msg import TransformStamped
from tf2_ros import StaticTransformBroadcaster
from scipy.spatial.transform import Rotation
import numpy as np
import time
from rc2024_interfaces.action import SeizeAndKick


class ArmTestNode(Node):
    def __init__(self,name):
        super().__init__(name)
        self.joint_cmd_pub = self.create_publisher(JointState,'joint_cmd',3)
        self.joint_state_pub = self.create_publisher(JointState,'joint_states',3)
        self.tgt_js = JointState()
        self.tgt_js.name=['joint1','joint2','joint3']
        #self.joint_queue = Queue(3)
        #self.servo_open = Float32()

        static_tf_publisher = StaticTransformBroadcaster(self)
        R = Rotation.from_euler('xyz',(np.pi/2,0,0))
        static_tf_publisher.sendTransform(
            self.quat_to_TF('world','base_link', 0, 0, 0, R.as_quat()))
        self.action_server_ = ActionServer(
            self, SeizeAndKick, 'kick_ball', self.kick_ball_execute
            # ,callback_group=MutuallyExclusiveCallbackGroup()
        )

    def kick_ball_execute(self, goal_handle: ServerGoalHandle):
        cnt_ms = 0
        tgt_list = [
                {'time':1000,'pos':[5.25,1.16,1.3]},
                {'time':1200,'pos':[5.25,1.16,0.3]},
                {'time':1500,'pos':[3.53,2.01,0.3]},
                {'time':2400,'pos':[1.94,-1.6,0.3]},
                {'time':2800,'pos':[1.21,-2.01,0.3]},
                {'time':3000,'pos':[1.21,-2.01,1.3]},
                {'time':4000,'pos':[1.21,-2.01,1.3]},]
        for i in range(len(tgt_list)):
            while cnt_ms<tgt_list[i]['time']*1.5:
                self.tgt_js.position=tgt_list[i]['pos']
                joint_cmd  = JointState()
                joint_cmd.position=self.tgt_js.position
                self.joint_cmd_pub.publish(joint_cmd)
                self.tgt_js.header.stamp =  self.get_clock().now().to_msg()
                self.joint_state_pub.publish(self.tgt_js)
        
                if goal_handle.is_cancel_requested:
                    #self.get_logger().info('cancel!')
                    result = SeizeAndKick.Result()
                    result.time = cnt_ms
                    return result
                cnt_ms +=100
                time.sleep(0.1)
        
        goal_handle.succeed()
        result = SeizeAndKick.Result()
        result.time = cnt_ms
        return result
        

 
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
    node = ArmTestNode("R1_Arm")  # 新建一个节点dd
    rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy