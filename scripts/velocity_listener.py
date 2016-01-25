#!/usr/bin/env python

import os
import rospy
from geometry_msgs.msg import Twist


#
# Current wiring of the Pololu DRV8835 to the Pi B+ pins
#
MOTOR_DRIVER_MODE_PIN     = 25   # 1 for Phase/Enable mode, the easiest
LEFT_MOTOR_PWM_PIN        = 22   # from 0 to 1, precision of about 0.01 
LEFT_MOTOR_DIRECTION_PIN  = 23   # 0 for Forward, 1 for Reverse
RIGHT_MOTOR_PWM_PIN       = 17
RIGHT_MOTOR_DIRECTION_PIN = 18


#
# Required initialisations
#
def init_platform():
    os.system('sudo pi-blaster')
    os.system('echo "{}=1" > /dev/pi-blaster'.format(MOTOR_DRIVER_MODE_PIN))

#
# For now, only use linear.x & angular.z (4 arrows-like commands with teleop_twist) 
#
def callback(msg):
    rospy.loginfo("* Received new velocity command *")

    left_motor_dir = 0
    right_motor_dir = 0
    left_motor_speed = msg.linear.x/2 - msg.angular.z/4
    right_motor_speed = msg.linear.x/2 + msg.angular.z/4

    rospy.loginfo("left: %.2f", msg.linear.x/2 - msg.angular.z/4)
    rospy.loginfo("right: %.2f", msg.linear.x/2 + msg.angular.z/4)

    if left_motor_speed < 0:
        left_motor_dir = 1
        left_motor_speed = abs (left_motor_speed)
    if right_motor_speed < 0:
        right_motor_dir = 1
        right_motor_speed = abs (right_motor_speed)
   
    # The actual command sent throw pi-blaster
    os.system('echo "{}={}" > /dev/pi-blaster'.format(LEFT_MOTOR_DIRECTION_PIN, left_motor_dir))
    os.system('echo "{}={:.2}" > /dev/pi-blaster'.format(LEFT_MOTOR_PWM_PIN, left_motor_speed))
    os.system('echo "{}={}" > /dev/pi-blaster'.format(RIGHT_MOTOR_DIRECTION_PIN, right_motor_dir))
    os.system('echo "{}={:.2}" > /dev/pi-blaster'.format(RIGHT_MOTOR_PWM_PIN, right_motor_speed))


def velocity_listener():
    rospy.init_node('velocity_listener')
    rospy.Subscriber("cmd_vel", Twist, callback)
    rospy.spin()

if __name__ == '__main__':
    init_platform()
    velocity_listener()
