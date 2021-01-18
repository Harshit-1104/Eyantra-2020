import cv2
import numpy as np

cap = cv2.VideoCapture('ballmotionwhite.m4v')
cap.set(1, 206)
ret,frame = cap.read()
#while True :
    #ret,frame = cap.read()
hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
low_red = np.array([0,100,100])
high_red = np.array([20,255,255])
red_mask = cv2.inRange(hsv_frame,low_red,high_red)
    #red = cv2.bitwise_and(frame,frame,mask = red_mask)
_, thresh = cv2.threshold(red_mask, 200, 255, cv2.THRESH_BINARY)
    #cv2.imshow('hfgsh',thresh)
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
for i in range(0, len(contours)):
    approx = cv2.approxPolyDP(contours[i], 0.001* cv2.arcLength(contours[i], True), True)
    m = cv2.moments(contours[i])
    area = cv2.contourArea(contours[i])
    if area > 3000:
        cv2.drawContours(frame, contours,i, (0, 255, 0), 2)
        cx = int(m['m10'] / m['m00'])
        cy = int(m['m01'] / m['m00'])
        print(str(cx) + " : " + str(cy))
    cv2.imshow('red',frame)
    key = cv2.waitKey(1)
    if key == 27:
        break