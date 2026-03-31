import cv2
import numpy as np
from modules.pothole import PotholeDetector

cap = cv2.VideoCapture('data/videos/sample.mp4')
# Pick frame 150 where it's clearer
cap.set(cv2.CAP_PROP_POS_FRAMES, 150)
ret, frame = cap.read()

if ret:
    pd = PotholeDetector()
    potholes = pd.detect(frame)
    
    print(f"Detected {len(potholes)} potholes.")
    
    for p in potholes:
        x1, y1, x2, y2 = p['bbox']
        # Massive red/orange highlight
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 100, 255), 15)
        cv2.putText(frame, " POTHOLE SEEN ", (x1, y1-30), cv2.FONT_HERSHEY_DUPLEX, 2.5, (0, 100, 255), 8)
    
    cv2.imwrite('outputs/pothole_highlight_test.jpg', frame)
    print("Saved outputs/pothole_highlight_test.jpg")
else:
    print("Could not read frame.")
cap.release()
