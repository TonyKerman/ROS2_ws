FROM osrf/ros:humble-desktop
RUN rm /etc/apt/sources.list
ADD sources.list /etc/apt/
RUN apt clean && apt update &&apt upgrade -y && apt-get install -y python3-pip openssh-server gdb gdbserver
    #安装rosdepc<https://zhuanlan.zhihu.com/p/398754989>
RUN sudo pip install rosdepc 

RUN sudo rosdepc init && rosdepc update

USER root

RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc

# 创建项目源码目录，这个目录将成为 Container 里面构建和执行的工作区
RUN mkdir -p /root/2ROS2workspace
WORKDIR /root/2ROS2workspace
ENV LC_ALL C.UTF-8
