#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
# 1.导入消息类型JointState
from sensor_msgs.msg import JointState
from my_interfaces.msg import Myinput, Myoutput
import threading,time,serial,struct
import numpy as np

servos_bis = [775, 1155, 400, 700]

class ControlArmNode(Node):
    def __init__(self,name):
        super().__init__(name)
        self.joint_states_publisher_ = self.create_publisher(JointState,"joint_states", 10)

        self.output_pub = self.create_publisher(Myoutput,"output_msg",10)
        

        self.joint_states = JointState()
        self.inputMsg = Myinput()
        self.outputMsg = Myoutput()
        self.lock = threading.Lock()
        
        self.pub_rate = self.create_rate(10)
        self.thread_pub = threading.Thread(target=self._thread_pub)
        self.thread_pub.setDaemon(True)
        self.thread_pub.start()

        is_open =False
        while not is_open:
            try:
                
                serial_name =  'ttyACM0'
                self.serial_port = serial.Serial(serial_name, 115200,timeout=0.5)
                self.get_logger().info('serial success!')
                is_open =True
            except:
                self.get_logger().fatal(f'No device found in {serial_name}\n\n\n')
                time.sleep(1)
                break
        
        if is_open:
            while True:
                self._thread_serial()

    
    def _thread_serial(self):
        b_end = b'\xef'
        raw = self.serial_port.read_until(b_end,41)
        raw =struct.unpack('hhhhddddc',raw)
        with self.lock:
            self.inputMsg.servoPos=raw[0:4]
            self.inputMsg.quants=raw[4:8]
       

        
    def _thread_pub(self):
        last_update_time = time.time()

        self.joint_states.name = ['joint1','joint2','joint3','joint4','joint5','joint6']
        self.joint_states.position = [0.0,0.0,0.0,0.0,0.0,0.0]
        self.joint_states.velocity = []
        #self.joint_states.name = ['joint1']
        #self.joint_states.position = [10.0]
        #self.joint_states.velocity = [0.0]
        self.joint_states.effort = []
        self.joint_states.header.frame_id = ""
        while rclpy.ok():
            # delta_time =  time.time()-last_update_time
            # last_update_time = time.time()
            self.joint_states.header.stamp = self.get_clock().now().to_msg()
            with self.lock:
                
                self.joint_states.position[0]+=1 
                #self.joint_states.velocity = [0.0]
                #self.joint_states.effort = []
                #self.joint_states.position=[(pos-servos_bis)*0.24*np.pi/180 for pos in self.inputMsg.servopos]
            self.joint_states_publisher_.publish(self.joint_states)
            self.get_logger().info('send')
            self.pub_rate.sleep()
            

        

# class RotateWheelNode(Node):
#     def __init__(self,name):
#         super().__init__(name)
#         self.get_logger().info(f"node {name} init..")
#         # 创建并初始化发布者成员属性pub_joint_states_
#         self.joint_states_publisher_ = self.create_publisher(JointState,"joint_states", 10) 
#         # 初始化数据
#         self._init_joint_states()
#         self.pub_rate = self.create_rate(30)
#         self.thread_ = threading.Thread(target=self._thread_pub)
#         self.thread_.start()

    
#     def _init_joint_states(self):
#         # 初始左右轮子的速度
#         self.joint_speeds = [0.0,0.0]
#         self.joint_states = JointState()
#         self.joint_states.header.stamp = self.get_clock().now().to_msg()
#         self.joint_states.header.frame_id = ""
#         # 关节名称
#         self.joint_states.name = ['left_wheel_joint','right_wheel_joint']
#         # 关节的位置
#         self.joint_states.position = [0.0,0.0]
#         # 关节速度
#         self.joint_states.velocity = self.joint_speeds
#         # 力 
#         self.joint_states.effort = []

#     def update_speed(self,speeds):
#         self.joint_speeds = speeds

#     def _thread_pub(self):
#         last_update_time = time.time()
#         while rclpy.ok():
#             delta_time =  time.time()-last_update_time
#             last_update_time = time.time()
#             # 更新位置
#             self.joint_states.position[0]  += delta_time*self.joint_states.velocity[0]
#             self.joint_states.position[1]  += delta_time*self.joint_states.velocity[1]
#             # 更新速度
#             self.joint_states.velocity = self.joint_speeds
#             # 更新 header
#             self.joint_states.header.stamp = self.get_clock().now().to_msg()
#             # 发布关节数据
#             self.joint_states_publisher_.publish(self.joint_states)
#             self.pub_rate.sleep()

def main(args=None):
    rclpy.init(args=args) # 初始化rclpy
    node = ControlArmNode("arm_control")  # 新建一个节点
    
    rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy
