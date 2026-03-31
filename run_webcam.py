import cv2
import os
import sys
import time
from modules.detection import Detector
from modules.tracking import Tracker
from modules.helmet import check_helmet
from modules.blur import blur_face
from modules.anpr import read_plate
from modules.speed import estimate_speed
from modules.lane import check_wrong_side
from utils import config

def run_webcam():
    print("\n" + "="*70)
    print("🚦 WEBCAM - REAL-TIME TRAFFIC MONITORING")
    print("="*70 + "\n")

    # Initialize Modules
    print("Initializing AI models...")
    detector = Detector(config.MODEL_PATH)
    tracker = Tracker()
    print("✓ Models loaded.")

    # Open Webcam (0 is default camera)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ ERROR: Could not open webcam.")
        return

    # Set resolution for better performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    window_name = "WEBCAM AI - Real-Time Analysis"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1280, 720)

    violation_count = 0
    frame_num = 0
    font = cv2.FONT_HERSHEY_DUPLEX
    
    colors = {
        'vehicle': (0, 255, 0),      # Green
        'violation': (0, 0, 255),    # Red
        'text': (255, 255, 255)
    }

    print("✓ Webcam started. Press 'ESC' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret: 
            print("❌ Failed to grab frame.")
            break
            
        frame_num += 1

        # 1. AI DETECTION
        raw_results = detector.detect(frame)
        all_detections = []
        if raw_results and hasattr(raw_results, 'boxes'):
            for box in raw_results.boxes:
                b = list(map(int, box.xyxy[0]))
                cls = int(box.cls[0])
                name = raw_results.names.get(cls, 'obj')
                all_detections.append({'bbox': b, 'class': name})

        # 2. TRACKING & VIOLATION ANALYSIS
        tracks = tracker.update(raw_results)

        for track_id, box_tensor in tracks:
            tx1, ty1, tx2, ty2, tconf, tcls = box_tensor.tolist()
            tx1, ty1, tx2, ty2 = map(int, [tx1, ty1, tx2, ty2])
            tx1, ty1, tx2, ty2 = max(0, tx1), max(0, ty1), min(width, tx2), min(height, ty2)
            
            class_name = raw_results.names.get(int(tcls), "vehicle")
            if class_name not in ["car", "motorcycle", "bus", "truck", "person"]:
                continue

            cx, cy = (tx1 + tx2) / 2, (ty1 + ty2) / 2

            # A. Violation Checks
            is_no_helmet = False
            rider_count = 0
            if class_name == "motorcycle":
                for d in all_detections:
                    if d['class'] == 'person':
                        px1, py1, px2, py2 = d['bbox']
                        if tx1-20 <= (px1+px2)/2 <= tx2+20:
                            rider_count += 1
                            h_crop = frame[py1:py2, px1:px2]
                            if h_crop.size > 0 and check_helmet(h_crop) == "no_helmet":
                                is_no_helmet = True
            
            is_multi_rider = (class_name == "motorcycle" and rider_count > config.MAX_RIDERS)
            
            # Composite Violation Check
            v_types = []
            if is_multi_rider: v_types.append("MultiRider")
            if is_no_helmet: v_types.append("NoHelmet")
            
            has_v = len(v_types) > 0
            if has_v:
                violation_count += 1
                # Blur Face for privacy
                for d in all_detections:
                    if d['class'] == 'person':
                        bx1, by1, bx2, by2 = d['bbox']
                        if tx1 <= (bx1+bx2)/2 <= tx2:
                            frame = blur_face(frame, bx1, by1, bx2-bx1, (by2-by1)//3)

            # DRAWING LOGIC
            color = colors['violation'] if has_v else colors['vehicle']
            cv2.rectangle(frame, (tx1, ty1), (tx2, ty2), color, 2)
            
            label = f"ID:{track_id} {class_name}"
            if has_v: label += f" !{v_types[0]}"
            cv2.putText(frame, label, (tx1, ty1-10), font, 0.5, color, 2)

        # Status Overlay
        cv2.rectangle(frame, (0, 0), (width, 85), (0,0,0), -1)
        cv2.putText(frame, f"WEBCAM MONITOR | Frame: {frame_num} | Total Violations: {violation_count}", 
                    (15, 30), font, 0.8, (255,255,255), 2)
        cv2.putText(frame, f"Max Riders: {config.MAX_RIDERS} | ANPR & FACE-BLUR: ACTIVE", 
                    (15, 65), font, 0.6, (0, 255, 255), 1)

        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == 27: break # ESC to quit

    cap.release()
    cv2.destroyAllWindows()
    print(f"\n🎬 WEBCAM MONITORING STOPPED. Total Violations: {violation_count}")

if __name__ == "__main__":
    run_webcam()
