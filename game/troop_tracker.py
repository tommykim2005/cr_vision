class TroopTracker:
    """Smooths detections over multiple frames to confirm deployments."""

    GRID_COLS = 8
    GRID_ROWS = 12

    def __init__(self, min_conf=0.6, required_frames=3, max_gap=2,
                 frame_width=1, frame_height=1):
        self.min_conf = min_conf
        self.required_frames = required_frames
        self.max_gap = max_gap
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.active = {}
        self.frame_count = 0

    def _bbox_to_grid(self, bbox):
        """Map bbox center to an (col, row) grid cell."""
        cx = (bbox[0] + bbox[2]) / 2
        cy = (bbox[1] + bbox[3]) / 2
        col = min(int(cx / self.frame_width * self.GRID_COLS), self.GRID_COLS - 1)
        row = min(int(cy / self.frame_height * self.GRID_ROWS), self.GRID_ROWS - 1)
        return col, row

    def process(self, detections):
        """Process detections and return confirmed deployments."""
        deployments = []
        self.frame_count += 1
        seen_this_frame = set()

        for det in detections:
            if det["conf"] < self.min_conf:
                continue

            troop_name = det["class"]
            col, row = self._bbox_to_grid(det["bbox"])
            key = (troop_name, col, row)
            seen_this_frame.add(key)

            if key not in self.active:
                self.active[key] = {"frames": 1, "last_frame": self.frame_count, "confirmed": False}
            else:
                self.active[key]["frames"] += 1
                self.active[key]["last_frame"] = self.frame_count

                if self.active[key]["frames"] >= self.required_frames and not self.active[key]["confirmed"]:
                    self.active[key]["confirmed"] = True
                    deployments.append(troop_name)

        # Cleanup: remove if not seen for max_gap frames
        to_remove = [k for k, data in self.active.items()
                     if self.frame_count - data["last_frame"] > self.max_gap]
        for k in to_remove:
            del self.active[k]

        return deployments

    def reset(self):
        """Clear all tracking state."""
        self.active.clear()
        self.frame_count = 0
