FROM ubuntu:22.04
RUN rm /etc/apt/sources.list
ADD sources.list /etc/apt/
RUN apt clean && apt update &&apt upgrade -y && apt-get install -y \
python3-pip openssh-server gdb gdbserver xterm

# 创建 docker 用户并且赋予不用密码进行 sudo 的权限
RUN echo "#!/bin/bash\nadduser docker << EOF\npassword\npassword\ndocker\n\n\n\nY\nEOF" >> create_docker.sh && \
    chmod 755 create_docker.sh && \
    ./create_docker.sh && \
    gpasswd -a docker sudo && \
    rm create_docker.sh && \
    touch /etc/sudoers\
    mkdir /home/docker \ 
    chmod 644 /etc/sudoers && \
    echo "docker ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers


USER docker

#RUN echo "source /opt/ros/humble/setup.bash" >> /home/docker/.bashrc

ENV LC_ALL C.UTF-8
