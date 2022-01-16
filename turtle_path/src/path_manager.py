#!/usr/bin/env python

import rospy
from math import pi, fmod, sin, cos, sqrt
from geometry_msgs.msg import Twist
# hint: some imports are missing 
from turtle_path.srv import * 
from turtlesim.msg import Pose

cur_pos = Pose()

def cb_pose(data): # get the current position `xxfrom subscribing the turtle position
    global cur_pos
    cur_pos = data

def cb_walk(req):
    if (req.distance < 0):
        return False


    # hint: calculate the projected (x, y) after walking the distance,
    # and return false if it is outside the boundary

    final_x = cur_pos.x + req.distance * cos(cur_pos.theta)
    final_y = cur_pos.y + req.distance * sin(cur_pos.theta)


    if (final_y < 0 or final_y > 11):
        return False

    if (final_x < 0 or final_x > 11):
        return False


    rate = rospy.Rate(100) # 100Hz control loop


    while (not ( ((cur_pos.x >= final_x - 0.05) and (cur_pos.x <= final_x + 0.05)) and ( (cur_pos.y > final_y - 0.05) and (cur_pos.y < final_y + 0.05)  ))): # control loop

        # in each iteration of the control loop, publish a velocity
        vel = Twist()
        distance = sqrt( (final_y - cur_pos.y) ** 2 + (final_x - cur_pos.x) ** 2 )
        vel.linear.z = cur_pos.theta
        vel.linear.x = distance
        pub.publish(vel)

        # hint: you need to use the formula for distance between two points

        rate.sleep()

    vel = Twist() # publish a velocity 0 at the end, to ensure the turtle really stops
    pub.publish(vel)

    return True



def cb_orientation(req):

    rate = rospy.Rate(100) # 100Hz control loop

    if ((req.orientation % (2 * pi))  < pi): 
        scale = req.orientation % pi
    else:
        scale = pi - req.orientation % pi  


    while (not ( (abs(cur_pos.theta) <= scale + 0.05)  and (abs(cur_pos.theta) >= scale - 0.05))): # control loop 
   # in each iteration of the control loop, publish a velocity
        vel = Twist()

        # hint: signed smallest distance between two angles: 
        # see https://stackoverflow.com/questions/1878907/the-smallest-difference-between-2-angles
        dist = fmod(req.orientation - cur_pos.theta + pi + 2 * pi, 2 * pi) - pi
        
        if (dist > 0):
            vel.angular.z = 0.05

        else:
            vel.angular.z = -0.05

        pub.publish(vel)

        rate.sleep()


    vel = Twist() # publish a velocity 0 at the end, to ensure the turtle really stops
    vel.angular.z = 0
    pub.publish(vel) 

    return True



if __name__ == '__main__':
    rospy.init_node('path_manager')
    
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 1) # publisher of the turtle velocity
    sub = rospy.Subscriber('/turtle1/pose', Pose , cb_pose) # subscriber of the turtle position, callback to cb_pose
    
    ## init each service server here:
    # rospy.Service( ... )		# callback to cb_orientation
    # rospy.Service( ... )		# callback to cb_walk
    
    rospy.Service('set_orientation', SetOrientation, cb_orientation)
    rospy.Service('walk_distance', WalkDistance, cb_walk)


    rospy.spin()
