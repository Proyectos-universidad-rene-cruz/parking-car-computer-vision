import cv2
import pickle

# ? size values
width, height = 65, 30

try: 
    #? If CarParkPos exists -> edit the file with the previous rectangles added
    with open('CarParkPos', 'rb') as f:
        positionList = pickle.load(f)
except:
    #? There does not exist any CarParkPos -> create a new list 
    positionList = [] 

#? detect the clicks and inserts a rectangle 
def mouseclick(events, x, y, flags, params):
    #? leftbutton pressed -> inserts a new rectangle in the position (x, y)
    if events == cv2.EVENT_LBUTTONDOWN:
        positionList.append((x, y))
    #? right button pressed -> removes the selected rectangle in the position
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(positionList):
            x1, y1 = pos
            if x1 < x < x1+width and y1 < y < y1+height:
                positionList.pop(i)
    #? writes the rectangles in the files named "CarParkPos"
    with open('CarParkPos', 'wb') as f:
        pickle.dump(positionList, f)
    

#? Base image
while True:
    #? reference image -> it must be the same view of the video
    img = cv2.imread('parking_3.png')
    #? print purple rectangles in the selected places
    for pos in positionList:
        cv2.rectangle(
            img, pos, (pos[0]+width, pos[1]+height), (255, 0, 255), 2)
    # ? Diplsay the image
    cv2.imshow("image", img)
    #? mouse function detection
    cv2.setMouseCallback("image", mouseclick)
    cv2.waitKey(1)
