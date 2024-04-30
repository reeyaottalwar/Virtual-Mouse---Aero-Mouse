# Libraries needed
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import pyautogui
import screen_brightness_control as sbc
import numpy as np
import os
import datetime
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import math
import tensorflow
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import threading

# Initializing Variables
screenWidth, screenHeight = pyautogui.size()
offset = 20
imgSize = 800
indX, indY, indexX, indexY = 0, 0, 0, 0
pyautogui.FAILSAFE = False
action = 'Cursor'
minPerc = 95

#Cursor thread
def cur_move(hands):
    global indX, indY
    for hand in hands:
        landmarks = hand['lmList']
        for id, landmark in enumerate(landmarks):
            x = int(landmark[0])
            y = int(landmark[1])
            if id == 8:
                cv2.circle(img=frame, center=(x, y), radius=20, color=(255, 0, 0))
                # Smooth cursor movement
                indexX = x * screenWidth / fwidth
                indexY = y * screenHeight / fheight
                # Moving cursor smoothly
                indX = indexX
                indY = indexY
                print("Moving to : ", indX, indY)
                try:
                    pyautogui.moveTo(indX, indY)
                except pyautogui.FailSafeException:
                    pyautogui.moveTo(screenWidth / 2, screenHeight / 2)
    cv2.imshow("Aeromouse Cursor Tracking", frame)

def prediction_thread(hands):
    hand = hands[0]
    x, y, w, h = hand['bbox']
    imgCrop = frame[y - offset:y + h + offset, x - offset:x + w + offset]
    if imgCrop.size == 0:
        print("Error: Cropped image is empty.")
        return
    imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
    # Centralizing the image
    asp_ratio = h / w
    if asp_ratio >= 1:  # Landscape mode
        new_width = imgSize
        new_height = int(new_width / asp_ratio)
        resize_img = cv2.resize(imgCrop, (new_width, new_height))
        top_pad = (imgSize - new_height) // 2
        imgWhite[top_pad:top_pad + new_height, :] = resize_img
    else:  # Portrait mode
        new_height = imgSize
        new_width = int(new_height * asp_ratio)
        resize_img = cv2.resize(imgCrop, (new_width, new_height))
        left_pad = (imgSize - new_width) // 2
        imgWhite[:, left_pad:left_pad + new_width] = resize_img
    padding = 20
    imgWhite = cv2.copyMakeBorder(imgWhite, padding, padding, padding, padding, cv2.BORDER_CONSTANT,
                                  value=(255, 255, 255))
    prediction, confidence = classifier.getPrediction(imgWhite, draw=False)
    action = Labels[confidence]
    percPred = int(prediction[confidence] * 100)
    if percPred < minPerc:
        return
    else:
        pass
    cv2.imshow("ImageWhites", imgWhite)
    cv2.imshow("ImageCrop", imgCrop)
    # Features
    try:
        print(action)
        # Left Click
        if action == "LeftClick":
            pyautogui.click(indX, indY)
        # Right Click
        elif action == 'RightClick':
            pyautogui.rightClick(indX, indY)
        # Double Click
        elif action == 'DoubleClick':
            pyautogui.doubleClick(indX, indY)
        # Scroll Up
        elif action == 'ScrollUp':
            pyautogui.scroll(40)
        # Scroll Down
        elif action == 'ScrollDown':
            pyautogui.scroll(-40)
        # Screen Capture
        elif action == 'ScreenCapture':
            capture_screenshot()
        # Volume Up
        elif action == 'VolumeUp':
            change_volume(0.1)
        # Volume Down
        elif action == 'VolumeDown':
            change_volume(-0.1)
        # Brightness Up
        elif action == 'BrightnessUp':
            change_brightness(5)
        # Brightness Down
        elif action == 'BrightnessDown':
            change_brightness(-5)
        # Ignoring this case
        else:
            pass
    # Next case execution
    except:
        print("exception ")
def capture_screenshot():
    # Create a directory named "screenshots" if it doesn't exist
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    # Construct unique filename with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_name = f"screenshot_{timestamp}.png"
    screenshot_path = os.path.join("screenshots", screenshot_name)
    # Capture screenshot and save it with the unique filename
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    print(f"\nScreenshot saved successfully! \nPath: {screenshot_path}")
def change_volume(chanvol):
    # Get the default audio endpoint volume
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    # Get the current volume level
    newvol = volume.GetMasterVolumeLevelScalar() + chanvol
    # Ensure the new volume is within the valid range
    if 0.0 <= newvol <= 1.0:
        volume.SetMasterVolumeLevelScalar(newvol, None)
    else:
        if chanvol==0.01:
            volume.SetMasterVolumeLevelScalar(1.0, None)
        else:
            volume.SetMasterVolumeLevelScalar(0.0, None)
def change_brightness(change_amount):
    current_brightness = sbc.get_brightness()[0]
    print(current_brightness)
    new_brightness = current_brightness + change_amount
    # Ensure the new brightness is within the valid range (0 to 100)
    new_brightness = max(0, min(100, new_brightness))
    print("Changing brightness to:", new_brightness)
    sbc.set_brightness(new_brightness)

# Capturing Start
cap = cv2.VideoCapture(0)
pyautogui.FAILSAFE - False
detector = HandDetector(detectionCon=0.8, maxHands=2)
# Importing the trained model path
try:
    classifier = Classifier(
        "C:\\Users\\YOGA\\PycharmProjects\\CursorMovementsThroughHandGestures\\.venv\\Model\\keras_model.h5",
        "C:\\Users\\YOGA\\PycharmProjects\\CursorMovementsThroughHandGestures\\.venv\\Model\\labels.txt")
except:
    pass
# Labels for the functions used in the model
Labels = ['Cursor', 'LeftClick', 'RightClick', 'DoubleClick', 'ScreenCapture', 'ScrollUp', 'ScrollDown',
          'VolumeUp', 'VolumeDown', 'BrightnessUp', 'BrightnessDown']

# Code for the Welcome part Dialog box
def close_dialog():
    root.destroy()
root = tk.Tk()
root.withdraw()
messagebox.showinfo("AeroMouse", "AeroMouse has been enabled.")
okButton = tk.Button(root, text="OK", command=close_dialog)
okButton.pack()
root.destroy()

# Main
if __name__ == '__main__':
    while True:
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)
        hands, _ = detector.findHands(frame, flipType=False, draw=True)
        fheight, fwidth, _ = frame.shape
        if hands:
            cursor_thread = threading.Thread(target=cur_move, args=(hands,))
            cursor_thread.start()
            # Predictions on the live-video input data frame
            pred_thread = threading.Thread(target=prediction_thread, args=(hands,))
            pred_thread.start()
        # Display the frame
        cv2.imshow("AeroMouse", frame)
        # Ending the session with escape button
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # Escape key
            break
cap.release()
cv2.destroyAllWindows()
