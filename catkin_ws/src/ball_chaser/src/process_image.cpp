#include "ros/ros.h"
#include "ball_chaser/DriveToTarget.h"
#include <sensor_msgs/Image.h>

// Define a global client that can request services
ros::ServiceClient client;

// This function calls the command_robot service to drive the robot in the specified direction
void drive_robot(float lin_x, float ang_z)
{
     ROS_INFO_STREAM("Driving robot: linear_x=" << lin_x << ", angular_z=" << ang_z);

    ball_chaser::DriveToTarget srv;
    srv.request.linear_x = lin_x;
    srv.request.angular_z = ang_z;

    if (!client.call(srv))
    {
        ROS_ERROR("Failed to call service command_robot");
    }
}

// This callback function continuously executes and reads the image data
void process_image_callback(const sensor_msgs::Image img)
{

    int white_pixel = 255;

    int ball_x_position = -1; 
    bool ball_found = false;  

    for (int i = 0; i < img.height * img.width; ++i)
    {
      
        if (img.data[i * 3] == white_pixel &&
            img.data[i * 3 + 1] == white_pixel &&
            img.data[i * 3 + 2] == white_pixel)
        {
            ball_x_position = i % img.width; 
            ball_found = true;
            break; 
        }
    }

    if (ball_found)
    {
        int left_boundary = img.width / 3;
        int right_boundary = 2 * img.width / 3;

        if (ball_x_position < left_boundary)
        {
            ROS_INFO_STREAM("White ball detected on the LEFT. Turning left.");
            drive_robot(0.1, 0.5); 
        }
        else if (ball_x_position < right_boundary)
        {
            ROS_INFO_STREAM("White ball detected in the CENTER. Driving straight.");
            drive_robot(0.3, 0.0); 
        }
        else
        {
            ROS_INFO_STREAM("White ball detected on the RIGHT. Turning right.");
            drive_robot(0.1, -0.5);
        }
    }
    else
    {
        ROS_INFO_STREAM("No white ball detected. Stopping robot.");
        drive_robot(0.0, 0.0); 
    }
}

int main(int argc, char** argv)
{
    // Initialize the process_image node and create a handle to it
    ros::init(argc, argv, "process_image");
    ros::NodeHandle n;

    // Define a client service capable of requesting services from command_robot
    client = n.serviceClient<ball_chaser::DriveToTarget>("/ball_chaser/command_robot");

    // Subscribe to /camera/rgb/image_raw topic to read the image data inside the process_image_callback function
    ros::Subscriber sub1 = n.subscribe("/camera/rgb/image_raw", 10, process_image_callback);

    // Handle ROS communication events
    ros::spin();

    return 0;
}