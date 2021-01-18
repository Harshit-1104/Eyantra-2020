import cv2
import numpy as np

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


############################################################
##############	ADD YOUR CODE HERE	##############

img = cv2.imread('./Test_Images/Test1.png')
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

print (shapes)

