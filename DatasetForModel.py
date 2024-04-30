'''
This code is used for taking the dataset for every gesture used for the functions defined by us.
Here for ebery function we made a directory of the same name

Procedure:
1. Run the code.
2. Camera is started
3. Observe and adjust your gesture with different hand and angles.
4. Press "s" key to save that frame.
5. Press "x" to stop the process altogether.
'''

#Libraries
import cv2 #for Computer Vision, the access to camera
from cvzone.HandTrackingModule import HandDetector #For detecting
import numpy as np
import math
import time

#Main
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=2)
offset = 20
imgSize = 400
count = 0

time.sleep(1)
#Instructions
print("\...You can show your hand sign and press \'s\' to save that image...")
print("You can stop the program using the key \'x\'")
#Data Storing File
folder = "C:\\Users\\YOGA\\PycharmProjects\\CursorMovementsThroughHandGestures\\.venv\\Data\\ScreenCapture"
#Start
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    #Cropping the image
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']
        #x1, y1, w1, h1 = hand['vbox']
        imgCrop = img[y-offset:y + h+offset, x-offset:x + w+offset]
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255  # Box
        #Centralizing the image
        asp_ratio = h/w
        if asp_ratio > 1: #Portrait mode
            i = imgSize/ h
            newWidth = math.ceil(i*w)
            ResizeImg = cv2.resize(imgCrop, (newWidth, imgSize))
            imgReShape = ResizeImg.shape
            WidthGap = math.ceil((imgSize-newWidth)/2)
            imgWhite[:, WidthGap:(newWidth+WidthGap)] = ResizeImg
        else: #Landscape mode
            i = imgSize / w
            newHeight = math.ceil(i * h)
            ResizeImg = cv2.resize(imgCrop, (imgSize, newHeight))
            imgReShape = ResizeImg.shape
            HeightGap = math.ceil((imgSize - newHeight) / 2)
            imgWhite[HeightGap:newHeight + HeightGap , :] = ResizeImg

        cv2.imshow("ImageWhites", imgWhite)
        cv2.imshow("ImageCrop", imgCrop)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    # Saving the images
    if key == ord("s"):
        if hands:  # Check if hands are detected
            count += 1
            cv2.imwrite(f'{folder}/Img_{time.time()}.jpg', imgWhite)
            print("Counter:", count)
        else:
            print("Error: No hand detected. Cannot save image.")

    if key == ord("x"):
        break
