'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 1A - Part 2 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''

# Team ID:			[ 763 ]
# Author List:		[ Akansha Gupta, Harshit Gupta, Suyash Kumar Sirvastav, Vatsal Ojha ]
# Filename:			task_1a_part2.py
# Functions:		process_video
# 					[ Comma separated list of functions in this file ]
# Global variables:	frame_details
# 					[ List of global variables defined in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, os)                ##
##############################################################
import cv2
import numpy as np
import os
##############################################################


# Global variable for details of frames seleced in the video will be put in this dictionary, returned from process_video function
frame_details = {}


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################




##############################################################


def process_video(vid_file_path, frame_list):

	"""
	Purpose:
	---
	this function takes file path of a video and list of frame numbers as arguments
	and returns dictionary containing details of red color circle co-ordinates in the frame

	Input Arguments:
	---
	`vid_file_path` :		[ str ]
		file path of video
	`frame_list` :			[ list ]
		list of frame numbers

	Returns:
	---
	`frame_details` :		[ dictionary ]
		co-ordinate details of red colored circle present in selected frame(s) of video
		{ frame_number : [cX, cY] }

	Example call:
	---
	frame_details = process_video(vid_file_path, frame_list)
	"""

	global frame_details

	##############	ADD YOUR CODE HERE	##############
	cap = cv2.VideoCapture(vid_file_path)
	for frame_no in frame_list:
		cap.set(1, frame_no-1) # 0 based indexing
		ret, frame = cap.read()

		if frame is None:
			break

		# frame = cv2.resize(frame, (1300, 700))
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		low_red = np.array([0, 202, 73])
		high_red = np.array([2, 255, 216])

		mask4 = cv2.inRange(hsv, low_red, high_red)
		_, thresh = cv2.threshold(mask4, 200, 255, cv2.THRESH_BINARY)
		contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		for i in range(0, len(contours)):
			approx = cv2.approxPolyDP(contours[i], 0.01 * cv2.arcLength(contours[i], True), True)
			m = cv2.moments(contours[i])
			area = cv2.contourArea(contours[i])
			if len(approx) > 5 and area > 3000:
				cx = int(m['m10'] / m['m00'])
				cy = int(m['m01'] / m['m00'])

				b, g, r = frame[cy, cx]  # because in open cv the image is stored in bgr format
				if r > max(g, b):
					cl = 'red'
				elif g > max(r, b):
					cl = 'green'
				elif b > max(r, g):
					cl = 'blue'
				else:
					cl = 'random'

				if cl == 'red':
					frame_details[frame_no] = [cx, cy]

		cv2.destroyAllWindows()

	##################################################

	return frame_details


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    the function first takes input for selecting one of two videos available in Videos folder
#                   and a input list of frame numbers for which the details are to be calculated. It runs process_video
#                   function on these two inputs as argument.

if __name__ == '__main__':

	curr_dir_path = os.getcwd()
	print('Currently working in '+ curr_dir_path)

	# path directory of videos in 'Videos' folder
	vid_dir_path = curr_dir_path + '/Videos/'
	
	try:
		file_count = len(os.listdir(vid_dir_path))
	
	except Exception:
		print('\n[ERROR] "Videos" folder is not found in current directory.')
		exit()
	
	print('\n============================================')
	print('\nSelect the video to process from the options given below:')
	print('\nFor processing ballmotion.m4v from Videos folder, enter \t=> 1')
	print('\nFor processing ballmotionwhite.m4v from Videos folder, enter \t=> 2')
	
	choice = input('\n==> "1" or "2": ')

	if choice == '1':
		vid_name = 'ballmotion.m4v'
		vid_file_path = vid_dir_path + vid_name
		print('\n\tSelected video is: ballmotion.m4v')
	
	elif choice=='2':
		vid_name = 'ballmotionwhite.m4v'
		vid_file_path = vid_dir_path + vid_name
		print('\n\tSelected video is: ballmotionwhite.m4v')
	
	else:
		print('\n[ERROR] You did not select from available options!')
		exit()
	
	print('\n============================================')

	if os.path.exists(vid_file_path):
		print('\nFound ' + vid_name)
	
	else:
		print('\n[ERROR] ' + vid_name + ' file is not found. Make sure "Videos" folders has the selected file.')
		exit()
	
	print('\n============================================')

	print('\nEnter list of frame(s) you want to process, (between 1 and 404) (without space & separated by comma) (for example: 33,44,95)')

	frame_list = input('\nEnter list ==> ')
	frame_list = list(frame_list.split(','))

	try:
		for i in range(len(frame_list)):
			frame_list[i] = int(frame_list[i])
		print('\n\tSelected frame(s) is/are: ', frame_list)
	
	except Exception:
		print('\n[ERROR] Enter list of frame(s) correctly')
		exit()
	
	print('\n============================================')

	try:
		print('\nRunning process_video function on', vid_name, 'for frame following frame(s):', frame_list)
		frame_details = process_video(vid_file_path, frame_list)

		if type(frame_details) is dict:
			print(frame_details)
			print('\nOutput generated. Please verify')
		
		else:
			print('\n[ERROR] process_video function returned a ' + str(type(frame_details)) + ' instead of a dictionary.\n')
			exit()
	
	except Exception:
		print('\n[ERROR] process_video function is throwing an error. Please debug process_video function')
		exit()

	print('\n============================================')

