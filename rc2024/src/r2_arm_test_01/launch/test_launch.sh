export PKG1="r2_arm_test_01"
export PKG2="rc2024_interfaces"
export LAUNCH="test_.launch.py"
export WORKSPACE=/root/2ROS2workspace/rc2024
cd $WORKSPACE
colcon build --packages-select $PKG1 $PKG2
source install/setup.bash
ros2 launch $PKG1 $LAUNCH
