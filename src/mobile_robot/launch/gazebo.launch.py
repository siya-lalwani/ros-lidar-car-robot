from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.actions import ExecuteProcess, TimerAction
import os
import xacro

def generate_launch_description():
    package_name = "mobile_robot"
    package_path = get_package_share_directory(package_name)
    xacro_file = os.path.join(
        package_path,
        "model",
        "mobile_robot.xacro"
    )
    robot_description = xacro.process_file(xacro_file).toxml()
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "robot_description":robot_description,
                "use_sim_time":True
            }
        ]
    )
    gazebo = ExecuteProcess(
        cmd=[
            "gz",
            "sim",
            "-r",
            "empty.sdf"
        ],
        output="screen"
    )
    bridge=Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
        "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
        "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
        "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
        "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
        "/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V"
        ],
        output="screen"
    )
    spawn_robot=Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
        "-world", "empty",
        "-topic", "robot_description",
        "-name", "mobile_robot"
        ],
        output="screen"
    )
    return LaunchDescription([
        robot_state_publisher,
        gazebo,
        bridge,
        TimerAction(
            period=3.0,
            actions=[spawn_robot]
        )
    ])