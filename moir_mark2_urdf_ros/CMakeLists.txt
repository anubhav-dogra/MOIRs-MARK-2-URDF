cmake_minimum_required(VERSION 2.8.3)
project(moir_mark2_urdf_ros)

find_package(catkin REQUIRED COMPONENTS
  rospy
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES modular_robot
#  CATKIN_DEPENDS rospy
#  DEPENDS system_lib
)
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

