import streamlit as st
import cv2
import os
import sys
import numpy as np
from PIL import Image

# FIX: Add parent directory to sys.path so modules can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import project modules
from modules.detection import Detector
from modules.tracking import Tracker
from modules.pothole import PotholeDetector
from modules.speed import estimate_speed
from modules.lane import check_wrong_side
from modules.helmet import check_helmet
from modules.blur import blur_face
from modules.anpr import read_plate
from utils import config

st.set_page_config(page_title="Traffic AI System", layout="wide")

st.title("🚦 Traffic Violation Detection AI")
st.sidebar.header("Settings")

# Sidebar Configuration
status_placeholder = st.sidebar.empty()
violation_stats = st.sidebar.empty()

video_file = st.file_uploader("Upload a traffic video file", type=['mp4', 'avi', 'mov'])

@st.cache_resource
def load_models():
    # Get the absolute path to the project root
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    detector_path = os.path.join(root, config.MODEL_PATH)
    
    # Only try to load pothole model if enabled and path exists
    pothole_detector = None
    if getattr(config, 'ENABLE_POTHOLE', False) and hasattr(config, 'POTHOLE_MODEL_PATH'):
        pothole_path = os.path.join(root, config.POTHOLE_MODEL_PATH)
        if os.path.exists(pothole_path):
            pothole_detector = PotholeDetector(pothole_path)
    
    detector = Detector(detector_path)
    tracker = Tracker()
        
    return detector, tracker, pothole_detector

if video_file:
    # Save the upload temporarily
    temp_path = "temp_web_upload.mp4"
    with open(temp_path, "wb") as f:
        f.write(video_file.read())

    # Load resources
    detector, tracker, pothole_detector = load_models()
    
    cap = cv2.VideoCapture(temp_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    frame_window = st.image([])
    
    violation_count = 0
    frame_num = 0
    font = cv2.FONT_HERSHEY_DUPLEX
    
    colors = {
        'vehicle': (0, 255, 0),
        'violation': (255, 0, 0), # Red for BGR is (0,0,255), but Streamlit uses RGB
        'rider': (0, 255, 255)
    }

    status_placeholder.success("Processing Video...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_num += 1
        
        # 1. VEHICLE DETECTION
        raw_results = detector.detect(frame)
        all_detections = []
        
        if raw_results and hasattr(raw_results, 'boxes'):
            for box in raw_results.boxes:
                b = list(map(int, box.xyxy[0]))
                cls = int(box.cls[0])
                name = raw_results.names.get(cls, 'obj')
                all_detections.append({'bbox': b, 'class': name})

        # 2. TRACKING & VIOLATIONS
        tracks = tracker.update(raw_results)
        
        for track_id, box_tensor in tracks:
            tx1, ty1, tx2, ty2, tconf, tcls = box_tensor.tolist()
            tx1, ty1, tx2, ty2 = map(int, [tx1, ty1, tx2, ty2])
            
            class_name = raw_results.names.get(int(tcls), "vehicle")
            if class_name not in ["car", "motorcycle", "bus", "truck"]:
                continue

            cx, cy = (tx1 + tx2) / 2, (ty1 + ty2) / 2

            # --- VIOLATIONS ---
            speed = estimate_speed(track_id, cx, cy, fps)
            is_overspeed = speed > config.SPEED_LIMIT
            is_wrong_side = check_wrong_side(track_id, cx, cy, width, height)
            
            is_no_helmet = False
            rider_count = 0
            riders_on_this_bike = []
            
            if class_name == "motorcycle":
                for d in all_detections:
                    if d['class'] == 'person':
                        px1, py1, px2, py2 = d['bbox']
                        if tx1-20 <= (px1+px2)/2 <= tx2+20 and ty1-50 <= (py1+py2)/2 <= ty2:
                            rider_count += 1
                            riders_on_this_bike.append(d['bbox'])
                            
                            person_crop = frame[py1:py2, px1:px2]
                            if person_crop.size > 0:
                                if check_helmet(person_crop) == "no_helmet":
                                    is_no_helmet = True
            
            is_multi_rider = (class_name == "motorcycle" and rider_count > config.MAX_RIDERS)
            
            v_types = []
            if is_overspeed: v_types.append("Speed")
            if is_wrong_side: v_types.append("Lane")
            if is_multi_rider: v_types.append("Riders")
            if is_no_helmet: v_types.append("Helmet")
            
            has_v = len(v_types) > 0
            
            if has_v:
                violation_count += 1
                # Privacy Blur
                for d in all_detections:
                    if d['class'] == 'person':
                        bx1, by1, bx2, by2 = d['bbox']
                        if tx1 <= (bx1+bx2)/2 <= tx2 and ty1 <= (by1+by2)/2 <= ty2:
                            frame = blur_face(frame, bx1, by1, bx2-bx1, by2-by1)

            # DRAW
            color = (0, 0, 255) if has_v else (0, 255, 0) # BGR
            cv2.rectangle(frame, (tx1, ty1), (tx2, ty2), color, 2)
            
            # Label
            label = f"ID:{track_id} {class_name}"
            if has_v: label += f" ! {','.join(v_types)}"
            cv2.putText(frame, label, (tx1, ty1-10), font, 0.5, color, 2)

            # Draw Rider Boxes
            if class_name == "motorcycle" and rider_count > 0:
                for idx, rbbox in enumerate(riders_on_this_bike):
                    rx1, ry1, rx2, ry2 = rbbox
                    cv2.rectangle(frame, (rx1, ry1), (rx2, ry2), (255, 255, 0), 1)

        # Update Sidebar
        violation_stats.info(f"Frame: {frame_num} | Violations detected: {violation_count}")

        # Display (Convert BGR to RGB for Streamlit)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_window.image(frame_rgb, channels="RGB")

    status_placeholder.success("Processing Complete!")
    cap.release()