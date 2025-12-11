import cv2
import numpy as np
from game.elixer_simulator import ElixerSimulator
from game.troop_tracker import TroopTracker
from game.troop_costs import TROOP_COSTS
from ultralytics import YOLO

model = YOLO("models/best.pt")
def start_model(sct, monitor):
    print("Starting YOLO model stream...")
    
    # Initialize trackers
    elixer = ElixerSimulator(start_elixer=6)
    tracker = TroopTracker(min_conf=0.9, required_frames=5, timeout=0.5)
    
    while True:
        img = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # Update elixir (regenerates over time)
        elixer.update()

        # Run YOLO
        results = model(frame, imgsz=640, verbose=False)
        
        # Convert YOLO results to detection format
        detections = []
        for box in results[0].boxes:
            detections.append({
                "class": model.names[int(box.cls)],
                "conf": float(box.conf)
            })
        
        deployments = tracker.process(detections)
        
        for troop in deployments:
            cost = TROOP_COSTS.get(troop, 0)
            elixer.spend(cost)
            print(f"Deployed {troop} (-{cost}) | Elixir: {elixer.get_elixer():.1f}")

        # Display
        annotated = results[0].plot()
        cv2.putText(annotated, f"Elixir: {elixer.get_elixer():.1f}", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("BlueStacks Frame", annotated)

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()