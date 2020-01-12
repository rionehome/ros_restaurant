#include <iostream>

#define OPENPOSE_FLAGS_DISABLE_PRODUCER
#define OPENPOSE_FLAGS_DISABLE_DISPLAY
#include <openpose/headers.hpp>
//#include <openpose/flags.hpp>

#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>

#include <rclcpp/rclcpp.hpp>
#include <cv_bridge/cv_bridge.h>

#include <pcl/point_types.h>
#include <pcl/point_cloud.h>
#include <pcl_conversions/pcl_conversions.h>

#include <sensor_msgs/msg/image.hpp>
#include <sensor_msgs/msg/point_cloud2.hpp>
#include <rione_msgs/msg/command.hpp>

using namespace std;

class ImageSystem :
    public rclcpp::Node {
        private:
            // subscription
            rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr Image;
            rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr PointCloud;

            // subscriber command from cerebrum
            rclcpp::Subscription<rione_msgs::msg::Command>::SharedPtr SubscriberCommand;

            // subscribe image function
            void subscribeImage(sensor_msgs::msg::Image::SharedPtr msg);
            // subscribe pointcloud2 function
            void subscribePointCloud2(sensor_msgs::msg::PointCloud2::SharedPtr msg);
            // subscribe command from cerebrum function
            void subscribeCommandFromCerebrum(rione_msgs::msg::Command::SharedPtr msg);
            // command send function
            bool sendCommand(string command, string content, string to);
            // detect customer function
            cv::Point3d detectCustomerPosition(cv::Mat image);

            bool isRaiseYourHand(op::Array<float> poseKeypoints);
            // play shuttor sound
            void playShuttorSound();

            // image width
            int width;
            // image height
            int height;
            // opencv2 image variable
            cv::Mat image;
            // opencv2 mat varibale for pointcloud data
            cv::Mat pointcloud_image;
            cv::Mat pointcloud_depth;
            cv::Vec3b *image_src;
            cv::Vec3b *depth_src;
            // point cloud2 varibale
            pcl::PCLPointCloud2 cloud;
            pcl::PointCloud<pcl::PointXYZRGB> temp_cloud;

            // OpenPose
            op::Wrapper opWrapper{op::ThreadManagerMode::Asynchronous};

            // message
            string message;
            
            // command
            rione_msgs::msg::Command msg;
        protected:
            // publish to cerebrum
            rclcpp::Publisher<rione_msgs::msg::Command>::SharedPtr publisher2cerebrum;
            // publish to sound
            rclcpp::Publisher<rione_msgs::msg::Command>::SharedPtr publisher2sound;
            // publish to control
            rclcpp::Publisher<rione_msgs::msg::Command>::SharedPtr publisher2control;
        public:
            ImageSystem();
            ~ImageSystem();
};
