# Node in ROS2 


## create a workspace
A trivial workspace might look like:

    workspace_folder/
    src/
      package_1/
          CMakeLists.txt
          package.xml

      package_2/
          setup.py
          package.xml
          resource/package_2
      ...
      package_n/
          CMakeLists.txt
          package.xml
### create a package(cmake):

    ros2 pkg create --build-type ament_cmake <package_name>

* <http://d2lros2foxy.fishros.com/#/humble/chapt2/advanced/2.%E4%BD%BF%E7%94%A8%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1%E6%96%B9%E5%BC%8F%E7%BC%96%E5%86%99ROS2%E8%8A%82%E7%82%B9>

* <https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Cpp-Publisher-And-Subscriber.html>

## write and build/run in c++
take first_node for example
* write first_node/src/code.cpp

* edit CMakeLists.txt

  ">>" is what we need to add in the file

        cmake_minimum_required(VERSION 3.8)
        project(first_node)

        if(NOT CMAKE_CXX_STANDARD)
        set(CMAKE_CXX_STANDARD 14)
        endif()

        if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
        add_compile_options(-Wall -Wextra -Wpedantic)
        endif()

        # find dependencies
        find_package(ament_cmake REQUIRED)
        >>find_package(rclcpp REQUIRED)
        # uncomment the following section in order to fill in
        # further dependencies manually.
        # find_package(<dependency> REQUIRED)

        >>add_executable(node_01 src/code.cpp)
        >>ament_target_dependencies(node_01 rclcpp)
        >>install(TARGETS
        >>node_01
        >>DESTINATION lib/${PROJECT_NAME}

        )

        ament_package()
* in terminal:
 >>
    colcon build [colcon build --packages-select example_cpp]
    source install/setup.bash #necessary
    ros2 run first_node node01 # "node01" is the exceutable which is set in CMakeLists.txt

## write and run in python

1. create a package

        cd ros2_ws/src
        ros2 pkg create first_node_py  --build-type ament_python --dependencies rclpy 

2. example steps of creating a node:
     1. 导入库文件
     2. 初始化客户端库
     3. 新建节点
     4. spin循环节点
     5. 关闭客户端库 
 
3. edit first_node_py/first_node_py/code.py
4. edit setup.py

         entry_points={
            'console_scripts': [的
        >>        "node02 = first_node_py.code:main"
            ],
        }, 
5. build and run

        colcon build
        source install/setup.bash
        ros2 run first_node_py node02

## write a python node with OOP()
    ../src/learning_node/first_node_py/first_node_py/code2.py
## write a publisher and subscriber node
see in package "pubsub_cpp" and "pubsub_py"
## write a service node (cpp)
<http://d2lros2foxy.fishros.com/#/humble/chapt3/get_started/5.%E6%9C%8D%E5%8A%A1%E4%B9%8BRCLCPP%E5%AE%9E%E7%8E%B0>

see package "srvcli_cpp"
1. create package

        ros2 pkg create --build-type ament_cmake cpp_srvcli --dependencies rclcpp 

2. write service_server_01.cpp && service_client_01.cpp

2.1. 导入接口example_interfaces
     
查看接口定义ros2 interface show example_interfaces/srv/AddTwoInts


ament_cmake类型功能包导入消息接口分为三步：

在CMakeLists.txt中导入，具体是先find_packages再ament_target_dependencies。

在packages.xml中导入，具体是添加depend标签并将消息接口写入。

在代码中导入，C++中是#include"消息功能包/xxx/xxx.hpp"。

CMakelists.txt
    
    # 这里我们一次性把服务端和客户端对example_interfaces的依赖都加上
    find_package(example_interfaces REQUIRED)

    add_executable(service_client_01 src/service_client_01.cpp)
    ament_target_dependencies(service_client_01 rclcpp example_interfaces)

    add_executable(service_server_01 src/service_server_01.cpp)
    ament_target_dependencies(service_server_01 rclcpp example_interfaces)
packages.xml
    
    <depend>example_interfaces</depend>

<http://d2lros2foxy.fishros.com/#/humble/chapt2/advanced/3.Colcon%E4%BD%BF%E7%94%A8%E8%BF%9B%E9%98%B6>
