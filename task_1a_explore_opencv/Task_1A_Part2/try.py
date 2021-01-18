import cv2
import numpy as np

cap = cv2.VideoCapture('ballmotion.m4v')

ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=10)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea)

    (x, y, w, h) = cv2.boundingRect(contour)
    cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
    m = cv2.moments(contour)
    cx = int(m['m10'] / m['m00'])
    cy = int(m['m01'] / m['m00'])
    cv2.putText(frame1, "Coordinates: " + str(cx) + " : " + str(cy), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

    cv2.imshow('video', frame1)

    if cv2.waitKey(40) == 27 or cv2.waitKey(40) == ord('q'):
        break

    frame1 = frame2
    ret, frame2 = cap.read()

cv2.destroyAllWindows()
cap.release()
