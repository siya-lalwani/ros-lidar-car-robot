import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """Simplified launch file for debugging"""
    
    # Get package directory
    mobile_robot_dir = get_package_share_directory('mobile_robot')
    
    # Paths to files
    urdf_file = os.path.join(mobile_robot_dir, 'model', 'mobile_robot.xacro')
    
    # Robot State Publisher (loads URDF and publishes TF)
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        arguments=[urdf_file],
        parameters=[{'use_sim_time': True}],
        output='screen',
        emulate_tty=True
    )
    
    # Gazebo Server
    gazebo_server = Node(
        package='gazebo_ros',
        executable='gzserver',
        output='screen',
        emulate_tty=True,
        arguments=[
            '-s', 'libgazebo_ros_init.so',
            '-s', 'libgazebo_ros_factory.so'
        ]
    )
    
    # Gazebo Client (GUI) - optional, comment out for headless mode
    gazebo_client = Node(
        package='gazebo_ros',
        executable='gzclient',
        output='screen',
        emulate_tty=True
    )
    
    # Spawn the robot
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        output='screen',
        emulate_tty=True,
        arguments=[
            '-entity', 'mobile_robot',
            '-topic', 'robot_description'
        ]
    )
    
    ld = LaunchDescription()
    
    # Add nodes in order
    ld.add_action(gazebo_server)
    ld.add_action(robot_state_publisher)
    ld.add_action(spawn_entity)
    ld.add_action(gazebo_client)
    
    return ld
