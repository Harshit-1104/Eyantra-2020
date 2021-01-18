import cv2
import numpy as np


def nothing(x):
    print(x)


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


cap = cv2.VideoCapture('ballmotion.m4v')
cv2.namedWindow('image')
cv2.createTrackbar('HL', 'image', 0, 255, nothing)
cv2.createTrackbar('SL', 'image', 202, 255, nothing)
cv2.createTrackbar('VL', 'image', 73, 255, nothing)
cv2.createTrackbar('HH', 'image', 2, 255, nothing)
cv2.createTrackbar('SH', 'image', 255, 255, nothing)
cv2.createTrackbar('VH', 'image', 216, 255, nothing)
cnt = 0
res1 = []
res2 = []
while True:
    ret, frame = cap.read()
    if frame is None:
        break

    #frame = cv2.resize(frame, (1300, 700))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hl = cv2.getTrackbarPos('HL', 'image')
    sl = cv2.getTrackbarPos('SL', 'image')
    vl = cv2.getTrackbarPos('VL', 'image')
    hh = cv2.getTrackbarPos('HH', 'image')
    sh = cv2.getTrackbarPos('SH', 'image')
    vh = cv2.getTrackbarPos('VH', 'image')

    low_red1 = np.array([0, 120, 70])
    high_red1 = np.array([10, 255, 255])
    """
    low_red2 = np.array([0, 120, 70])
    high_red2 = np.array([10, 255, 255])
    low_red3 = np.array([170, 120, 70])
    high_red3 = np.array([180, 255, 255])
    """
    low_red4 = np.array([hl, sl, vl])
    high_red4 = np.array([hh, sh, vh])

    mask1 = cv2.inRange(hsv, low_red1, high_red1)
    """
    mask2 = cv2.inRange(hsv, low_red2, high_red2)
    mask3 = cv2.inRange(hsv, low_red3, high_red3)
    """
    mask4 = cv2.inRange(hsv, low_red4, high_red4)
    #red = cv2.bitwise_and(frame, frame, mask=mask4)
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
                res1.append([cx, cy])
                cnt = cnt+1
                cv2.drawContours(frame, contours, i, (0, 255, 0), 2)
    #cv2.imshow("mask1", mask1)
    """
    cv2.imshow("mask2", mask2)
    cv2.imshow("mask3", mask3)
    """
    cv2.imshow("mask4", mask4)
#    cv2.imshow("mask", mask1 | mask2)
    cv2.imshow("red", thresh)
    cv2.imshow("frame", frame)
    t = 1
    if cv2.waitKey(t) == ord('q') or cv2.waitKey(t) == 27:
        break

cv2.destroyAllWindows()
print(res1)

cap = cv2.VideoCapture('ballmotionwhite.m4v')
cv2.namedWindow('image')
cv2.createTrackbar('HL', 'image', 0, 255, nothing)
cv2.createTrackbar('SL', 'image', 202, 255, nothing)
cv2.createTrackbar('VL', 'image', 73, 255, nothing)
cv2.createTrackbar('HH', 'image', 2, 255, nothing)
cv2.createTrackbar('SH', 'image', 255, 255, nothing)
cv2.createTrackbar('VH', 'image', 216, 255, nothing)
cnt = 0
while True:
    ret, frame = cap.read()
    if frame is None:
        break

    #frame = cv2.resize(frame, (1300, 700))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hl = cv2.getTrackbarPos('HL', 'image')
    sl = cv2.getTrackbarPos('SL', 'image')
    vl = cv2.getTrackbarPos('VL', 'image')
    hh = cv2.getTrackbarPos('HH', 'image')
    sh = cv2.getTrackbarPos('SH', 'image')
    vh = cv2.getTrackbarPos('VH', 'image')

    low_red1 = np.array([0, 120, 70])
    high_red1 = np.array([10, 255, 255])
    """
    low_red2 = np.array([0, 120, 70])
    high_red2 = np.array([10, 255, 255])
    low_red3 = np.array([170, 120, 70])
    high_red3 = np.array([180, 255, 255])
    """
    low_red4 = np.array([hl, sl, vl])
    high_red4 = np.array([hh, sh, vh])

    mask1 = cv2.inRange(hsv, low_red1, high_red1)
    """
    mask2 = cv2.inRange(hsv, low_red2, high_red2)
    mask3 = cv2.inRange(hsv, low_red3, high_red3)
    """
    mask4 = cv2.inRange(hsv, low_red4, high_red4)
    #red = cv2.bitwise_and(frame, frame, mask=mask4)
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
                res2.append([cx, cy])
                cnt = cnt+1
                cv2.drawContours(frame, contours, i, (0, 255, 0), 2)
    #cv2.imshow("mask1", mask1)
    """
    cv2.imshow("mask2", mask2)
    cv2.imshow("mask3", mask3)
    """
    cv2.imshow("mask4", mask4)
#    cv2.imshow("mask", mask1 | mask2)
    cv2.imshow("red", thresh)
    cv2.imshow("frame", frame)
    t = 1
    if cv2.waitKey(t) == ord('q') or cv2.waitKey(t) == 27:
        break

cv2.destroyAllWindows()
correct = 0
wrong = 0

for a, b in zip(res1, res2):
    if isclose(a[0], b[0]) and isclose(a[1], b[1]):
        correct +=1
    else:
        wrong +=1

print(correct, wrong)