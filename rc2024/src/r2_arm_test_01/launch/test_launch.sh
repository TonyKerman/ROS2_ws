export PKG="r2_arm_test_01"
export LAUNCH="test_.launch.py"
export WORKSPACE=/root/2ROS2workspace/rc2024
cd $WORKSPACE
colcon build --packages-select $PKG
source install/setup.bash
ros2 launch $PKG $LAUNCH
