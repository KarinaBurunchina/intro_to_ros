#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64

getdata = 2.8

def callback(data):
    print("Angle: " + str(data.data))
    global getdata #to use variable outside the function
    getdata = data.data 
    
def rotate_listen():
	
	#initializing node
    rospy.init_node('rotate_listen', anonymous=True)
    
    #declaring that node is publishing to the joint3 topic with msg type Float64
    pub = rospy.Publisher('/robot/joint3_position_controller/command', Float64, queue_size = 10)
    
    rate = rospy.Rate(15) # 15hz rate for looping
    
    msg_old = 2.0 #stores a previous input value
    
    while not rospy.is_shutdown():
    #declares that node subscribes to the Karya topic with the msg type Float64
    	rospy.Subscriber('/Karya', Float64, callback)
    	
    	msg_to_send = getdata #recieve value from subscriber
    	print ("Recieved angle: " + str(msg_to_send)) #verification
    	
    	#Compare: if value is less than the previous input -> publish
    	if msg_to_send <= msg_old:
    		msg_old = msg_to_send
    		pub.publish(msg_to_send)
    		rospy.loginfo("isMoving goalpos to " + str(msg_to_send))
    	rate.sleep()

if __name__ == '__main__':
    try:
    	rotate_listen()
    except rospy.ROSInterruptException:
        pass
