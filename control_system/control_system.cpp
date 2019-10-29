#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp>

#include "rione_msgs/msg/command.hpp"

using namespace std::chrono_literals;

// Class definition
class ControlSystem : public rclcpp::Node{
private:
  rclcpp::Subscription<rione_msgs::msg::Command>::SharedPtr subscription_;

public:
  ControlSystem();
  void print_msg();
};


ControlSystem::ControlSystem()
  : Node("controlsystem_node")
  {
    auto callback =
      [this](const rione_msgs::msg::Command::SharedPtr msg) -> void
      {
        if (msg->command=="print")
        {
            RCLCPP_INFO(this->get_logger(), "I heard: %s", msg->command.c_str());
            RCLCPP_INFO(this->get_logger(), "I heard: %s", msg->content.c_str());
            RCLCPP_INFO(this->get_logger(), "I heard: %s", msg->sender.c_str());
            ControlSystem::print_msg();
        }
      };

    subscription_ = create_subscription<rione_msgs::msg::Command>(
      "test_topic", callback);
  }

void ControlSystem::print_msg()
{
    std::cout << "print function called!" << std::endl;
}


//main 
int main(int argc, char * argv[]){
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ControlSystem>());
  rclcpp::shutdown();
  return 0;
}