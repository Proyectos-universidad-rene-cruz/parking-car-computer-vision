import cv2 as cv
import numpy as np
import pickle
import cvzone

# ? Video feed
capture = cv.VideoCapture('parking.mp4')
#? size values
width, height = 65, 30

#? call previous file created with 'ParkingSpacePicker.py'
with open('CarParkPos', 'rb') as f:
    positionList = pickle.load(f)

#? print green or red rectangles to show free spaces
def checkParkingSpace(imgPro):
    #? iterate the selected rectangles by position
    for position in positionList:
        x, y = position
        #? separate rectangles by creating a new and only file
        imgCrop = imgPro[y:y+height, x:x+width]
        #? count -> binary count for the free space separation
        count = cv.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count), (x, y+height-10), scale=0.8, thickness=1, offset=0)
        #? categorize empty and non-empty space
        if count < 430:
            color = (0,255,0) #? green
        else:
            color = (0, 0, 255) #? red
        #? show rectangle in the selected color
        cv.rectangle(img, position, (position[0]+width, position[1]+height), color , 2)

#? Base video
while True:
    #? count frames
    if capture.get(cv.CAP_PROP_POS_FRAMES) == capture.get(cv.CAP_PROP_FRAME_COUNT):
        capture.set(cv.CAP_PROP_POS_FRAMES, 0)
    #? read video
    success, img = capture.read()
    #? process video
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) #? grayscale
    imgBlur = cv.GaussianBlur(imgGray, (3, 3), 1) #? create a gaussian matrix for process
    # ? binary image
    imgTreshold = cv.adaptiveThreshold(
        imgBlur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 20)
    imgMedian = cv.medianBlur(imgTreshold, 5)
    kernel = np.ones((9, 9), np.uint8) #? matrix of ones to process
    imgDilate = cv.dilate(imgMedian, kernel, iterations=1)
    #? function at 16
    checkParkingSpace(imgDilate)
    cv.imshow("image", img)
    cv.waitKey(1)
