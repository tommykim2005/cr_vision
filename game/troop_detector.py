from ultralytics import YOLO

class TroopDetector:
    def __init__(self, model_path, img_size= 640, conf_threshhold=0.5):
        self.model = YOLO("models/best.pt")
        self.img_size = img_size
        self.conf_threshhold = conf_threshhold

    def detect(self, frame):
        # returns a list of detections
        results = self.model(frame, imgsz=self.img_size, verbose=False)

        detections = []
        for box in results[0].boxes:
            conf = float(box.conf)
            if conf >= self.conf_threshhold:
                detections.append({
                    "class": self.model.names[int(box.cls)],
                    "conf": conf,
                    "bbox": box.xyxy[0].toList()
                })

            return detections
        
    def get_annotated_frame(self, frame):
        results = self.model(frame, imgsz = self.img_size, verbose = False)
        return results[0].plot
