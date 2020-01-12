#include "image_system/image_system.hpp"

using namespace std;

ImageSystem::ImageSystem() : Node("image_system") {

    //
    // SUBSCRIBER : subscribe image data from realsense
    //
    Image = this->create_subscription<sensor_msgs::msg::Image>(
        "/camera/color/image_raw",
        10,
        [this](sensor_msgs::msg::Image::SharedPtr msg){
            subscribeImage(msg);
        }
    );

    //
    // SUBSCRIBER : subscribe pointcloud2 data from realsense
    //
    PointCloud = this->create_subscription<sensor_msgs::msg::PointCloud2>(
        "/camera/depth/color/points",
        10,
        [this](sensor_msgs::msg::PointCloud2::SharedPtr msg){
            subscribePointCloud2(msg);
        }
    );

    //
    // SUBSCRIBER : subscribe command data from cerebrum
    //
    SubscriberCommand = this->create_subscription<rione_msgs::msg::Command>(
        "/image_system/command",
        10,
        [this](rione_msgs::msg::Command::SharedPtr msg){
            subscribeCommandFromCerebrum(msg);
        }
    );
    
    //
    // PUBLISHER : publish command data to cerebrum
    //
    publisher2cerebrum = this->create_publisher<rione_msgs::msg::Command>(
        "cerebrum/command",
        10
    );

    //
    // PUBLISHER : publish command data to sound
    //
    publisher2sound = this->create_publisher<rione_msgs::msg::Command>(
        "sound_system/command",
        10
    );

    //
    // PUBLSIHER : publish command data to control
    //
    publisher2control = this->create_publisher<rione_msgs::msg::Command>(
        "control_system/command",
        10
    );

    //
    // PUBLISHER : publish goal data to navigation
    //
    publisher2navigation = this->create_publisher<geometry_msgs::msg::PoseStamped>(
        "move_base_simple/goal",
        10
    );

    opWrapper.start();
    RCLCPP_INFO(this->get_logger(), "FINISH SETUP");

}

ImageSystem::~ImageSystem() {
}

void ImageSystem::subscribeCommandFromCerebrum(rione_msgs::msg::Command::SharedPtr msg){
    // get command message for detecting customer.
    if (msg->command == "detect") {
        if (msg->content == "customer") {
            RCLCPP_INFO(this->get_logger(), "DETECTING CUSTOMER ...");
            playShuttorSound();
            cv::Point3d PersonPosition = detectCustomerPosition(pointcloud_image);
            sendGoalPosition(PersonPosition);
        }
    }
}


//
// DEFINITION : CUSTOMER
//
// This program say customer raised their hand left or right!!!
//
cv::Point3d ImageSystem::detectCustomerPosition(cv::Mat target_image){
    int person_number;
    // 1. get cv mat image and convert openpose image data for detecting analys.
    const op::Matrix imageToProcess = OP_CV2OPCONSTMAT(target_image);
    // 2. analys human pose...
    auto datumProcessed = opWrapper.emplaceAndPop(imageToProcess);
    RCLCPP_INFO(this->get_logger(), "GOT HUMAN POSE");

    // detect customer raised hand left or right.
    if (datumProcessed != nullptr) {
        for(person_number=0; person_number<datumProcessed->size(); person_number++){
            // check customer raised hand
            if (isRaiseYourHand(datumProcessed->at(person_number)->poseKeypoints)) {
                // get knee position
                auto RKneePoint = temp_cloud[
                    (int)datumProcessed->at(person_number)->poseKeypoints[10*3+0]+
                    (int)datumProcessed->at(person_number)->poseKeypoints[10*3+1]*width
                ];

                auto LKneePoint = temp_cloud[
                    (int)datumProcessed->at(person_number)->poseKeypoints[13*3+0]+
                    (int)datumProcessed->at(person_number)->poseKeypoints[13*3+1]*width
                ];

                float person_x = (RKneePoint.x + LKneePoint.x)/2.0;
                float person_y = (RKneePoint.y + LKneePoint.y)/2.0;
                float person_z = (RKneePoint.z + LKneePoint.z)/2.0;

                cout << "Position x: " << (RKneePoint.x + LKneePoint.x)/2.0 << endl;
                cout << "Position y: " << (RKneePoint.y + LKneePoint.y)/2.0 << endl;
                cout << "Position z: " << (RKneePoint.z + LKneePoint.z)/2.0 << endl;

                cv::Point3d PersonPosition(person_x, person_y, person_z);
                return PersonPosition;
            }
        }
    }

    //cout << datumProcessed->at(0)->poseKeypoints.toString() << endl;
}

