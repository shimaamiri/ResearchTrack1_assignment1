from __future__ import print_function

import time
from sr.robot import *

#initial values
a_th = 2.0 #Threshold for the control of the linear distance

d_th = 0.4 #Threshold for the control of the orientation


R = Robot()
""" instance of the class Robot"""


def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    
    
def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    

def find_silver_token():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist=2
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==2:
	return -1, -1
    else:
   	return dist, rot_y
   	
   	
def find_golden_token():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist=1
    for token in R.see():
        if token.dist < dist and -45<token.rot_y<45 and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==1:
	return -1, -1
    else:
   	return dist, rot_y 
   	
   	
def right_wall():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the robot from golden tokens on the right side 
	rot_y (float): angle between the robot and the golden tokens on the right side
    """
    dist=100
    for token in R.see():
        if token.dist < dist and 65<token.rot_y<115 and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y
   	
   	
def left_wall():
    """
    Function to calculate distance from left wall

    Returns:
	dist (float): distance of the robot from golden tokens on the left side 
	rot_y (float): angle between the robot and the golden tokens on the left side 
    """
    dist=100
    for token in R.see():
        if token.dist < dist and -115<token.rot_y<-65 and token.info.marker_type is MARKER_TOKEN_GOLD :
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y
   	
   	
def grab_token(dist,rot_y):
    """
    Function to grab silver tokens

    arguments:
	dist (float): distance of the closest silver token 
	rot_y (float): angle between the robot and the silver token 
    """
    if dist <d_th and -70<rot_y<70: # if we are close to the token, we try grab it.
        if R.grab(): # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
            print("Gotcha!")
	    turn(30,2)
	    drive(30,0.2)
	    R.release()
	    drive(-30,0.8)
	    turn(-30,2)
	
    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
	print("Go forward")
        drive(30, 0.2)
    elif rot_y < -a_th  and -70<rot_y<70: # if the robot is not well aligned with the token, we move it on the left or on the right
        print("Left a bit...")
        turn(-5, 0.2)
    elif rot_y > a_th and -70<rot_y<70:
        print("Right a bit...")
        turn(+5, 0.2)
    
	

while 1:
 """
 Main loop, 
 while the conditions are satisfied, it iterates until the user terminate the program 
    
 """
 #obtains initial values 
 dist, rot_y = find_silver_token()
 g_dist, g_rot_y = find_golden_token()
 r_dist = right_wall() #distance from left wall
 l_dist = left_wall()  #distance from left wall

 #when the robot approaches the wall, changes its orientation	    
 if g_dist != -1:
     if (l_dist > r_dist):
	print("wall..turn left!" )
	turn(-10, 0.2)	
     elif (l_dist < r_dist):
	print("Wall..turn right!") 
	turn(10,0.2) 
 
 #when there is no silver token, the robot can freely go forward		
 if dist== -1 and g_dist== -1:
    print("Go forward!")
    drive(60,0.1)
    
 #when a silver token is detected, the robot trys to catch it		
 if dist!= -1:
    grab_token(dist,rot_y)
    drive(60,0.1)
 
