class TroopTracker:
    def __init__(self, min_conf=0.9, required_frames=5):
        self.min_conf = min_conf
        self.required_frames = required_frames
        self.active = {}
    
    def process(self, detections):
        deployments = []

        for det in detections:
            det_name = det["class"]
            confidence = det["conf"]

            if confidence < self.min_conf:
                continue
            
            if det_name not in self.active:
                self.active[det_name] = {"frames:": 1}

            else:
                self.active[det_name]["frames"] += 1

                if self.active[det_name]["frames"] == self.required_frames:
                    deployments.append(det_name)
                    del self.active[det_name]
        return deployments



