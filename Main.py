import cv2 as cv
import numpy as np
import pickle
import cvzone

# ? Video feed
cap = cv.VideoCapture('parking.mp4')
width, height = 65, 30

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)


def checkParkingSpace():
    for pos in posList:
        x, y = pos
        # imgCrop = img[y:y+height, x:x+width]
        # cv.imshow(str(x*y), imgCrop)


while True:
    if cap.get(cv.CAP_PROP_POS_FRAMES) == cap.get(cv.CAP_PROP_FRAME_COUNT):
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()

    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (3, 3), 1)
    # ? binary image
    imgTreshold = cv.adaptiveThreshold(
        imgBlur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 16)

    checkParkingSpace()

    for pos in posList:
        cv.rectangle(img, pos, (pos[0]+width, pos[1]+height), (255, 0, 255), 2)

    cv.imshow("imgBlur", imgBlur)
    cv.imshow("image", img)
    cv.waitKey(1)
