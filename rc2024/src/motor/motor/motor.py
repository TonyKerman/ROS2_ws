from sensor_msgs.msg import JointState
from builtin_interfaces.msg import Time
from typing import Iterable
import numpy as np


class Pid_parms():
    def __init__(self,vals:Iterable=(1,0,0)):
        if isinstance(vals,np.ndarray):
            vals = vals.tolist
        if len(vals) != 3 :
            raise ValueError('PID parameters must have 3 elements(kp,ki,kd)!')
        self.kp,self.ki,self.kd = vals
        
    def reset(self,vals:Iterable):
        if isinstance(vals,np.ndarray):
            vals = vals.tolist
        if len(vals) != 3 :
            raise ValueError('PID parameters must have 3 elements(kp,ki,kd)!') 
        self.kp,self.ki,self.kd = vals
    
class Motor():
    def __init__(self,motor_name:str,pid_parms:Iterable=(1,0,0)):
        self.state = JointState()
        self.pid_parms = Pid_parms(pid_parms)
        self.state.name =motor_name
        

    def update(self,time:Time,position:float=0,velocity:float=0,effort:float=0):
        self.state.header.stamp = time
        self.state.position = position
        self.state.velocity =velocity
        self.state.effort = effort
        

        
