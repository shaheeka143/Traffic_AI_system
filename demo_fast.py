import cv2
import os
import numpy as np
from modules.speed import estimate_speed
from modules.lane import check_wrong_side
from utils import config

# DUMMY CLASSES for demonstration
class MockResults:
    def __init__(self, boxes, names):
        self.boxes = boxes
        self.names = names

class MockBox:
    def __init__(self, data, names):
        self.data = data
        self.xyxy = [data[:4]]
        self.conf = [data[4]]
        self.cls = [data[5]]
        self.names = names
    
    def tolist(self): return self.data.tolist()

class MockDetector:
    def __init__(self, model_path):
        self.names = {0: 'person', 3: 'motorcycle', 2: 'car'}
    
    def detect(self, frame):
        # We manually "detect" the shapes from create_demo_video.py
        # This is a hack to show the logic without waiting for real AI setup
        boxes = []
        # Find colors in the frame to identify our demo objects
        
        # --- VIOLATION 1: OVERSPEED (Light Blue rectangle) ---
        # Find the car (Yellow-ish box we made: [255, 255, 0])
        mask = cv2.inRange(frame, (250, 250, 0), (255, 255, 10))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if w > 20: 
                boxes.append(MockBox(np.array([x, y, x+w, y+h, 0.9, 2]), self.names))

        # --- VIOLATION 2: WRONG SIDE (Yellow-ish/Green rectangle) ---
        mask = cv2.inRange(frame, (0, 250, 250), (10, 255, 255))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if w > 20: 
                boxes.append(MockBox(np.array([x, y, x+w, y+h, 0.9, 2]), self.names))

        # --- VIOLATION 3: MULTI-RIDER ---
        # Motorcycle (Green box: [0, 255, 0])
        mask = cv2.inRange(frame, (0, 250, 0), (10, 255, 10))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if w > 20: 
                boxes.append(MockBox(np.array([x, y, x+w, y+h, 0.9, 3]), self.names))

        # Persons (Blue boxes: [255, 0, 0])
        mask = cv2.inRange(frame, (250, 0, 0), (255, 10, 10))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if w > 1: 
                boxes.append(MockBox(np.array([x, y, x+w, y+h, 0.9, 0]), self.names))
        
        # Wrap everything in a results object
        class ResultWrapper:
            def __init__(self, b, n): 
                self.boxes = b
                self.names = n
        
        return ResultWrapper(boxes, self.names)

class MockTracker:
    def __init__(self):
        self.history = {} # id: last_pos
    
    def update(self, results):
        tracks = []
        for i, box in enumerate(results.boxes):
            bx = box.data
            tracks.append((i, bx))
        return tracks

# MAIN SCRIPT
def run_fast_demo():
    print("-" * 60)
    print("FAST TRAFFIC VIOLATION DEMO (No local AI dependencies)")
    print("-" * 60)
    
    cap = cv2.VideoCapture("demo_violations.mp4")
    if not cap.isOpened():
        print("❌ Cannot open demo_violations.mp4. Please run create_demo_video.py first.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_video = cv2.VideoWriter("outputs/fast_demo.mp4", fourcc, fps, (width, height))
    
    detector = MockDetector(None)
    tracker = MockTracker()
    
    violation_count = 0
    frame_num = 0
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    colors = {'vehicle': (0, 255, 0), 'person': (255, 100, 100), 'violation': (0, 0, 255), 'text': (255, 255, 255), 'bg': (0, 0, 0)}

    while True:
        ret, frame = cap.read()
        if not ret: break
        
        frame_num += 1
        results = detector.detect(frame)
        tracks = tracker.update(results)
        
        # Filter detections for multi-rider count
        detections = []
        for box in results.boxes:
            x1, y1, x2, y2, conf, cls = box.data
            detections.append({'bbox': (int(x1), int(y1), int(x2), int(y2)), 'class': detector.names[int(cls)]})

        for track_id, box_data in tracks:
            x1, y1, x2, y2, conf, cls = box_data
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            class_name = detector.names[int(cls)]
            
            if class_name not in ["car", "motorcycle"]: continue
            
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            
            # 1. Speed
            speed = estimate_speed(track_id, cx, cy, fps)
            is_overspeed = speed > config.SPEED_LIMIT
            
            # 2. Lane
            is_wrong_side = check_wrong_side(track_id, cx, cy, width, height)
            
            # 3. Multi-Rider
            rider_count = 0
            is_multi_rider = False
            if class_name == "motorcycle":
                for d in detections:
                    if d['class'] == 'person':
                        px1, py1, px2, py2 = d['bbox']
                        if x1-10 <= (px1+px2)/2 <= x2+10: rider_count += 1
                if rider_count > config.MAX_RIDERS: is_multi_rider = True
            
            has_violation = is_overspeed or is_wrong_side or is_multi_rider
            color = colors['violation'] if has_violation else colors['vehicle']
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
            v_types = []
            if is_overspeed: v_types.append(f"OVERSPEED ({int(speed)}km/h)")
            if is_wrong_side: v_types.append("WRONG SIDE")
            if is_multi_rider: v_types.append(f"MULTI-RIDER ({rider_count})")
            
            label = f"ID:{track_id} {class_name}"
            if speed > 0: label += f" {int(speed)}km/h"
            cv2.putText(frame, label, (x1, y1-10), font, 0.6, color, 2)
            
            if has_violation:
                violation_count += 1
                v_label = "! " + " | ".join(v_types)
                cv2.putText(frame, v_label, (x1, y1-35), font, 0.7, colors['violation'], 2)

        # Overlay status
        cv2.rectangle(frame, (0, 0), (width, 80), colors['bg'], -1)
        cv2.putText(frame, f"TRAFFIC AI VIOLATION DEMO | Frame: {frame_num} | Violations: {violation_count}", (10, 30), font, 0.7, colors['text'], 2)
        cv2.putText(frame, f"Limit: {config.SPEED_LIMIT}km/h | Max Riders: {config.MAX_RIDERS}", (10, 60), font, 0.6, colors['text'], 1)
        
        out_video.write(frame)
        if frame_num % 50 == 0: print(f"  Processed {frame_num} frames...")

    cap.release()
    out_video.release()
    print(f"Demo complete! Results saved in outputs/fast_demo.mp4")

if __name__ == "__main__":
    run_fast_demo()
