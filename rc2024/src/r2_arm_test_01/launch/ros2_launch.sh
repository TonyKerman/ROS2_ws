export PKG="r2_arm_test_01"
export LAUNCH="display_rviz2.launch.py"

cd ../..
colcon build --packages-select $PKG
source install/setup.bash
ros2 launch $PKG $LAUNCH
