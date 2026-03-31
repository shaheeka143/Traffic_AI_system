import cv2
import numpy as np

class PotholeDetector:
    def __init__(self, model_path=None):
        self.model = None
        # In a real scenario, we'd load a YOLO model here.
        # For this demo, we use an improved heuristic that avoids vehicles.

    def detect(self, frame, vehicle_boxes=[]):
        """
        Detects potholes while ignoring vehicles.
        """
        h, w = frame.shape[:2]
        # 1. Create a mask of the road area (typically bottom triangle/trapezoid)
        mask = np.zeros((h, w), dtype=np.uint8)
        # Trapezoid for the road in the center-bottom
        pts = np.array([[int(w*0.1), h], [int(w*0.4), int(h*0.6)], 
                        [int(w*0.6), int(h*0.6)], [int(w*0.9), h]])
        cv2.fillPoly(mask, [pts], 255)

        # 2. Black out all detected vehicles from the mask
        for box in vehicle_boxes:
            x1, y1, x2, y2 = box
            # Increase box slightly to ensure we don't catch edges
            cv2.rectangle(mask, (x1-5, y1-5), (x2+5, y2+5), 0, -1)

        # 3. Process Only Road Surface
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        road_only = cv2.bitwise_and(gray, gray, mask=mask)
        
        # Look for small, dark, circular-ish regions (potholes)
        blur = cv2.GaussianBlur(road_only, (11, 11), 0)
        
        # Find local minima or use thresholding on the road texture
        # Using a very low threshold to find "cracks"
        _, thresh = cv2.threshold(blur, 40, 255, cv2.THRESH_BINARY_INV)
        
        # Mask the result again to be sure
        thresh = cv2.bitwise_and(thresh, mask)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        results = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            # Potholes in video are usually small-medium
            if 1000 < area < 15000:
                x, y, rw, rh = cv2.boundingRect(cnt)
                # Potholes are usually wider than tall due to perspective
                if rw > 1.2 * rh:
                    results.append({
                        'bbox': (int(x), int(y), int(x + rw), int(y + rh)),
                        'class': 'pothole'
                    })
        return results