import rclpy
from rclpy.node import Node
from std_msgs.msg import String,Byte
from std_msgs.msg import Int64MultiArray, Float64MultiArray,Int16MultiArray
import serial
import serial.tools.list_ports
import queue
import threading
from time import sleep
from .ModelData import servos_bis
from struct import pack


class SerialNode(Node):

    def __init__(self):
        super().__init__('serial_node')
        self.mpuPublisher = self.create_publisher(
            Int64MultiArray, 'mpu_data', 10)
        self.servoPublisher = self.create_publisher(
            Float64MultiArray, 'servo_data', 10)
        self.serialMsg_subscriber = self.create_subscription(
            Int16MultiArray, 'serial_Msg', self.serial_callback, 3)

        self.ports = list(serial.tools.list_ports.comports())
        try:
            # change this to your serial port and baud rate
            self.serial_port = serial.Serial(self.ports[0][0], 115200,timeout=0.01)
        except IndexError:
            self.get_logger().info('No serial port found')
        # create queues to store data
        self.mpuData_queue = queue.Queue()
        self.servoData_queue = queue.Queue()
        self.serMsg_queue = queue.Queue()
        # create a thread to read and write the serial
        self.read_thread = threading.Thread(target=self.serial_thread)
        self.read_thread.setDaemon(True)
        self.read_thread.start()
        self.get_logger().info('Serial node has been started')

    def serial_thread(self):
        while True:
            try:

                if not self.serial_port.is_open:
                    try:
                        self.ports = list(serial.tools.list_ports.comports())
                        # change this to your serial port and baud rate
                        serial_port = serial.Serial(self.ports[0][0], 115200,timeout=0.05)
                    except IndexError:
                        self.get_logger().info('No serial port found')
                        sleep(0.3)
                        continue
                self.read_serial()
                
                self.write_serial()
            except Exception as e:
                print(e)
                continue

    # 读串口数据帧，并根据帧类型选择解码
    # 注意，发送给解码函数时已经去掉校验位
    def read_serial(self):
        byte = self.serial_port.read(1)
        # decode the byte as UTF-8
        if byte == b'\x55' and self.serial_port.read(1) == b'\x55':
            massageType = self.serial_port.read(1)
            l = self.serial_port.read(1).hex()
            length = int(l, 16)
            data = b''
            for i in range(length):
                data += (self.serial_port.read(1))
            if massageType == b'\x33':
                self.mpuData_queue.put(self.mDecode_MpuMsg(data))
            elif massageType == b'\x11':
                self.servoData_queue.put(self.mDecode_ServoMsg(data))
            return 0
        else:
            self.get_logger().info("%s" % byte.decode(encoding='utf-8'))
            return -1

    def write_serial(self):
        # self.serial_port.write(b'\x55\x55\x01\x02\x03\x04')
        # self.get_logger().info("send a cmd")
        # sleep(0.5)
        if not self.serMsg_queue.empty():
            self.serial_port.write(self.serMsg_queue.get())
           
            pass
    def sendmsg(self,data):
        msg=b'\x55\x55'
        msgtype=b'\x01'
        buf=b''
        for b in data:
            if b<32767:
                buf+=pack('>H',b)
        #print(buf)
        msglen=pack(">B",len(buf))
        msg+=msgtype
        msg+=msglen
        msg+=buf
        #print(msg)
        return msg

    def mDecode_MpuMsg(self, rawData):
        val = []
        datalen = 4
        for i in range(0, len(rawData), datalen):
            val.append(int.from_bytes(
                rawData[i:i+datalen], byteorder='big', signed=True))
        return val

    def mDecode_ServoMsg(self, rawData):
        # l = [rawData[i:i+2] for i in range(0,len(rawData),2)]
        # for i in range(0,len(l),2):
        #     val.append(int(l[i]+l[i+1],16))
        val = []
        datalen = 2
        for i in range(0, len(rawData), datalen):
            val.append(int.from_bytes(
                rawData[i:i+datalen], byteorder='big', signed=False))
        n = 4

        def to_angle(pos, bis) -> float:
            return (pos - bis)*0.24
        angles = [to_angle(val[i], servos_bis[i]) for i in range(n)]
        #print(angles[0], angles[1], angles[2])
        return angles

    def publish_mpuData(self):
        while not self.mpuData_queue.empty():  # check if the queue is not empty
            data = self.mpuData_queue.get()  # get the data from the queue
            msg = Int64MultiArray()
            msg.data = data
            # publish the data as a string message
            self.mpuPublisher.publish(msg)
            self.get_logger().info('mpuData: "%s"' % msg.data)
        else:
            pass

    def publish_servoData(self):
        while not self.servoData_queue.empty():  # check if the queue is not empty
            data = self.servoData_queue.get()  # get the data from the queue
            msg = Float64MultiArray()
            msg.data = data
            # publish the data as a string message
            self.servoPublisher.publish(msg)
            self.get_logger().info('ServoData: "%s"' % msg.data)
        else:
            pass

    def serial_callback(self, msg):
        #self.get_logger().info(msg.data)
        self.serMsg_queue.put(self.sendmsg(msg.data))
        
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
        # spin once to handle callbacks
        rclpy.spin_once(serial_node, timeout_sec=0)
        serial_node.publish_servoData()  # publish the data from the queue
        serial_node.publish_mpuData()
    serial_node.read_thread.join()
    serial_node.destroy_node()
    rclpy.shutdown()
    exit()
