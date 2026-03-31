import cv2
import os
import sys
import numpy as np
from modules.detection import Detector
from modules.tracking import Tracker
from modules.pothole import PotholeDetector
from modules.speed import estimate_speed
from modules.lane import check_wrong_side
from modules.helmet import check_helmet
from modules.blur import blur_face
from modules.anpr import read_plate

from utils import config

# Create output folders
os.makedirs("outputs", exist_ok=True)
os.makedirs("outputs/evidence", exist_ok=True)
os.makedirs("outputs/csv", exist_ok=True)

print("=" * 60)
print("TRAFFIC AI SYSTEM - FULL VIOLATION & ANPR DETECTION")
print("=" * 60)

if not os.path.exists(config.VIDEO_PATH):
    print(f"❌ ERROR: Video file not found: {config.VIDEO_PATH}")
    sys.exit(1)

cap = cv2.VideoCapture(config.VIDEO_PATH)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Model initialization
detector = Detector(config.MODEL_PATH)
tracker = Tracker()
pothole_detector = PotholeDetector(config.POTHOLE_MODEL_PATH)

# Output Setup
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video_path = "outputs/violation_output.mp4"
out_video = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

violation_count = 0
frame_num = 0

font = cv2.FONT_HERSHEY_DUPLEX
colors = {
    'vehicle': (0, 255, 0),      # Green
    'pothole': (0, 140, 255),    # Brighter Orange
    'violation': (0, 0, 255),    # Red
}

print(f"✓ Starting full processing: {config.VIDEO_PATH}")

