import easyocr
import numpy as np
import cv2

# Initialize the reader once to avoid reloading models (Singleton pattern)
_reader = None

def get_reader():
    global _reader
    if _reader is None:
        # Initializing for English (can add 'hi' etc. for multi-lingual)
        # gpu=True will use CUDA if available
        _reader = easyocr.Reader(['en'], gpu=False) 
    return _reader

def read_plate(image):
    """
    Reads license plate text from a cropped image using EasyOCR with 
    additional preprocessing to improve accuracy.
    """
    if image is None or image.size == 0:
        return "PLATE_DETECT_FAIL"

    try:
        # 1. OPTIMIZE IMAGE FOR OCR
        # Resize - OCR works better with slightly larger clear text
        height, width = image.shape[:2]
        if width < 250: # If too small, upscale
            scale = 2 
            image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        
        # Convert to Grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # Sharpening & Denoising
        # Bilateral filter is good for keeping character edges while reducing background noise
        denoised = cv2.bilateralFilter(gray, 11, 17, 17)
        
        # Adaptive Thresholding to make text pop against plate background
        thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY, 11, 2)

        reader = get_reader()
        # Read the text from processed image
        results = reader.readtext(thresh, detail=0)
        
        if not results:
            # Fallback to original image if thresholding was too aggressive
            results = reader.readtext(image, detail=0)

        if not results:
            return "PLATE_UNREADABLE"
            
        plate_text = " ".join(results).upper().strip()
        
        import re
        plate_text = re.sub(r'[^A-Z0-9-]', '', plate_text)
        
        return plate_text if plate_text else "PLATE_UNREADABLE"
        
    except Exception as e:
        print(f"EasyOCR Error: {e}")
        return "OCR_ERROR"