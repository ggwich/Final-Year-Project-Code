#!/usr/bin/env python3

# This script creates a ROS node "Turtlebot3_Fake"
# This node just spams the 'cmd_vel' topic with bogus Twist messages
# Made for my Final Year Project to simulate a command injection attack

import rospy
from geometry_msgs.msg import Twist

def talker():
    frequency = 10 # How many times a second the node should publish
    linearSpeed = 0 # How fast the turtlebot should move forward/back
    rotateSpeed = 2.84 # How fast the turtlebot should spin
    
    
    # Changing queue_size here had no practical effect as far as I could tell
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    
    rospy.init_node('turtlebot3_Fake', anonymous=False)
    
    # cmd_vel topic uses Twist messages
    # Turtlebot listens to this topic to receive movement instructions
    spam = Twist()
    
    # Changing angular component seems to have a noticable effect at 10Hz
    # I couldn't get anything to happen with linear at this rate
    # Adjusting other message components has no effect
    spam.linear.x = linearSpeed
    spam.angular.z = rotateSpeed
    
    
    n = 0
    rateLimiter = rospy.Rate(frequency)
    while not rospy.is_shutdown():
        # Send a message in console output every 15 minutes
        # This was just so I could see if it ever stopped, feel free to remove
        if (n % (frequency*900)) == 0:
            rospy.loginfo(f"{n} messages published")
        n += 1

        # This line actually publishes our spam message onto 'cmd_vel'
        pub.publish(spam)

        # This limits the while loop to only running at the frequency given
        rateLimiter.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
