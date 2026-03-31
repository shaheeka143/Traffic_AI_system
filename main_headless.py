import cv2
import os
import sys
from modules.detection import Detector
from modules.tracking import Tracker
from modules.helmet import check_helmet
from modules.blur import blur_face

from utils import config

# Try to import ANPR, but make it optional
try:
    from modules.anpr import read_plate
except ImportError as e:
    def read_plate(image):
        return "PLATE_UNAVAILABLE"

# Create output folders
os.makedirs("outputs/evidence", exist_ok=True)
os.makedirs("outputs/csv", exist_ok=True)
os.makedirs("outputs/logs", exist_ok=True)

# Validation checks
print("=" * 60)
print("Traffic Violation Detection System - Headless Mode")
print("=" * 60)

# Use VIDEO_PATH from config
VIDEO_PATH = config.VIDEO_PATH
if not os.path.exists(VIDEO_PATH):
    print(f"❌ ERROR: Video file not found: {VIDEO_PATH}")
    sys.exit(1)

# Load models
print("\nLoading models...")
detector = Detector(config.MODEL_PATH)
tracker = Tracker()
print("✓ Models loaded successfully")

# Open video
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print(f"❌ ERROR: Could not open video file")
    sys.exit(1)

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
print(f"✓ Video loaded: {total_frames} frames @ {fps} fps")
print("\nProcessing video (Headless)... This may take a minute.")

violation_count = 0
frame_num = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_num += 1
    if frame_num % 30 == 0:
        print(f"  Progress: {frame_num}/{total_frames} frames ({(frame_num/total_frames)*100:.1f}%)")

    # Detect objects
    results = detector.detect(frame)
    tracks = tracker.update(results)

    # Process tracked vehicles
    for track_id, det in tracks:
        x1, y1, x2, y2 = map(int, det[:4])

        # Check for helmet violations
        crop = frame[max(0,y1):min(frame.shape[0],y2), max(0,x1):min(frame.shape[1],x2)]
        if crop.size > 0:
            helmet_status = check_helmet(crop)

            if helmet_status == "no_helmet":
                violation_count += 1
                
                # Save evidence
                filename = f"outputs/evidence/headless_violation_{track_id}_f{frame_num}.jpg"
                cv2.imwrite(filename, frame)
                
                plate_text = read_plate(crop)
                print(f"  [VIOLATION] ID:{track_id} | Plate:{plate_text} | Frame:{frame_num}")

cap.release()

# Summary
print("\n" + "=" * 60)
print("Processing Complete!")
print("=" * 60)
print(f"Total violations detected: {violation_count}")
print(f"Images saved to: outputs/evidence/")
print("=" * 60)
