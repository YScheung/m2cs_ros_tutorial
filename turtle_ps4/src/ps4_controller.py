#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
# hint: some imports are missing
from std_srvs.srv import Empty, EmptyRequest
from m2_ps4.msg import Ps4Data 


old_data = Ps4Data()
count = 1
def callback(data):
    global old_data
    global count

    #ps4 data is passed here

    rospy.loginfo(data.cross) 
    
    if (data.hat_ly != 0):
        t = Twist()
        speed = data.hat_ly
        t.linear.x = speed * count * 0.44 
        pub.publish(t)

    if (data.l3 == True):
        count = count + 1   

    if (data.ps == True):
        clear_path_client()

    if (data.triangle == True):
        change_color_client(0,220,0,0,0)

    if (data.circle == True):
        change_color_client(255,0,0,0,0)

    if (data.cross == True):
        change_color_client(0,0,255,0,0)

    if (data.square == True):
        change_color_client(128,0,128,0,0) 




    if (data.hat_rx == 1):
        t = Twist()
        t.angular.z = 1
        pub.publish(t)

    if (data.hat_rx == -1):
        t = Twist()
        t.angular.z = -1
        pub.publish(t) 
    

    # you should publish the velocity here

    # hint: to detect a button being pressed, you can use the following pseudocode:
    #

    old_data = data

    
    
if __name__ == '__main__':
    rospy.init_node('ps4_controller')

    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 1)  # publisher object goes here... hint: the topic type is Twist
    

    clear_path_client = rospy.ServiceProxy('clear', Empty)
    change_color_client = rospy.ServiceProxy('turtle1/set_pen', SetPen)

    sub = rospy.Subscriber('input/ps4_data', Ps4Data, callback) # subscriber object goes here

    # one service object is needed for each service called!
    #srv_col = # service client object goes here... hint: the srv type is SetPen
    # fill in the other service client object...

    rospy.spin()
