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