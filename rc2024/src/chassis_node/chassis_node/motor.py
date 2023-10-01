from sensor_msgs.msg import JointState


class Motor():
    def __init__(self) -> None:
        self.state = JointState()