FROM tony/ros2:humble-basic

SHELL ["/bin/bash", "-c"]

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y software-properties-common 

# Install dependencies: See https://github.com/IntelRealSense/realsense-ros/tree/ros2-development
# Librealsense: See https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md#installing-the-packages
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE \
 && add-apt-repository "deb https://librealsense.intel.com/Debian/apt-repo $(lsb_release -cs) main" -u \
 && apt-get upgrade -y \
 && apt-get install -y \
    librealsense2-dbg \
    librealsense2-dev \
    librealsense2-utils 
RUN apt-get install -y librealsense2-dkms || true
RUN rm -rf /var/lib/dpkg/info/*librealsense2-dkms*\
&& apt-get -f install
ARG DEBIAN_FRONTEND=dialog
