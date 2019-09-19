# CMake generated Testfile for 
# Source directory: /home/hirose/ros2_ws/ros_restaurant/control_system
# Build directory: /home/hirose/ros2_ws/ros_restaurant/build/control_system
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(lint_cmake "/usr/bin/python3" "-u" "/opt/ros/crystal/share/ament_cmake_test/cmake/run_test.py" "/home/hirose/ros2_ws/ros_restaurant/build/control_system/test_results/control_system/lint_cmake.xunit.xml" "--package-name" "control_system" "--output-file" "/home/hirose/ros2_ws/ros_restaurant/build/control_system/ament_lint_cmake/lint_cmake.txt" "--command" "/opt/ros/crystal/bin/ament_lint_cmake" "--xunit-file" "/home/hirose/ros2_ws/ros_restaurant/build/control_system/test_results/control_system/lint_cmake.xunit.xml")
set_tests_properties(lint_cmake PROPERTIES  LABELS "lint_cmake;linter" TIMEOUT "60" WORKING_DIRECTORY "/home/hirose/ros2_ws/ros_restaurant/control_system")
add_test(xmllint "/usr/bin/python3" "-u" "/opt/ros/crystal/share/ament_cmake_test/cmake/run_test.py" "/home/hirose/ros2_ws/ros_restaurant/build/control_system/test_results/control_system/xmllint.xunit.xml" "--package-name" "control_system" "--output-file" "/home/hirose/ros2_ws/ros_restaurant/build/control_system/ament_xmllint/xmllint.txt" "--command" "/opt/ros/crystal/bin/ament_xmllint" "--xunit-file" "/home/hirose/ros2_ws/ros_restaurant/build/control_system/test_results/control_system/xmllint.xunit.xml")
set_tests_properties(xmllint PROPERTIES  LABELS "xmllint;linter" TIMEOUT "60" WORKING_DIRECTORY "/home/hirose/ros2_ws/ros_restaurant/control_system")
