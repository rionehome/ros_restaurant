cmake_minimum_required(VERSION 3.10)
project(image_system)

# Default to C++14
set(CMAKE_CXX_STANDARD 14)


# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_ros REQUIRED)
find_package(rclcpp REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(pcl_conversions REQUIRED)
find_package(OpenPose REQUIRED)
find_package(PCL 1.9 REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rione_msgs REQUIRED)
find_package(gflags REQUIRED)
find_package(OpenCV REQUIRED)

link_directories(/usr/local/lib)

add_library(image_system src/image_system.cpp)
ament_target_dependencies(image_system
    rclcpp
    rione_msgs
    sensor_msgs
    geometry_msgs
    OpenCV
    cv_bridge
    gflags
    pcl_conversions
    PCL
)
target_link_libraries(image_system
    openpose
)
target_include_directories(image_system PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)


install(
  DIRECTORY include/
  DESTINATION include
)


install(
  TARGETS image_system
  EXPORT export_${PROJECT_NAME}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

add_executable(image_system_node src/image_system_node.cpp)
ament_target_dependencies(image_system_node)

target_include_directories(image_system_node PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
target_link_libraries(image_system_node image_system boost_system)


install(TARGETS image_system_node
  EXPORT export_${PROJECT_NAME}
  DESTINATION lib/${PROJECT_NAME}
)

file(GLOB RESOURCE_FILES ${CMAKE_CURRENT_SOURCE_DIR}/resources/*.wav)
file(COPY ${RESOURCE_FILES} DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()


ament_package()
