
import sys
import rclpy
from rclpy.node import Node

from std_msgs.msg import Int64MultiArray,Float64MultiArray
from geometry_msgs.msg import TransformStamped
from tf2_ros import StaticTransformBroadcaster
from tf2_ros import TransformBroadcaster
import numpy as np
import scipy
from scipy.spatial.transform import Rotation

arm_length=[0.17,0.14,0,0]


#平移变换
def translation(qx,qy,qz):
    Dq = np.array([[1,0,0,qx],
                 [0,1,0,qy],
                 [0,0,1,qz],
                 [0,0,0,1]],dtype=float)
    return Dq


#旋转变换npa
def rotation(cls,angles):
    r = Rotation.from_euler(cls,angles,degrees=True)
    R = r.as_matrix()
    return R


#一般变换
def transform(Dm,Rm):
    if(Dm.shape !=(4,4) or Rm.shape!=(3,3)):
        raise IndexError("Wrong Matrix size!")
    temp = np.append(Rm,np.reshape(Dm[:3,3],(3,1)),axis=1)
    temp = np.append(temp,[[0.,0.,0.,1.]],axis=0)
    return temp


#DH变换
def DH_transform(alpha,a,d,theta):
    ScrewX = transform(translation(a,0,0),rotation('x',alpha))
    ScrewZ =transform(translation(0,0,d),rotation('z',theta))
    T = ScrewX @ ScrewZ
    return T



def TFtransform_from_Matrix(timestamp,A:str,B:str,m:np.ndarray):
   
    if m.shape != (4, 4):
        raise IndexError('The matrix shape is not 4x4')
    T = TransformStamped()
    T.header.stamp = timestamp
    T.header.frame_id = A
    T.child_frame_id = B
    T.transform.translation.x = m[0][3]
    T.transform.translation.y = m[1][3]
    T.transform.translation.z = m[2][3]
    w = 0.5*np.sqrt(1+np.square(m[0][0])+np.square(m[1][1])+np.square(m[2][2]))
    T.transform.rotation.w = w
    T.transform.rotation.x = (m[2][1]-m[1][2])/(4*w)
    T.transform.rotation.y = (m[0][2]-m[2][0])/(4*w)
    T.transform.rotation.z = (m[1][0]-m[0][1])/(4*w)
    #print(T.transform.rotation.x,'   ',T.transform.rotation.y,'   ',T.transform.rotation.z,'   ',T.transform.rotation.w)
    return T



class TF_Publisher(Node):
    def __init__(self):
        super().__init__('tf_publisher')
        self.tf_broadcaster = TransformBroadcaster(self)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.mpu_subscriber = self.create_subscription(Int64MultiArray,'mpu_data',self.mpu_callback,10)
        self.servo_subscriber = self.create_subscription(Float64MultiArray,'servo_data',self.servo_callback,10)
        self.tf_publisher = TransformBroadcaster(self)

        T0 =np.array([[ 0.707, -0.,    -0.707,  0.   ],
              [ 0.   ,  1.,    -0.,     0.   ],
              [ 0.707,  0.,     0.707,  0.   ],
              [ 0.    , 0.,     0.,     1.   ]],dtype=float)
        static_tf_publisher = StaticTransformBroadcaster(self)
        t = TFtransform_from_Matrix(self.get_clock().now().to_msg(),'base0','base1',T0)
        static_tf_publisher.sendTransform(t)

        self.servoAngles = [0,0,0,0]
       
                                                 
    def timer_callback(self):
        self.T1 = DH_transform(0,0.01,0,self.servoAngles[0])
        self.T2 = DH_transform(0,0.17,0,-self.servoAngles[1])
        self.T3 = DH_transform(0,0.14,0,-self.servoAngles[2]-90)
        self.T4 = DH_transform(-90,0,0.01,self.servoAngles[3])
        self.t1 = TFtransform_from_Matrix(self.get_clock().now().to_msg(),'base1','S1',self.T1)
        self.tf_publisher.sendTransform(self.t1)
        self.t2 = TFtransform_from_Matrix(self.get_clock().now().to_msg(),'S1','S2',self.T2)
        self.tf_publisher.sendTransform(self.t2)
        self.t3 = TFtransform_from_Matrix(self.get_clock().now().to_msg(),'S2','S3',self.T3)
        self.tf_publisher.sendTransform(self.t3)
        self.t4 = TFtransform_from_Matrix(self.get_clock().now().to_msg(),'S3','S4',self.T4)
        self.tf_publisher.sendTransform(self.t4)
        self.get_logger().info('Publishing Transform')

    def mpu_callback(self,msg):
        res = msg.data
        pass

    def servo_callback(self,msg):
        self.servoAngles = msg.data
        pass


pose =['waiting','aiming']
# def control():
#     state = pose[0]
#     if state == 'waiting':
#         angles = [-90,170,0,0]
#     if state == 'aiming':
#         #solve 
#         # h/cos(a0)=l1*cos(a1)+l2*sin(-a2+a1-pi/2),
#         # l1*sin(a1)=x+l2*cos(-a2+a1-pi/2),
#         # a3=a1-a2-pi/2,a0=pi/6
#         #  for a1,a2,a3
#         a1 = 0
#         a2 = 0
#         pass

def main(args=None):
    rclpy.init(args=args)
    tf_publisher = TF_Publisher()
    
    rclpy.spin(tf_publisher)
    tf_publisher.destroy_node()
    rclpy.shutdown()


