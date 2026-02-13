import mss
import numpy as np
import cv2

class ScreenCapture:
    def __init__(self, monitor):
        # monitor dictionary with left, top, width, height
        self.sct = mss.mss()
        self.monitor = monitor

    def grab(self):
        # returns BGR frame for YOLO
        img = np.array(self.sct.grab(self.monitor))
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)