// check position of RShoulder, RElbow, RWrist, LShoulder, LElbow, LWrist
bool ImageSystem::isRaiseYourHand(op::Array<float> poseKeypoints){
    float RShoulder, RElbow, RWrist, LShoulder, LElbow, LWrist;

    RShoulder = poseKeypoints[4*3+1];
    RElbow    = poseKeypoints[3*3+1];
    RWrist    = poseKeypoints[2*3+1];

    LShoulder = poseKeypoints[7*3+1];
    LElbow    = poseKeypoints[6*3+1];
    LWrist    = poseKeypoints[5*3+1];

    if (RShoulder < RElbow or RElbow < RWrist){
        return true;
    }

    if (LShoulder < LElbow or LElbow < LWrist){
        return true;
    }
    return false;
}

void ImageSystem::playShuttorSound(){
    // [TODO] You need to change path on your enviroment!!!
    FILE *aplay = popen("aplay ../data/camera-shutter3.wav", "w");
    pclose(aplay);
}

void ImageSystem::subscribeImage(sensor_msgs::msg::Image::SharedPtr msg){
    // translate from Image message to cv image
    try {
        image = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8)->image;
    } catch(cv_bridge::Exception& e){
        RCLCPP_ERROR(this->get_logger(), e.what());
    }
}

void ImageSystem::subscribePointCloud2(sensor_msgs::msg::PointCloud2::SharedPtr msg){
    width = msg->width;
    height = msg->height;
    // translate from PointCloud2 message to PointCloud of PCL.
    pcl_conversions::toPCL(*msg, cloud);
    pcl::fromPCLPointCloud2(cloud, temp_cloud);

    // convert from PointCloud2 to image and depth data.
    pointcloud_image = cv::Mat::zeros(msg->width, msg->height, CV_8UC3);
    pointcloud_depth = cv::Mat::zeros(msg->width, msg->height, CV_64F);

    // separete image data and depth data
    int w, h;
    for(h=0; h<height; h++){
        for(w=0; w<width; w++){
            image_src = pointcloud_image.ptr<cv::Vec3b>(h);
            depth_src = pointcloud_depth.ptr<cv::Vec3b>(h);
            image_src[w][0] = (char)temp_cloud[msg->width*h+w].b;
            image_src[w][1] = (char)temp_cloud[msg->width*h+w].g;
            image_src[w][2] = (char)temp_cloud[msg->width*h+w].r;
            depth_src[w]    = temp_cloud[msg->width*h+w].z;
        }
    }
}

bool ImageSystem::sendCommand(string command, string content, string to){
    msg.flag = true;
    msg.command = command;
    msg.content = content;
    msg.sender  = to;
    
    if (to == "cerebrum"){
        //publisher2cerebrum
    } else if (to == "sound"){
        //publisher2sound
    } else if (to == "control"){
        //publisher2control
    } else {
        RCLCPP_WARN(this->get_logger(), "COULD'T SEND MESSAGE");
        return false;
    }
}

bool ImageSystem::sendGoalPosition(cv::Point3d position){
    customer_position.header.frame_id    = "map";
    customer_position.pose.position.x    = position.x;
    customer_position.pose.position.y    = position.y;
    customer_position.pose.orientation.z = 1.0;
    publisher2navigation->publish(customer_position);

    RCLCPP_INFO(this->get_logger(), "SUCCESSED TO SEND GOAL POSITION TO NAVIGATION");

    return true;
}
