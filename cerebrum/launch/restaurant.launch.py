import os

from launch import LaunchDescription
import launch.actions

import launch_ros.actions

from ament_index_python.packages import get_package_prefix

from nav2_common.launch import RewrittenYaml

def generate_launch_description():
    use_sim_time = launch.substitutions.LaunchConfiguration('use_sim_time',
                                                            default='false')
    autostart = launch.substitutions.LaunchConfiguration('autostart')
    params_file = launch.substitutions.LaunchConfiguration('params')
    bt_xml_file = launch.substitutions.LaunchConfiguration('bt_xml_file')

    # Create our own temporary YAML files that include substitutions
    param_substitutions = {
        'use_sim_time': use_sim_time,
        'bt_xml_filename': bt_xml_file,
        'autostart': autostart,
    }

    configured_params = RewrittenYaml(
        source_file=params_file, rewrites=param_substitutions,
        convert_types=True
    )

    return LaunchDescription([
        launch_ros.actions.Node(
            package="turtlebot_bringup",
            node_executable="turtlebot2",
            output="screen",
            parameters=["turtlebot2.yaml"]
        ),
        launch_ros.actions.Node(
            package="ydlidar",
            node_executable="ydlidar_node",
            output="screen",
            parameters=["ydlidar.yaml"]
        ),
        launch_ros.actions.Node(
            package="sound_system",
            node_executable="sound_system",
            output="screen"
        ),
        launch_ros.actions.Node(
            package="control_system",
            node_executable="turn",
            output="screen"
        ),
        launch_ros.actions.Node(
            package="control_system",
            node_executable="localization",
            output="screen"
        ),
        launch_ros.actions.Node(
            package="control_system",
            node_executable="get_distance",
            output="screen"
        ),
        launch_ros.actions.Node(
            package="image_system",
            node_executable="image_system_node",
            output="screen"
        ),
        launch_ros.actions.Node(
            package="realsense_ros2_camera",
            node_executable="realsense_ros2_camera",
            output="screen"
        ),
        launch_ros.actions.Node(
            package="cerebrum",
            node_executable="restaurant",
            output="screen"
        ),

        # Set env var to print messages to stdout immediately
        launch.actions.SetEnvironmentVariable(
            'RCUTILS_CONSOLE_STDOUT_LINE_BUFFERED', '1'),

        launch.actions.DeclareLaunchArgument(
            'use_sim_time', default_value='false',
            description='Use simulation (Gazebo) clock if true'),

        launch.actions.DeclareLaunchArgument(
            'autostart', default_value='true',
            description='Automatically startup the nav2 stack'),

        launch.actions.DeclareLaunchArgument(
            'params',
            default_value=['nav2_params.yaml'],
            description='Full path to the ROS2 parameters file to use'),

        launch.actions.DeclareLaunchArgument(
            'bt_xml_file',
            default_value=os.path.join(get_package_prefix('nav2_bt_navigator'),
                'behavior_trees', 'navigate_w_replanning_and_recovery.xml'),
            description='Full path to the behavior tree xml file to use'),

        launch_ros.actions.Node(
            package='nav2_world_model',
            node_executable='world_model',
            output='screen',
            parameters=[configured_params]),

        launch_ros.actions.Node(
            package='dwb_controller',
            node_executable='dwb_controller',
            output='screen',
            parameters=[configured_params]),

        launch_ros.actions.Node(
            package='nav2_navfn_planner',
            node_executable='navfn_planner',
            node_name='navfn_planner',
            output='screen',
            parameters=[configured_params]),

        launch_ros.actions.Node(
            package='nav2_recoveries',
            node_executable='recoveries_node',
            node_name='recoveries',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}]),
        launch_ros.actions.Node(
            package='nav2_bt_navigator',
            node_executable='bt_navigator',
            node_name='bt_navigator',
            output='screen',
            parameters=[configured_params]),

        launch_ros.actions.Node(
            package='nav2_lifecycle_manager',
            node_executable='lifecycle_manager',
            node_name='lifecycle_manager_control',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time},
                        {'autostart': autostart},
                        {'node_names': ['world_model',
                                        'dwb_controller',
                                        'navfn_planner',
                                        'bt_navigator']}]),
    ])
