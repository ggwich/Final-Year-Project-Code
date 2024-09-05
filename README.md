# What is this?
For my Final Year Project at Cardiff University, I compared how well various machine learning models performed for the task of network-based intrusion detection in ROS systems. 
As a part of this project, I needed to simulate an attack where commands were injected over a network to a ROS system, so that I had data to train/test the models with.

# What are the scripts for?
These scripts implement an attack method outlined in *"Security for the Robot Operating System"* (Dieber et al., 2017), where an attacker utilises XML-RPC calls to identify a target subscriber and manipulate which publishers they receive topic messages from. In non-ROS terms, this just means we lie to the robot about where it should be getting its instructions or data from.

In the case of these scripts, "[spam_node.py](https://github.com/ggwich/Final-Year-Project-Code/blob/main/cmd_vel/spam_node.py)" creates a node which will spam messages to either the 'cmd_vel' or 'scan' topics of a Turtlebot3 Burger robot running in a Gazebo simulation, with the goal of interfering with whatever the robot was doing. 
The second script, "[node_injector.py](https://github.com/ggwich/Final-Year-Project-Code/blob/main/cmd_vel/node_injector.py)", is then run which will periodically inject this node as a publisher in parallel to the legitimate publisher for whichever subscriber node is being targetted.
