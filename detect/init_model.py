import mss
import numpy as np
import cv2
from ultralytics import YOLO
import time

from detect.vs_detector import VSDetector
from detect.window_detector import find_window
from game.game_loop import start_model


# Load model
model = YOLO("models/best.pt")


def init_program():

    # VS detector
    game_detector = VSDetector("images/vs_icon.png", threshold=0.5)
    vs_triggered = False

    sct = mss.mss()

    monitor = find_window("BlueStacks Air")
    print(monitor)

    print("Waiting for VS screen...")

    while True:
        # capture frame
        img = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        # detect VS only once
        if game_detector.detect(frame) and not vs_triggered:
            print("GAMESTART")
            vs_triggered = True
            time.sleep(0.5)  # small delay so VS passes
            start_model(sct, monitor)
            break


