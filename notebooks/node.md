# Node in ROS2 


## create a workspace 创建工作区
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
### create a package(cmake):创建包

    ros2 pkg create --build-type ament_cmake <package_name>

* <http://d2lros2foxy.fishros.com/#/humble/chapt2/advanced/2.%E4%BD%BF%E7%94%A8%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1%E6%96%B9%E5%BC%8F%E7%BC%96%E5%86%99ROS2%E8%8A%82%E7%82%B9>

* <https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Cpp-Publisher-And-Subscriber.html>

## write and build/run in c++ 写代码并构建运行 C++
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

## write and run in python 写代码并构建运行 C++

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
4. edit setup.py 添加入口点

         entry_points={
            'console_scripts': [
        >>        "node02 = first_node_py.code:main"
            ],
        }, 
5. build and run 构建执行

        colcon build
        source install/setup.bash #执行一次就行
        ros2 run first_node_py node02
