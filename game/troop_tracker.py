import time


class TroopTracker:
    """Smooths detections over multiple frames to confirm deployments."""
    
    def __init__(self, min_conf=0.6, required_frames=3, max_gap=2):
        self.min_conf = min_conf
        self.required_frames = required_frames
        self.max_gap = max_gap  # Max frames a troop can be missing before reset
        self.active = {}
        self.frame_count = 0
    
    def process(self, detections):
        """
        Process detections and return confirmed deployments.
        """
        deployments = []
        self.frame_count += 1
        seen_this_frame = set()
        
        for det in detections:
            if det["conf"] < self.min_conf:
                continue
            
            troop_name = det["class"]
            seen_this_frame.add(troop_name)
            
            if troop_name not in self.active:
                self.active[troop_name] = {"frames": 1, "last_frame": self.frame_count, "confirmed": False}
            else:
                self.active[troop_name]["frames"] += 1
                self.active[troop_name]["last_frame"] = self.frame_count
                
                if self.active[troop_name]["frames"] >= self.required_frames and not self.active[troop_name]["confirmed"]:
                    self.active[troop_name]["confirmed"] = True
                    deployments.append(troop_name)
        
        # Cleanup: remove if not seen for max_gap frames
        to_remove = []
        for name, data in self.active.items():
            if self.frame_count - data["last_frame"] > self.max_gap:
                to_remove.append(name)
        
        for name in to_remove:
            del self.active[name]
        
        return deployments