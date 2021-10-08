'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 1B of Nirikshak Bot (NB) Theme (eYRC 2020-21).
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

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_1b.py
# Functions:		applyPerspectiveTransform, detectMaze, writeToCsv
# 					[ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, csv)               ##
##############################################################
import numpy as np
import cv2
import csv
##############################################################


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################






##############################################################


def applyPerspectiveTransform(input_img):
    """
	Purpose:
	---
	takes a maze test case image as input and applies a Perspective Transfrom on it to isolate the maze

	Input Arguments:
	---
	`input_img` :   [ numpy array ]
		maze image in the form of a numpy array
	
	Returns:
	---
	`warped_img` :  [ numpy array ]
		resultant warped maze image after applying Perspective Transform
	
	Example call:
	---
	warped_img = applyPerspectiveTransform(input_img)
	"""
    bgr_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    ret,mask = cv2.threshold(bgr_img,100,255,cv2.THRESH_BINARY)
   # cv2.imshow("task", mask)
   # cv2.imshow("bgr", bgr_img)
	##############	ADD YOUR CODE HERE	##############
    
    contours, heirarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    if len(contours)!=0:
        bigcvt = contours[0]
        areas = []
        maxarea = 0
        
    #Isolating the biggest contour
    for cvt in contours:
        area = cv2.contourArea(cvt)
        areas.append(area)
    
    for cvt in contours:
        area = cv2.contourArea(cvt)
        #print(area)
        areas.append(area)
        if area>maxarea and area!= max(areas):
            bigcvt = cvt
            maxarea = area
    
    max_xplusy = 0
    for i in range(len(bigcvt)):
        if (bigcvt[i][0][0] + bigcvt[i][0][1]) > max_xplusy:
            max_xplusy = (bigcvt[i][0][0] + bigcvt[i][0][1])
            index_lr = i
    min_xplusy = max_xplusy
    for i in range(len(bigcvt)):
        if (bigcvt[i][0][0] + bigcvt[i][0][1]) < min_xplusy:
            min_xplusy = (bigcvt[i][0][0] + bigcvt[i][0][1])
            index_ul = i  
    max_yminusx = 0
    for i in range(len(bigcvt)):
        if (-bigcvt[i][0][0] + bigcvt[i][0][1]) > max_yminusx:
            max_yminusx = (-bigcvt[i][0][0] + bigcvt[i][0][1])
            index_ll = i  
    max_xminusy = 0
    for i in range(len(bigcvt)):
        if (bigcvt[i][0][0] - bigcvt[i][0][1]) > max_xminusy:
            max_xminusy = (bigcvt[i][0][0] - bigcvt[i][0][1])
            index_ur = i  
    #img = cv2.circle(input_img, (bigcvt[index_lr][0][0], bigcvt[index_lr][0][1]), 1, (0,0,255), 2)
    #img = cv2.circle(input_img, (bigcvt[index_ul][0][0], bigcvt[index_ul][0][1]), 1, (0,0,255), 2)
    #img = cv2.circle(input_img, (bigcvt[index_ll][0][0], bigcvt[index_ll][0][1]), 1, (0,0,255), 2)
    #img = cv2.circle(input_img, (bigcvt[index_ur][0][0], bigcvt[index_ur][0][1]), 1, (0,0,255), 2)
    #img = cv2.drawContours(input_img, bigcvt, -1, (0,255,0), 3)
    
    width,height = 500,500
    pts1 = np.float32([[586,45],[788,163],[411,348],[615,464]])
    pts1 = np.float32([bigcvt[index_ul], bigcvt[index_ur], bigcvt[index_ll], bigcvt[index_lr]])
    pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgOutput = cv2.warpPerspective(input_img,matrix,(width,height))
    
    #cv2.imshow("warp", imgOutput)
    #cv2.waitKey(0)
    warped_img = imgOutput
	##################################################
    return warped_img


