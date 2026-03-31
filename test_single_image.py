
import cv2
import os
import sys
from modules.detection import Detector
from utils import config

def test_image(image_path, conf=0.25):
    print("\n" + "=" * 60)
    print(f"🚦 TRAFFIC AI: SINGLE IMAGE TESTER (Multi-Rider Check)")
    print("=" * 60)

    if not os.path.exists(image_path):
        print(f"❌ Error: Image file not found: {image_path}")
        print("Please place your test image in the project folder.")
        return

    # Initialize AI Detector
    print(f"[1/3] Initializing YOLOv8 (Sensitivity: {conf})...")
    detector = Detector(config.MODEL_PATH)
    frame = cv2.imread(image_path)
    if frame is None:
        print("❌ Error: Could not read image.")
        return

    # 1. Run Detection
    print("[2/3] Running Object Detection...")
    results = detector.detect(frame, conf=conf)
    motorcycles = []
    persons = []

    if hasattr(results, 'boxes'):
        for box in results.boxes:
            b = list(map(int, box.xyxy[0]))
            cls = int(box.cls[0])
            name = results.names.get(cls, 'obj')
            if name == "motorcycle": motorcycles.append(b)
            if name == "person": persons.append(b)

    # 2. Match Riders to Motorcycles
    print("[3/3] Analyzing Rider Proximity & Violations...")
    print("-" * 60)
    print(f"🔍 DETECTED: {len(motorcycles)} Motorcycles | {len(persons)} Persons")
    print("-" * 60)
    
    for idx, m_box in enumerate(motorcycles, 1):
        mx1, my1, mx2, my2 = m_box
        rider_count = 0
        for p_box in persons:
            px1, py1, px2, py2 = p_box
            if mx1-30 <= (px1+px2)/2 <= mx2+30 and my1-100 <= (py1+py2)/2 <= my2: 
                rider_count += 1
                cv2.rectangle(frame, (px1, py1), (px2, py2), (255, 255, 0), 2)
        
        is_violation = (rider_count > config.MAX_RIDERS)
        color = (0, 0, 255) if is_violation else (0, 255, 0)
        
        cv2.rectangle(frame, (mx1, my1), (mx2, my2), color, 4)
        
        print(f"🏍️ MOTORCYCLE #{idx}: {rider_count} Riders")
        print(f"   Status: {'🔴 VIOLATION (Multi-Rider)' if is_violation else '🟢 OK'}")
        
        label = f"Riders:{rider_count}"
        if is_violation: label += " !! VIOLATION !!"
        cv2.putText(frame, label, (mx1, my1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    os.makedirs("outputs", exist_ok=True)
    cv2.imwrite("outputs/test_result_last.jpg", frame)
    print("-" * 60)
    print(f"✓ FINISHED. Result saved: outputs/test_result_last.jpg")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    img_to_test = sys.argv[1] if len(sys.argv) > 1 else "test_photo.jpg"
    conf_level = float(sys.argv[2]) if len(sys.argv) > 2 else 0.25
    test_image(img_to_test, conf=conf_level)


