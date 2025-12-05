import subprocess
import numpy as np
import cv2

def get_frame():
    # capture the screen to raw bytes
    raw = subprocess.check_output(["adb", "exec-out", "screencap", "-p"])

    # convert to numpy array
    img_array = np.frombuffer(raw, dtype=np.uint8)
    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return frame

frame = get_frame()
cv2.imshow("BlueStacks Frame", frame)
cv2.waitKey(0)
