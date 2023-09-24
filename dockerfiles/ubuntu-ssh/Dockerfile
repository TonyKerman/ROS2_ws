FROM ubuntu:22.04

RUN apt-get update && apt-get install -y openssh-server gdb gdbserver sudo

# 创建 docker 用户并且赋予不用密码进行 sudo 的权限
RUN echo "#!/bin/bash\nadduser docker << EOF\npassword\npassword\ndocker\n\n\n\nY\nEOF" >> create_docker.sh && \
    chmod 755 create_docker.sh && \
    ./create_docker.sh && \
    gpasswd -a docker sudo && \
    rm create_docker.sh && \
    touch /etc/sudoers\
    chmod 644 /etc/sudoers && \
    echo "docker ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
# RUN echo "#!/bin/bash\nadduser docker << EOF\npassword\npassword\ndocker\n\n\n\nY\nEOF" >> create_docker.sh && \
#     chmod 755 create_docker.sh && \
#     ./create_docker.sh && \
#     gpasswd -a docker sudo && \
#     rm create_docker.sh
# 执行其它命令以创建必要的环境，不再赘述
#RUN ...

USER docker
# 创建项目源码目录，这个目录将成为 Container 里面构建和执行的工作区
RUN mkdir -p /home/docker/
#WORKDIR /home/docker/my-project
ENV LC_ALL C.UTF-8