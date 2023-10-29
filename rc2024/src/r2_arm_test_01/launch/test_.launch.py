import os
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    #注意要改
    package_name = 'r2_arm_test_01'
    urdf_name = "r2Arm.urdf"

    ld = LaunchDescription()
    pkg_share = FindPackageShare(package=package_name).find(package_name) 
    urdf_model_path = os.path.join(pkg_share, f'urdf/{urdf_name}')
    rviz_config_file_path = os.path.join(pkg_share, f'urdf/display_rviz2.rviz')  # 指定要加载的.rviz配置文件的路径
    #这仨不用改

    arm_node = Node(
        package=package_name,
        executable='r2_arm_test_node',
        name='arm_node'
        )
    client_node = Node(
        package=package_name,
        executable='client_node',
        name='client_node'
        )
    #robot_state_publisher_node负责发布机器人模型信息robot_description，并将joint_states数据转换tf信息发布


    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        arguments=[urdf_model_path]
        )
    
    #rviz2_node负责显示机器人的信息
    
    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        # 加载.rviz配置文件
       arguments=['-d',rviz_config_file_path]

        )
    ld.add_action(arm_node)
    ld.add_action(client_node)
    ld.add_action(robot_state_publisher_node)
    ld.add_action(rviz2_node)

    return ld
