import cv2
import numpy as np


class VSDetector:
    """Detects VS screen using template matching with multi-scale support."""
    
    def __init__(self, template_path, threshold=0.75):
        self.template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if self.template is None:
            raise FileNotFoundError(f"Could not find template: {template_path}")
        
        self.threshold = threshold
        self.scales = [0.5, 0.75, 1.0, 1.25, 1.5]
    
    def detect(self, frame):
        """Returns True if VS screen is detected."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        for scale in self.scales:
            resized = cv2.resize(self.template, None, fx=scale, fy=scale)
            
            # Skip if template is larger than frame
            if resized.shape[0] > gray.shape[0] or resized.shape[1] > gray.shape[1]:
                continue
            
            result = cv2.matchTemplate(gray, resized, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            
            if max_val >= self.threshold:
                return True
        
        return False