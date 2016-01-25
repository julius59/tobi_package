cmake_minimum_required(VERSION 2.8.3)
project(tobi_package)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  rospy
)

catkin_package()
