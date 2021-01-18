import cv2
import numpy as np

cap = cv2.VideoCapture('ballmotion.m4v')

while True:
    ret, frame = cap.read()
    #frame = cv2.resize(frame, (1550, 800))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #equ = cv2.equalizeHist(imgGray)
    h, s, v = cv2.split(hsv)
    _, thresh = cv2.threshold(s, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.imshow("other", thresh)
    for i in range(0, len(contours)):
        approx = cv2.approxPolyDP(contours[i], 0.01 * cv2.arcLength(contours[i], True), True)
        m = cv2.moments(contours[i])
        area = cv2.contourArea(contours[i])
        if len(approx) > 10 and area > 3000:
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
                print(str(cx) + " : " + str(cy))
                cv2.drawContours(frame, contours, i, (0, 255, 0), 2)

    cv2.imshow("frame", frame)
    if cv2.waitKey(40) == ord('q') or cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
