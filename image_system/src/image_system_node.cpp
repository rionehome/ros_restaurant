#include "../include/image_system/image_system.hpp"

int main(int argc, char *argv[]) {
    rclcpp::init(argc, argv);

    auto node = make_shared<ImageSystem>();
    RCLCPP_INFO(node->get_logger(), "START IMAGE SYSTEM");

    rclcpp::spin(node);
    rclcpp::shutdown();

    return 0;
}