while True:
    ret, frame = cap.read()
    if not ret: break
    frame_num += 1

    # 1. VEHICLE DETECTION
    raw_results = detector.detect(frame)
    all_detections = []
    vehicle_boxes = []
    
    if raw_results and hasattr(raw_results, 'boxes'):
        for box in raw_results.boxes:
            b = list(map(int, box.xyxy[0]))
            cls = int(box.cls[0])
            name = raw_results.names.get(cls, 'obj')
            all_detections.append({'bbox': b, 'class': name})
            if name in ["car", "motorcycle", "bus", "truck"]:
                vehicle_boxes.append(b)

    # 2. POTHOLE DETECTION
    if config.ENABLE_POTHOLE:
        potholes = pothole_detector.detect(frame, vehicle_boxes=vehicle_boxes)
        for p in potholes:
            px1, py1, px2, py2 = p['bbox']
            cv2.rectangle(frame, (px1, py1), (px2, py2), colors['pothole'], 3)
            cv2.putText(frame, " POTHOLE", (px1, py1-5), font, 0.5, (255, 255, 255), 1)

    # 3. TRACKING & VIOLATIONS
    tracks = tracker.update(raw_results)
    for track_id, box_tensor in tracks:
        tx1, ty1, tx2, ty2, tconf, tcls = box_tensor.tolist()
        tx1, ty1, tx2, ty2 = map(int, [tx1, ty1, tx2, ty2])
        # Ensure boxes are within frame
        tx1, ty1 = max(0, tx1), max(0, ty1)
        tx2, ty2 = min(width, tx2), min(height, ty2)
        
        class_name = raw_results.names.get(int(tcls), "vehicle")
        if class_name not in ["car", "motorcycle", "bus", "truck"]:
            continue

        cx, cy = (tx1 + tx2) / 2, (ty1 + ty2) / 2

        # --- A. SPEED & LANE ---
        speed = estimate_speed(track_id, cx, cy, fps)
        is_overspeed = speed > config.SPEED_LIMIT
        is_wrong_side = check_wrong_side(track_id, cx, cy, width, height)
        
        # --- B. HELMET & MULTI-RIDER ---
        is_no_helmet = False
        rider_count = 0
        riders_on_this_bike = []
        
        if class_name == "motorcycle":
            # Find persons near/on this motorcycle
            for d in all_detections:
                if d['class'] == 'person':
                    px1, py1, px2, py2 = d['bbox']
                    # Check if person is on this motorcycle (horizontal overlap + vertical proximity)
                    if tx1-20 <= (px1+px2)/2 <= tx2+20 and ty1-50 <= (py1+py2)/2 <= ty2:
                        rider_count += 1
                        riders_on_this_bike.append(d['bbox'])
                        
                        # HELMET CHECK: Focus on the person's head region
                        person_crop = frame[py1:py2, px1:px2]
                        if person_crop.size > 0:
                            helmet_status = check_helmet(person_crop)
                            if helmet_status == "no_helmet":
                                is_no_helmet = True # Any rider without helmet is a violation
        
        is_multi_rider = (class_name == "motorcycle" and rider_count > config.MAX_RIDERS)
        
        # --- C. ANPR & BLURRING ---
        v_types = []
        if is_overspeed: v_types.append("Speeding")
        if is_wrong_side: v_types.append("WrongSide")
        if is_multi_rider: v_types.append("MultiRider")
        if is_no_helmet: v_types.append("NoHelmet")
        
        has_v = len(v_types) > 0
        if has_v:
            violation_count += 1
            v_label = "-".join(v_types)
            
            # --- PLATE EXTRACTION ---
            plate_crop = frame[ty1:ty2, tx1:tx2] 
            plate_num = read_plate(plate_crop)
            
            # --- PRIVACY PRESERVATION (Face Blur) ---
            for d in all_detections:
                if d['class'] == 'person':
                    bx1, by1, bx2, by2 = d['bbox']
                    if tx1 <= (bx1+bx2)/2 <= tx2 and ty1 <= (by1+by2)/2 <= ty2:
                        blur_y2 = by1 + int((by2-by1)*0.3)
                        frame = blur_face(frame, bx1, by1, bx2-bx1, blur_y2-by1)

            # SAVE EVIDENCE
            safe_plate = plate_num.replace(" ", "")
            evidence_path = f"outputs/evidence/violation_{track_id}_{v_label}_{safe_plate}.jpg"
            if not os.path.exists(evidence_path):
                # Save a slightly larger crop to see surroundings
                cv2.imwrite(evidence_path, frame[max(0, ty1-80):min(height, ty2+80), max(0, tx1-80):min(width, tx2+80)])

        # DRAW INDIVIDUAL RIDER BOXES (Helps identify multi-rider even when blurred)
        if class_name == "motorcycle" and rider_count > 0:
            for idx, rbbox in enumerate(riders_on_this_bike):
                rx1, ry1, rx2, ry2 = rbbox
                # Draw a thinner, dotted-style box (or just a different color) for each rider
                cv2.rectangle(frame, (rx1, ry1), (rx2, ry2), (255, 255, 0), 1)
                cv2.putText(frame, f"R{idx+1}", (rx1, ry1-5), font, 0.4, (255, 255, 0), 1)

        # DRAW MAIN VEHICLE BOX
        color = colors['violation'] if has_v else colors['vehicle']
        cv2.rectangle(frame, (tx1, ty1), (tx2, ty2), color, 2)
        
        # LABEL: Show ALL violations found
        label = f"ID:{track_id} {class_name}"
        if rider_count > 0: label += f" ({rider_count} riders)"
        
        if has_v:
            label += " | " + " ".join([f"!{v}" for v in v_types])
            
        cv2.putText(frame, label, (tx1, ty1-10), font, 0.5, color, 1)

    # Status Overlay
    cv2.rectangle(frame, (0, 0), (width, 80), (0,0,0), -1)
    cv2.putText(frame, f"TRAFFIC AI v2.0 | Frame: {frame_num}/{total_frames} | Violations: {violation_count}", 
                (10, 30), font, 0.7, (255,255,255), 2)
    cv2.putText(frame, f"Limit: {config.SPEED_LIMIT}km/h | Max Riders: {config.MAX_RIDERS} | ANPR: ACTIVE", 
                (10, 65), font, 0.6, (0, 255, 255), 1)

    out_video.write(frame)
    if frame_num % 100 == 0: print(f"  Processed {frame_num}/{total_frames} frames...")

cap.release()
out_video.release()
print(f"\nALL OBJECTIVES COMPLETE. Output saved: outputs/violation_output.mp4")