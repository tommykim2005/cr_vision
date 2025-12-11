import time


class TroopTracker:
    """
    Smooths detections over multiple frames to confirm deployments.
    Uses position to distinguish multiple troops of same type.
    """
    
    def __init__(self, min_conf=0.9, required_frames=3, timeout=0.5):
        self.min_conf = min_conf
        self.required_frames = required_frames
        self.timeout = timeout
        self.active = {}
    
    def _make_key(self, troop_name, bbox, grid_size=50):
        """Create unique key based on troop type and position."""
        cx = (bbox[0] + bbox[2]) / 2
        cy = (bbox[1] + bbox[3]) / 2
        return (troop_name, int(cx // grid_size), int(cy // grid_size))
    
    def process(self, detections):
        """
        Process detections and return confirmed deployments.
        
        Args:
            detections: List of {"class": str, "conf": float, "bbox": [x1,y1,x2,y2]}
        
        Returns:
            List of troop names that were confirmed this frame
        """
        deployments = []
        now = time.time()
        
        for det in detections:
            if det["conf"] < self.min_conf:
                continue
            
            key = self._make_key(det["class"], det["bbox"])
            
            if key not in self.active:
                self.active[key] = {"frames": 1, "last_seen": now}
            else:
                self.active[key]["frames"] += 1
                self.active[key]["last_seen"] = now
                
                if self.active[key]["frames"] == self.required_frames:
                    deployments.append(det["class"])
        
        # Cleanup: remove confirmed or timed-out entries
        to_remove = []
        for key, data in self.active.items():
            if key[0] in deployments and data["frames"] >= self.required_frames:
                to_remove.append(key)
            elif now - data["last_seen"] > self.timeout:
                to_remove.append(key)
        
        for key in to_remove:
            del self.active[key]
        
        return deployments