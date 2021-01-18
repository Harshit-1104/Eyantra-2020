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


# import imutils
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

    warped_img = None

    ##############	ADD YOUR CODE HERE	##############
    def orderpoints(pts):
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        dif = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(dif)]
        rect[3] = pts[np.argmax(dif)]
        return rect

    def four_point_transform(image, pts):
        rect = orderpoints(pts)
        (tl, tr, bl, br) = rect
        maxWidth = 512
        maxHeight = 512
        dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype="float32")
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        return warped

    img = input_img
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)
    _, thresh = cv2.threshold(edged, 127, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow('image1', img)
    # cv2.imshow('edged', edged)
    # cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break
    # cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 2)
    # cv2.imshow("Outline", img)
    # print(img.shape)
    warped = four_point_transform(img, screenCnt.reshape(4, 2))
    # cv2.imshow('final', warped)
    warped_img = warped
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

    ##############	ADD YOUR CODE HERE	##############
    def fun(im):
        val = 0
        if im[0, 50] == 0:
            val = val + 2
        if im[99, 50] == 0:
            val = val + 8
        if im[50, 1] == 0:
            val += 1
        if im[50, 99] == 0:
            val += 4
        return val

    img = warped_img
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # print(img.shape)
    ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    img = cv2.resize(img, (1000, 1000))
    # print(img.shape)
    # cv2.imshow('IMAGE', img[0:100, 0:100])
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # print(img[0:100,0])
    l = []
    for x in range(0, 1000, 100):
        l2 = []
        for y in range(0, 1000, 100):
            im = img[x:x + 100, y:y + 100]
            val = fun(im)
            l2.append(val)
        l.append(l2)
    # print(l)

    maze_array = l
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

        print(
            '\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
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

                    print(
                        '\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
                    exit()

            else:

                print(
                    '\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
                exit()

    else:

        print('')

