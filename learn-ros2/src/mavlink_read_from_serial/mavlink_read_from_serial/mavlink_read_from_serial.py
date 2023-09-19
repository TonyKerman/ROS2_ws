import py_mavlink_lib as mav
import rclpy
from rclpy import Node
from serial import Serial

class Mavlink_serial(Node):
    def __init__(self,name):
        super().__init__(name)
        serial_name = 'ttyACM0'
        self.serial = Serial(serial_name,115200,timeout=1000)
        self.rate = self.create_rate(100)
        self.M = mav.MAVLink()
        while True:
            self.read()
            #self.rate.sleep()
    
    def read(self):
        b = self.serial.read()
        msg = self.M.parse_buffer(b)
        if msg != None:
            self.get_logger().info(str(msg))

def main(args = None):
    rclpy.init(args = args)
    node = Mavlink_serial('Mavlink serial node')
    rclpy.spin(node)
    rclpy.shutdown() # 关闭rclpy

