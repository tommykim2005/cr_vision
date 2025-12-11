# game/troop_tracker.py

import time

class TroopTracker:
    def __init__(self, min_conf=0.9, required_frames=3, timeout=0.5):
        self.min_conf = min_conf
        self.required_frames = required_frames
        self.timeout = timeout  # seconds before we forget a troop
        self.active = {}
    
    def process(self, detections):
        deployments = []
        now = time.time()
        
        # Get current detected troop names
        detected_this_frame = set()
        
        for det in detections:
            det_name = det["class"]
            confidence = det["conf"]

            if confidence < self.min_conf:
                continue
            
            detected_this_frame.add(det_name)
            
            if det_name not in self.active:
                # First time seeing this troop
                self.active[det_name] = {
                    "frames": 1,
                    "last_seen": now
                }
            else:
                self.active[det_name]["frames"] += 1
                self.active[det_name]["last_seen"] = now

                if self.active[det_name]["frames"] == self.required_frames:
                    deployments.append(det_name)
        
        # Clean up old detections that timed out or were confirmed
        to_remove = []
        for name, data in self.active.items():
            if name in deployments:
                to_remove.append(name)
            elif now - data["last_seen"] > self.timeout:
                # Troop disappeared — probably a false positive
                to_remove.append(name)
        
        for name in to_remove:
            del self.active[name]
        
        return deployments