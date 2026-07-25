from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():
    ld = LaunchDescription()
    ld.add_action(
        DeclareLaunchArgument(
            "model",
            default_value="model/mobile_robot.xacro"
        )
    )
    ld.add_action(
        IncludeLaunchDescription(
            PathJoinSubstitution([
                FindPackageShare("urdf_launch"),
                "launch",
                "display.launch.py"
            ]),
            launch_arguments={
                "urdf_package":"mobile_robot",
                "urdf_package_path":LaunchConfiguration("model"),
                "jsp_gui":"true"
            }.items()
        )
    )
    return ld