#include <iostream>
#include <rclcpp/rclcpp.hpp>
#include "rione_msgs/msg/command.hpp"

class TestRioneMsgs : public rclcpp::Node
{
private:
  rclcpp::Publisher<rione_msgs::msg::Command>::SharedPtr publisher_;
public:
  TestRioneMsgs();
};


TestRioneMsgs::TestRioneMsgs()
  : Node("testrionemsgs_node")
  {
    auto msg = std::make_shared<rione_msgs::msg::Command>();
    publisher_ = this->create_publisher<rione_msgs::msg::Command>("test_topic",10);
    std::cout << "command:";
    std::cin >> msg->command;
    std::cout << "content:";
    std::cin >> msg->content;
    std::cout << "command:";
    std::cin >> msg->sender;
    RCLCPP_INFO(this->get_logger(), "Pub:%s", msg->command.c_str());
    RCLCPP_INFO(this->get_logger(), "Pub:%s", msg->content.c_str());
    RCLCPP_INFO(this->get_logger(), "Pub:%s", msg->sender.c_str());
    publisher_->publish(msg);
  }


//main 
int main(int argc, char * argv[]){
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<TestRioneMsgs>());
  rclcpp::shutdown();
  return 0;
}