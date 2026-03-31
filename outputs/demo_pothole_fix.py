import cv2
import numpy as np
from modules.pothole import PotholeDetector
from modules.detection import Detector

# Paths
VIDEO_PATH = 'data/videos/sample.mp4'
MODEL_PATH = 'data/models/yolo_helmet.pt'

cap = cv2.VideoCapture(VIDEO_PATH)
cap.set(cv2.CAP_PROP_POS_FRAMES, 50) # Use frame 50
ret, frame = cap.read()

if ret:
    # 1. Detect vehicles for masking
    detector = Detector(MODEL_PATH)
    raw_results = detector.detect(frame)
    vehicle_boxes = []
    if raw_results and raw_results.boxes:
        for box in raw_results.boxes:
            b = list(map(int, box.xyxy[0]))
            cls = int(box.cls[0])
            name = raw_results.names.get(cls, 'obj')
            if name in ["car", "motorcycle", "bus", "truck"]:
                vehicle_boxes.append(b)
                # Draw vehicle boxes in green for context
                cv2.rectangle(frame, (b[0], b[1]), (b[2], b[3]), (0, 255, 0), 2)

    # 2. Detect potholes using the updated MASKED logic
    pd = PotholeDetector()
    potholes = pd.detect(frame, vehicle_boxes=vehicle_boxes)
    
    print(f"Detected {len(potholes)} potholes on road.")
    
    for p in potholes:
        x1, y1, x2, y2 = p['bbox']
        # Massive highlight strictly for the road
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 140, 255), 6)
        # Background for label
        cv2.rectangle(frame, (x1, y1-35), (x1+200, y1), (0, 140, 255), -1)
        cv2.putText(frame, " POTHOLE ON ROAD ", (x1, y1-10), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)
    
    cv2.imwrite('outputs/pothole_fixed_road_only.jpg', frame)
    print("Saved outputs/pothole_fixed_road_only.jpg")
else:
    print("Could not read frame.")
cap.release()
