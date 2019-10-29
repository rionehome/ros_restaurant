cmake_minimum_required(VERSION 3.5)
project(control_system)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()


# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(rione_msgs REQUIRED)

add_executable(control_system
  control_system.cpp
)
ament_target_dependencies(control_system
  "rclcpp"
  "rione_msgs"
)

install(TARGETS
  control_system
  DESTINATION lib/${PROJECT_NAME}
)

add_executable(test_rione_msgs
  test/test_rione_msgs.cpp
)

ament_target_dependencies(test_rione_msgs
  "rclcpp"
  "rione_msgs"
)

install(TARGETS
  test_rione_msgs
  DESTINATION lib/${PROJECT_NAME}
)
ament_package()