from ultralytics import YOLO


class TroopDetector:
    def __init__(self, model_path, img_size=640):
        self.model = YOLO(model_path)
        self.img_size = img_size
        self._last_results = None

    def detect(self, frame):
        """Returns a list of all detections (no confidence filter)."""
        self._last_results = self.model(frame, imgsz=self.img_size, verbose=False)

        detections = []
        for box in self._last_results[0].boxes:
            detections.append({
                "class": self.model.names[int(box.cls)],
                "conf": float(box.conf),
                "bbox": box.xyxy[0].tolist()
            })

        return detections

    @property
    def has_results(self):
        """Check if detect() has been called at least once."""
        return self._last_results is not None

    def get_annotated_frame(self):
        """Returns frame with YOLO annotations drawn from cached results."""
        if self._last_results is None:
            raise ValueError("No results. Run detect() first.")

        return self._last_results[0].plot()
