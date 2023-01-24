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
find_package(rclcpp REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

add_executable(node01 src/code.cpp)
ament_target_dependencies(node01 rclcpp)
install(TARGETS
  node01
  DESTINATION lib/${PROJECT_NAME}

)

ament_package()
