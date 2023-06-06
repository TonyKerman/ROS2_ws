import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int64MultiArray,Float64MultiArray
import serial
import serial.tools.list_ports
import queue
import threading



class SerialNode(Node):

    def __init__(self):
        super().__init__('serial_node')
        self.mpuPublisher = self.create_publisher(Int64MultiArray, 'mpu_data', 10)
        self.servoPublisher = self.create_publisher(Float64MultiArray, 'servo_data', 10)
        self.ports = list(serial.tools.list_ports.comports())
        try:
            self.serial_port = serial.Serial(self.ports[0][0], 115200) # change this to your serial port and baud rate
        except IndexError:
            self.get_logger().info('No serial port found')
        self.mpuData_queue = queue.Queue() # create a queue to store the serial data
        self.servoData_queue = queue.Queue()
        self.read_thread = threading.Thread(target=self.read_serial) # create a thread to read the serial data
        self.get_logger().info('Serial node has been started')
        self.read_thread.start() # start the thread


    def read_serial(self):
        
        while True:
            try:
                if not self.serial_port.is_open:
                    try:
                        self.serial_port = serial.Serial(self.ports[0][0], 115200) # change this to your serial port and baud rate
                    except IndexError:
                        self.get_logger().info('No serial port found')
                byte = self.serial_port.read(1)
                # decode the byte as UTF-8
                if byte == b'\x55' and self.serial_port.read(1) == b'\x55':
                    massageType = self.serial_port.read(1)
                    l =self.serial_port.read(1).hex()
                    length = int(l,16)
                    data = b''
                    for i in range(length):
                        data+=(self.serial_port.read(1))
                    if massageType == b'\x33':
                        self.mpuData_queue.put(self.mDecode_MpuMsg(data))
                    elif massageType == b'\x11':
                        self.servoData_queue.put(self.mDecode_ServoMsg(data))
                else:
                    pass
            except serial.SerialException as e:
                print(e)
                continue

            


    def mDecode_MpuMsg(self, rawData):
        # l = [rawData[i:i+4] for i in range(0,len(rawData),4)]
        # for i in range(0,len(l),2):
        #     val.append(int(l[i]+l[i+1],16))
        val =[]
        for i in range(0,len(rawData),4):
            val.append(int.from_bytes(rawData[i:i+4],byteorder='big',signed=True))
        return val
    
    def mDecode_ServoMsg(self,rawData):
        # l = [rawData[i:i+2] for i in range(0,len(rawData),2)]
        # for i in range(0,len(l),2):
        #     val.append(int(l[i]+l[i+1],16))
        val =[]
        for i in range(0,len(rawData),2):
            val.append(int.from_bytes(rawData[i:i+2],byteorder='big',signed=False))

        n =4
        bis = [800,1155,400,700]
        def to_angle(pos,bis)->float:
            return (pos - bis)*0.24
        angles = [to_angle(val[i],bis[i]) for i in range(n)]
        return angles
    

    def publish_mpuData(self):

        while not self.mpuData_queue.empty(): # check if the queue is not empty
            data = self.mpuData_queue.get() # get the data from the queue
            msg = Int64MultiArray()
            msg.data = data
            self.mpuPublisher.publish(msg) # publish the data as a string message
            self.get_logger().info('mpuData: "%s"' % msg.data)
        else:
            pass

    
    def publish_servoData(self):

        while not self.servoData_queue.empty(): # check if the queue is not empty
            data = self.servoData_queue.get() # get the data from the queue
            msg = Float64MultiArray()
            msg.data = data
            self.servoPublisher.publish(msg) # publish the data as a string message
            self.get_logger().info('ServoData: "%s"' % msg.data)
        else:
            pass


# def publish_data(self):

    #     while not self.data_queue.empty(): # check if the queue is not empty
    #         data = self.data_queue.get() # get the data from the queue
    #         msg = String()
    #         msg.data = data
    #         self.publisher.publish(msg) # publish the data as a string message
    #         self.get_logger().info('Publishing: "%s"' % msg.data)
    #     else:
    #         pass


def main(args=None):
    rclpy.init(args=args)
    serial_node = SerialNode()
    while rclpy.ok():
        rclpy.spin_once(serial_node,timeout_sec=0) # spin once to handle callbacks
        serial_node.publish_servoData() # publish the data from the queue
        serial_node.publish_mpuData()
    serial_node.destroy_node()
    rclpy.shutdown()
    exit()


