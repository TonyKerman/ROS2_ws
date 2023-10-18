export PKG1="motor"
export PKG2="rc2024_interfaces"
export LAUNCH="display.launch.py"
export WORKSPACE=/root/2ROS2workspace/rc2024
cd $WORKSPACE
colcon build --packages-select $PKG1 $PKG2
source install/setup.bash
ros2 launch $PKG1 $LAUNCH
