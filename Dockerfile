FROM osrf/ros:humble-desktop
RUN apt update &&apt upgrade -y && apt-get install -y openssh-server gdb gdbserver python3-pip
    #安装rosdepc<https://zhuanlan.zhihu.com/p/398754989>
RUN sudo pip install rosdepc 

RUN sudo rosdepc init && rosdepc update

USER root

RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc

# 创建项目源码目录，这个目录将成为 Container 里面构建和执行的工作区
RUN mkdir -p /root/ros2_ws
WORKDIR /root/ros2_ws
ENV LC_ALL C.UTF-8
