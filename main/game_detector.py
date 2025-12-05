import cv2
import numpy as np

class VSDetector:
    def __init__(self, template_path, threshold=0.5):
        self.template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if self.template is None:
            raise FileNotFoundError("Could not find image")
        
        self.thresh = threshold
        self.h, self.w = self.template.shape[:2]
        
    
    def detect(self, frame):

        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # match template
        result = cv2.matchTemplate(gray_frame,self.template, cv2.TM_CCOEFF_NORMED)

        _, max_val, _, _= cv2.minMaxLoc(result)

        return max_val >= self.thresh
