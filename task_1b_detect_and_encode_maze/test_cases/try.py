import cv2
import numpy as np

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


img = cv2.imread('maze00.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('1', gray)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
cv2.imshow('2', gray)
edged = cv2.Canny(gray, 75, 200)
cv2.imshow('3', edged)
_, thresh = cv2.threshold(edged, 127, 255, cv2.THRESH_BINARY)
cv2.imshow('4', thresh)
cnts, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
#cv2.drawContours(img, cnts, -1, (0, 255, 0), 2)
#cv2.imshow('5', img)
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    if len(approx) == 4:
        screenCnt = approx
        break
cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 2)
cv2.imshow("Outline", img)
print(img.shape)
'''
warped = four_point_transform(img, screenCnt.reshape(4, 2))
# cv2.imshow('final', warped)
warped_img = warped

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

maze_array = l
'''

cv2.waitKey(0)
cv2.destroyAllWindows()

