import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    # Get package directory
    mobile_robot_dir = get_package_share_directory('mobile_robot')
    
    # Paths to URDF and other files
    urdf_file = os.path.join(mobile_robot_dir, 'model', 'mobile_robot.xacro')
    gazebo_file = os.path.join(mobile_robot_dir, 'model', 'mobile_robot.gazebo')
    rviz_config_file = os.path.join(mobile_robot_dir, 'rviz', 'config.rviz')
    bridge_config_file = os.path.join(mobile_robot_dir, 'parameters', 'bridge_parameters.yaml')
    
    # Launch arguments
    use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )
    
    # Start Gazebo server
    start_gazebo_server_cmd = Node(
        package='gazebo_ros',
        executable='gzserver',
        output='screen',
        arguments=['--verbose', '-s', 'libgazebo_ros_factory.so', '-s', 'libgazebo_ros_init.so']
    )
    
    # Start Gazebo client (GUI)
    start_gazebo_client_cmd = Node(
        package='gazebo_ros',
        executable='gzclient',
        output='screen'
    )
    
    # Robot State Publisher to publish TF
    robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        arguments=[urdf_file],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )
    
    # Gazebo spawner node
    spawn_entity_cmd = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'mobile_robot',
            '-topic', 'robot_description',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.5'
        ],
        output='screen'
    )
    
    # ROS2 Gazebo Bridge
    bridge_cmd = Node(
        package='ros_gzbridge',
        executable='dynamic_bridge',
        parameters=[
            {'config_file': bridge_config_file},
            {'use_sim_time': True}
        ],
        output='screen'
    )
    
    # RViz2
    rviz_cmd = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )
    
    ld = LaunchDescription()
    
    # Add actions
    ld.add_action(use_sim_time)
    ld.add_action(start_gazebo_server_cmd)
    ld.add_action(start_gazebo_client_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(spawn_entity_cmd)
    ld.add_action(bridge_cmd)
    ld.add_action(rviz_cmd)
    
    return ld
