FROM osrf/ros:humble-desktop-full
RUN rm /etc/apt/sources.list
ADD sources.list /etc/apt/
RUN apt clean && apt update &&apt upgrade -y && apt-get install -y \
python3-pip openssh-server gdb gdbserver xterm


    #安装rosdepc<https://zhuanlan.zhihu.com/p/398754989>
#apt install ros-humble-cartographer ros-humble-gazebo-ros xterm vi
#
#
RUN pip install rosdepc 
# pymavlink
RUN rosdepc init && rosdepc update

USER root

RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc

ENV LC_ALL C.UTF-8
