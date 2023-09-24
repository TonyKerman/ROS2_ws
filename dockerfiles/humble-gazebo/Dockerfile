FROM osrf/ros:humble-desktop-full
RUN rm /etc/apt/sources.list
ADD sources.list /etc/apt/
RUN apt clean && apt update &&apt upgrade -y && apt-get install -y \
python3-pip openssh-server gdb gdbserver lsb-release wget gnupg xterm 

    #安装rosdepc<https://zhuanlan.zhihu.com/p/398754989>
#apt install ros-humble-cartographer ros-humble-gazebo-ros xterm vi
# install gazebo fortress
RUN  wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null \
apt-get update \
apt-get install ignition-fortress 

RUN pip install rosdepc pymavlink
# pymavlink
RUN rosdepc init && rosdepc update

# # 创建 docker 用户并且赋予不用密码进行 sudo 的权限
# RUN echo "#!/bin/bash\nadduser docker << EOF\npassword\npassword\ndocker\n\n\n\nY\nEOF" >> create_docker.sh && \
#     chmod 755 create_docker.sh && \
#     ./create_docker.sh && \
#     gpasswd -a docker sudo && \
#     rm create_docker.sh && \
#     touch /etc/sudoers\
#     chmod 644 /etc/sudoers && \
#     echo "docker ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER root

RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc

ENV LC_ALL C.UTF-8
