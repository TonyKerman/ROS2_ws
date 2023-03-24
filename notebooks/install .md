# ROS2 Study Note

## Install ROS2 with docker

1. install docker via apt
    <https://www.runoob.com/docker/ubuntu-docker-install.html>
then
    sudo groupadd docker
    sudo gpasswd -a ${USER} docker
    newgrp docker
    sudo service docker restart
2. set a workspace

3. pull  ros2 image

4. install docker-compose
    sudo apt install docker-compose
5. write a Dockerfile and docker-compose.yml

### Dockerfile

```
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

```

### docker-compose.yml

```
version: "3.9"

x-defaults: &default
  restart: unless-stopped
#  使用当前目录的 Dockerfile 来构建 docker 镜像
  build: .
  # build from specific image
  image : tony/ros2:demo
  volumes:
    - /home/tony/ROS2_ws:/root/ros2_ws
    # function along with"- DISPLAY=unix$DISPLAY" to enable Qt 
    - /tmp/.X11-unix:/tmp/.X11-unix
  networks:
    - default
    
services:
  my-project:
    <<: *default
    container_name: ros2_project
    hostname: "ros2_project"
    user: root
    working_dir: /root/ros2_ws

#   同时通过 tailf 命令保持 container 不要退出的状态
    command:
      bash -c "tail -f /dev/null"
    environment:
      - DISPLAY=unix$DISPLAY
```

5  build

    docker build -t tony/ros2:demo .
    docker-compose up -d
    xhost +
6 use vscode open it
  in vscode install ROS open container in left bar "remote resource..." complete settings 

* [https://www.allaban.me/posts/2020/08/ros2-setup-ide-docker/]
* [https://imhuwq.com/2018/12/02/Clion%20%E4%BD%BF%E7%94%A8%20Docker%20%E4%BD%9C%E4%B8%BA%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83/]
* [https://zhuanlan.zhihu.com/p/520752548]

