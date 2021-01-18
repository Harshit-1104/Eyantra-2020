'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 1A - Part 1 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
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

# Team ID: 763			[ Team-ID ]
# Author List:	Akansha Gupta, Harshit Gupta, Suyash Kumar Sirvastav, Vatsal Ojha	[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_1a_part1.py
# Functions:		scan_image, isclose, quad
# 					[ Comma separated list of functions in this file ]
# Global variables:	shapes
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


# Global variable for details of shapes found in image and will be put in this dictionary, returned from scan_image function
shapes = {}


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################


def isclose(a, b, rel_tol=1e-09, abs_tol=3.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def quad(approx):  # func to diff between square rhombus trapezium parallelogram quadrilateral
    x = approx.ravel()
    m12 = (x[3] - x[1]) / (x[2] - x[0])
    m23 = (x[5] - x[3]) / (x[4] - x[2])
    m34 = (x[7] - x[5]) / (x[6] - x[4])
    m41 = (x[1] - x[7]) / (x[0] - x[6])

    l12 = np.sqrt((x[3] - x[1]) ** 2 + (x[2] - x[0]) ** 2)
    l23 = np.sqrt((x[5] - x[3]) ** 2 + (x[4] - x[2]) ** 2)
    l34 = np.sqrt((x[7] - x[5]) ** 2 + (x[6] - x[4]) ** 2)
    l41 = np.sqrt((x[1] - x[7]) ** 2 + (x[0] - x[6]) ** 2)

    c123 = isclose(l12, l23)
    c234 = isclose(l23, l34)
    c341 = isclose(l34, l41)
    c1234 = isclose(l12, l34)
    c2341 = isclose(l23, l41)
    c1241 = isclose(l12, l41)

    d13 = np.sqrt((x[5]-x[1]) ** 2 + (x[4]-x[0]) ** 2)
    d24 = np.sqrt((x[7]-x[3]) ** 2 + (x[6]-x[2]) ** 2)

    p1223 = np.sqrt(l12 ** 2 + l23 ** 2)
    p2334 = np.sqrt(l23 ** 2 + l34 ** 2)

    if c123 and c234 and c341 and c1234 and c2341 and c1241:
        if isclose(d13, np.sqrt(2) * l12):
            return 'Square'
        else:
            return 'Rhombus'
    else:
        if isclose(m12, m34) and isclose(m23, m41):
            if isclose(p1223, d13) and isclose(p2334, d24):
                return 'Rectangle'
            else:
                return 'Parallelogram'
        elif isclose(m12, m34) or isclose(m23, m41):
            return 'Trapezium'
        else:
            return 'Quadrilateral'

##############################################################


def scan_image(img_file_path):
    """
    Purpose:
    ---
    this function takes file path of an image as an argument and returns dictionary
    containing details of colored (non-white) shapes in that image

    Input Arguments:
    ---
    `img_file_path` :		[ str ]
        file path of image

    Returns:
    ---
    `shapes` :              [ dictionary ]
        details of colored (non-white) shapes present in image at img_file_path
        { 'Shape' : ['color', Area, cX, cY] }

    Example call:
    ---
    shapes = scan_image(img_file_path)
    """

    global shapes

    ##############	ADD YOUR CODE HERE	##############

    img = cv2.imread(img_file_path)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(imgGray, 240, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea)
    shapes = {}

    for i in reversed(range(0, len(contours) - 1)):
        approx = cv2.approxPolyDP(contours[i], 0.01 * cv2.arcLength(contours[i], True), True)
        area = cv2.contourArea(contours[i])
        m = cv2.moments(contours[i])
        cx = int(m['m10'] / m['m00'])
        cy = int(m['m01'] / m['m00'])
        b, g, r = img[cy, cx]  # because in open cv the image is stored in bgr format

        if r > max(g, b):
            cl = 'red'
        elif g > max(r, b):
            cl = 'green'
        elif b > max(r, g):
            cl = 'blue'
        else:
            cl = 'random'

        if len(approx) == 3:
            shapes['Triangle'] = [cl, area, cx, cy]
        elif len(approx) == 4:
            shp = quad(approx)
            shapes[shp] = [cl, area, cx, cy]
        elif len(approx) == 5:
            shapes['Pentagon'] = [cl, area, cx, cy]
        elif len(approx) == 6:
            shapes['Hexagon'] = [cl, area, cx, cy]
        else:
            shapes['Circle'] = [cl, area, cx, cy]

    ##################################################

    return shapes


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
#
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    the function first takes 'Sample1.png' as input and runs scan_image function to find details
#                   of colored (non-white) shapes present in 'Sample1.png', it then asks the user whether
#                   to repeat the same on all images present in 'Samples' folder or not

if __name__ == '__main__':
    curr_dir_path = os.getcwd()
    print('Currently working in ' + curr_dir_path)

    # path directory of images in 'Samples' folder
    img_dir_path = curr_dir_path + '/Samples/'

    # path to 'Sample1.png' image file
    file_num = 1
    img_file_path = img_dir_path + 'Sample' + str(file_num) + '.png'

    print('\n============================================')
    print('\nLooking for Sample' + str(file_num) + '.png')

    if os.path.exists('Samples/Sample' + str(file_num) + '.png'):
        print('\nFound Sample' + str(file_num) + '.png')

    else:
        print('\n[ERROR] Sample' + str(file_num) + '.png not found. Make sure "Samples" folder has the selected file.')
        exit()

    print('\n============================================')

    try:
        print('\nRunning scan_image function with ' + img_file_path + ' as an argument')

        shapes = scan_image(img_file_path)

        if type(shapes) is dict:
            print(shapes)
            print('\nOutput generated. Please verify.')

        else:
            print('\n[ERROR] scan_image function returned a ' + str(type(shapes)) + ' instead of a dictionary.\n')
            exit()

    except Exception:
        print('\n[ERROR] scan_image function is throwing an error. Please debug scan_image function')
        exit()

    print('\n============================================')

    choice = input('\nWant to run your script on all the images in Samples folder ? ==>> "y" or "n": ')

    if choice == 'y':

        file_count = 2

        for file_num in range(file_count):

            # path to image file
            img_file_path = img_dir_path + 'Sample' + str(file_num + 1) + '.png'

            print('\n============================================')
            print('\nLooking for Sample' + str(file_num + 1) + '.png')

            if os.path.exists('Samples/Sample' + str(file_num + 1) + '.png'):
                print('\nFound Sample' + str(file_num + 1) + '.png')

            else:
                print('\n[ERROR] Sample' + str(file_num + 1) + '.png not found. Make sure "Samples" folder has the '
                                                               'selected file.')
                exit()

            print('\n============================================')

            try:
                print('\nRunning scan_image function with ' + img_file_path + ' as an argument')
                shapes = scan_image(img_file_path)

                if type(shapes) is dict:
                    print(shapes)
                    print('\nOutput generated. Please verify.')

                else:
                    print(
                        '\n[ERROR] scan_image function returned a ' + str(type(shapes)) + ' instead of a dictionary.\n')
                    exit()

            except Exception:
                print('\n[ERROR] scan_image function is throwing an error. Please debug scan_image function')
                exit()

            print('\n============================================')

    else:
        print('')
