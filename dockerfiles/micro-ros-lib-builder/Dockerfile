FROM ros:humble
RUN rm /etc/apt/sources.list
ADD sources.list /etc/apt/
RUN mkdir -p uros_ws
WORKDIR uros_ws
RUN apt update \
    &&  apt install -y wget dos2unix \
    &&  rm -rf log/ build/ src/* \
    &&  rm -rf /var/lib/apt/lists/* \
    && wget --no-check-certificate https://launchpad.net/gcc-arm-embedded/5.0/5-2016-q2-update/+download/gcc-arm-none-eabi-5_4-2016q2-20160622-linux.tar.bz2 \
    && tar -xvf gcc-arm-none-eabi-5_4-2016q2-20160622-linux.tar.bz2 \
    && rm -rf gcc-arm-none-eabi-5_4-2016q2-20160622-linux.tar.bz2 gcc-arm-none-eabi-5_4-2016q2/share/doc \
    && wget --no-check-certificate https://www.pjrc.com/teensy/td_158/teensy-compile-linux64.tar.bz2 \
    && mkdir teensy-compile \
    && tar -xvf teensy-compile-linux64.tar.bz2 -C teensy-compile \
    && rm -rf teensy-compile-linux64.tar.bz2 \
    && wget --no-check-certificate https://launchpad.net/gcc-arm-embedded/4.8/4.8-2014-q1-update/+download/gcc-arm-none-eabi-4_8-2014q1-20140314-linux.tar.bz2 \
    && tar -xvf gcc-arm-none-eabi-4_8-2014q1-20140314-linux.tar.bz2 \
    && rm -rf gcc-arm-none-eabi-4_8-2014q1-20140314-linux.tar.bz2 gcc-arm-none-eabi-4_8-2014q1/share/doc \
    && wget --no-check-certificate https://developer.arm.com/-/media/Files/downloads/gnu-rm/7-2017q4/gcc-arm-none-eabi-7-2017-q4-major-linux.tar.bz2 \
    && tar -xvf gcc-arm-none-eabi-7-2017-q4-major-linux.tar.bz2 \
    && rm -rf gcc-arm-none-eabi-7-2017-q4-major-linux.tar.bz2 gcc-arm-none-eabi-7-2017-q4-major/share/doc \
    && wget --no-check-certificate https://developer.arm.com/-/media/Files/downloads/gnu-rm/9-2020q2/gcc-arm-none-eabi-9-2020-q2-update-x86_64-linux.tar.bz2 \
    && tar -xvf gcc-arm-none-eabi-9-2020-q2-update-x86_64-linux.tar.bz2 \
    && rm -rf gcc-arm-none-eabi-9-2020-q2-update-x86_64-linux.tar.bz2 gcc-arm-none-eabi-9-2020-q2-update/share/doc \
    && wget --no-check-certificate https://github.com/espressif/crosstool-NG/releases/download/esp-2021r2/xtensa-esp32-elf-gcc8_4_0-esp-2021r2-linux-amd64.tar.gz \
    && tar -xvf xtensa-esp32-elf-gcc8_4_0-esp-2021r2-linux-amd64.tar.gz \
    && rm -rf xtensa-esp32-elf-gcc8_4_0-esp-2021r2-linux-amd64.tar.gz

# Install micro-ROS
RUN git clone -b $ROS_DISTRO https://github.com/micro-ROS/micro-ros-build.git src/micro-ros-build \
    &&  . /opt/ros/$ROS_DISTRO/setup.sh \
    &&  apt update \
    &&  apt install -y rsync python3-pip python3-nose clang-format pyflakes3 python3-mypy python3-pytest-mock gperf ros-$ROS_DISTRO-osrf-testing-tools-cpp python3-lttng ros-$ROS_DISTRO-mimick-vendor python3-babeltrace python3-pip \
    &&  pip install rosdepc \ 
    &&  rosdepc init &&rosdepc update --rosdistro $ROS_DISTRO \
    &&  rosdepc install --from-paths src --ignore-src -y \
    &&  colcon build \
    &&  . install/local_setup.sh \
    &&  rm -rf log/ build/ src/* \
    &&  rm -rf /var/lib/apt/lists/*

COPY ./entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]