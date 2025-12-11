from ultralytics import YOLO


class TroopDetector:
    def __init__(self, model_path, img_size=640, conf_threshold=0.5):
        self.model = YOLO(model_path)
        self.img_size = img_size
        self.conf_threshold = conf_threshold
        self._last_results = None

    def detect(self, frame):
        """Returns a list of detections."""
        self._last_results = self.model(frame, imgsz=self.img_size, verbose=False)

        detections = []
        for box in self._last_results[0].boxes:
            conf = float(box.conf)
            if conf >= self.conf_threshold:
                detections.append({
                    "class": self.model.names[int(box.cls)],
                    "conf": conf,
                    "bbox": box.xyxy[0].tolist()  
                })

        return detections  
    def get_annotated_frame(self, frame=None):
        """Returns frame with YOLO annotations drawn."""
        if frame is not None:
            self._last_results = self.model(frame, imgsz=self.img_size, verbose=False)
        
        if self._last_results is None:
            raise ValueError("No results. Run detect() first.")
        
        return self._last_results[0].plot()  # Fixed: added ()