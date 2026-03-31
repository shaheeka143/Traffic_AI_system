
import cv2
import numpy as np
import os
from modules.anpr import read_plate

def test_ocr():
    print("--- TESTING EASYOCR LOGIC ---")
    
    # 1. Create a dummy license plate image
    # (White background with black text)
    plate_img = np.ones((100, 300, 3), dtype=np.uint8) * 255
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = "MH12 DE 1234"
    cv2.putText(plate_img, text, (20, 65), font, 1.5, (0, 0, 0), 3)
    
    # Save for manual verification if needed
    os.makedirs("outputs/test", exist_ok=True)
    cv2.imwrite("outputs/test/mock_plate.png", plate_img)
    print(f"[OK] Created mock plate image with text: '{text}'")

    # 2. Run the actual OCR function
    print("Running EasyOCR (this may download weights on first run)...")
    result = read_plate(plate_img)
    
    print("-" * 30)
    print(f"EXPECTED: {text.replace(' ', '')}")
    print(f"DETECTED: {result}")
    print("-" * 30)
    
    if result.replace("-", "").replace(" ", "") == text.replace(" ", ""):
        print("SUCCESS: OCR accurately read the plate!")
    else:
        print("PARTIAL MATCH or FAILED (Expected exact match for clean image)")

if __name__ == "__main__":
    test_ocr()
