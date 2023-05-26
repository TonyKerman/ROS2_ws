import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import serial.tools.list_ports
import queue
import threading



class SerialNode(Node):
    def __init__(self):
        super().__init__('serial_node')
        self.publisher = self.create_publisher(String, 'serial_data', 10)
        ports = list(serial.tools.list_ports.comports())
        self.serial_port = serial.Serial(ports[0][0], 115200) # change this to your serial port and baud rate
        self.data_queue = queue.Queue() # create a queue to store the serial data
        self.read_thread = threading.Thread(target=self.read_serial) # create a thread to read the serial data
        self.read_thread.start() # start the thread

    def read_serial(self):
        while True:
            byte = self.serial_port.read(1)
            # decode the byte as UTF-8
            if byte == b'\x55' and self.serial_port.read(1) == b'\x55':
                massageType = self.serial_port.read(1).hex()
                l =self.serial_port.read(1).hex()
                length = int(l,16)
                #print('length is ',length)
                data = ''
                for i in range(length):
                    data+=(self.serial_port.read(1).hex())
                #data = mdecode(data)
                #print('put the data into the queue')
                self.data_queue.put(massageType+l+data) # put the data into the queue

            else:
                pass
                
    def publish_data(self):

        while not self.data_queue.empty(): # check if the queue is not empty
            data = self.data_queue.get() # get the data from the queue
            msg = String()
            msg.data = data
            self.publisher.publish(msg) # publish the data as a string message
            self.get_logger().info('Publishing: "%s"' % msg.data)
        else:
            pass



def main(args=None):
    rclpy.init(args=args)
    serial_node = SerialNode()
    while rclpy.ok():
        rclpy.spin_once(serial_node,timeout_sec=0.1) # spin once to handle callbacks
        serial_node.publish_data() # publish the data from the queue
    
    serial_node.destroy_node()
    rclpy.shutdown()