def detectMaze(warped_img):
    """
	Purpose:
	---
	takes the warped maze image as input and returns the maze encoded in form of a 2D array

	Input Arguments:
	---
	`warped_img` :    [ numpy array ]
		resultant warped maze image after applying Perspective Transform
	
	Returns:
	---
	`maze_array` :    [ nested list of lists ]
		encoded maze in the form of a 2D array

	Example call:
	---
	maze_array = detectMaze(warped_img)
	"""
    maze_array = []
	##############	ADD YOUR CODE HERE	##############
    for j in range(10):
        row_list = []
        for i in range(10):
            num = 0
            roi = warped_img[j*50:(j+1)*50, i*50:(i+1)*50]
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            ret,mask = cv2.threshold(roi,100,255,cv2.THRESH_BINARY)
            if mask[1, 24] == 0:
                num = num + 2
            if mask[24, 1] == 0:
                num = num + 1
            if mask[24, 48] == 0:
                num = num + 4
            if mask[48, 24] == 0:
                num = num + 8  
            row_list.append(num)
            #cv2.imshow("mask", mask)
            #cv2.waitKey(0)
        maze_array.append(row_list)

	##################################################
    return maze_array 
	
    


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
def writeToCsv(csv_file_path, maze_array):

	"""
	Purpose:
	---
	takes the encoded maze array and csv file name as input and writes the encoded maze array to the csv file

	Input Arguments:
	---
	`csv_file_path` :	[ str ]
		file path with name for csv file to write
	
	`maze_array` :		[ nested list of lists ]
		encoded maze in the form of a 2D array
	
	Example call:
	---
	warped_img = writeToCsv('test_cases/maze00.csv', maze_array)
	"""

	with open(csv_file_path, 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerows(maze_array)


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    This part of the code is only for testing your solution. The function first takes 'maze00.jpg'
# 					as input, applies Perspective Transform by calling applyPerspectiveTransform function,
# 					encodes the maze input in form of 2D array by calling detectMaze function and writes this data to csv file
# 					by calling writeToCsv function, it then asks the user whether to repeat the same on all maze images
# 					present in 'test_cases' folder or not. Write your solution ONLY in the space provided in the above
# 					applyPerspectiveTransform and detectMaze functions.

if __name__ == "__main__":

	# path directory of images in 'test_cases' folder
	img_dir_path = 'test_cases/'

	# path to 'maze00.jpg' image file
	file_num = 0
	img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

	print('\n============================================')
	print('\nFor maze0' + str(file_num) + '.jpg')

    # path for 'maze00.csv' output file
	csv_file_path = img_dir_path + 'maze0' + str(file_num) + '.csv'
	
	# read the 'maze00.jpg' image file
	input_img = cv2.imread(img_file_path)

	# get the resultant warped maze image after applying Perspective Transform
	warped_img = applyPerspectiveTransform(input_img)

	if type(warped_img) is np.ndarray:

		# get the encoded maze in the form of a 2D array
		maze_array = detectMaze(warped_img)

		if (type(maze_array) is list) and (len(maze_array) == 10):

			print('\nEncoded Maze Array = %s' % (maze_array))
			print('\n============================================')
			
			# writes the encoded maze array to the csv file
			writeToCsv(csv_file_path, maze_array)

			cv2.imshow('warped_img_0' + str(file_num), warped_img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
		
		else:

			print('\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
			exit()
	
	else:

		print('\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
		exit()
	
	choice = input('\nDo you want to run your script on all maze images ? => "y" or "n": ')

	if choice == 'y':

		for file_num in range(1, 10):
			
			# path to image file
			img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

			print('\n============================================')
			print('\nFor maze0' + str(file_num) + '.jpg')

			# path for csv output file
			csv_file_path = img_dir_path + 'maze0' + str(file_num) + '.csv'
			
			# read the image file
			input_img = cv2.imread(img_file_path)
            
			# get the resultant warped maze image after applying Perspective Transform
			warped_img = applyPerspectiveTransform(input_img)

			if type(warped_img) is np.ndarray:

				# get the encoded maze in the form of a 2D array
				maze_array = detectMaze(warped_img)
                
				if (type(maze_array) is list) and (len(maze_array) == 10):

					print('\nEncoded Maze Array = %s' % (maze_array))
					print('\n============================================')
					
					# writes the encoded maze array to the csv file
					writeToCsv(csv_file_path, maze_array)

					cv2.imshow('warped_img_0' + str(file_num), warped_img)
					cv2.waitKey(0)
					cv2.destroyAllWindows()
				
				else:

					print('\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
					exit()
			
			else:

				print('\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
				exit()

	else:

		print('')
