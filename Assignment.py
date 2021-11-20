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
    dist=4
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==4:
	return -1, -1
    else:
   	return dist, rot_y
   	
 

def check_wall():
    """
    Function to find the closest golden box

    Returns:
	w_th (float): distance of the closest golden box (-1 if the robot is not close to any golden box)
	w_rot_y (float): angle between the robot and the closest golden box (-1 if the robot is not near any golden box)
    """
 
    W_th=0.8
    W_rot_y=0
    for token in R.see():
        if token.dist < W_th and token.info.marker_type is MARKER_TOKEN_GOLD:
            W_th=token.dist
	    W_rot_y=token.rot_y
    if W_th==0.8:
	return -1, -1
    else:
   	return W_th, W_rot_y
   	
   	
def avoid_wall(W_rot_y):
    """
    Function to avoid crushing into wall

    argument:
	w_rot_y (float): angle between the robot and the closest golden box
    """
    W_R=[] #list of closest golden tokens located pn the right
    W_L=[] #list of closest golden tokens located pn the left
 
    if -80<W_rot_y<-1: #if the wall is on the left side of the robot
       print("wall...turn right")
       print(W_rot_y)
       turn(4,2)
    elif 1<W_rot_y<80: #if the wall is on the right side of the robot
       print("wall...turn left")
       print(W_rot_y)
       turn(-4,2)
    elif -1<W_rot_y<1: #if the wall is in front of the robot
       print("wall...front")
       for token in R.see():
         if 45<token.rot_y<135 and token.dist < 1.5 and token.info.marker_type is MARKER_TOKEN_GOLD:
	    W_R.append(token) 
         if -135<token.rot_y<-45 and token.dist < 1.5 and token.info.marker_type is MARKER_TOKEN_GOLD:
	    W_L.append(token)
       if len(W_L)<len(W_R):
           print("left")
           turn(-4,2)
       else:
           print("right")
           turn(4,2)
    else:
       drive(30,0.1)           
        	
        	
   	
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
 W_th, W_rot_y = check_wall()

 #if the distance of robot from wall is less than a threshold, we make the robot turn 
 if W_th!=-1:           
    avoid_wall(W_rot_y)
   
 #if the robot has enough distance from wall, it can search for the silver tokens   
 if W_th==-1:  
    if dist==-1 and -70<rot_y<70: # if no token is detected, we make the robot drive 
	print("No silver token!!")
	drive(30,0.1)
    else:
        grab_token(dist,rot_y)
        drive(30,0.1)
