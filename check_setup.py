"""
Setup verification script - checks all requirements and dependencies
"""
import os
import sys

print("\n" + "=" * 70)
print("TRAFFIC VIOLATION DETECTION SYSTEM - SETUP CHECK")
print("=" * 70 + "\n")

# Check Python version
print(f"✓ Python version: {sys.version}")

# Check required files and directories
checks = {
    "✓" if os.path.exists("data/models/yolo_helmet.pt") else "✗": "YOLO Model (data/models/yolo_helmet.pt)",
    "✓" if os.path.exists("temp.mp4") or os.path.isdir("data/videos") else "✗": "Video file/directory",
    "✓" if os.path.exists("utils/config.py") else "✗": "Config file",
    "✓" if os.path.exists("main.py") else "✗": "Main script",
}

print("FILE CHECKS:")
for status, item in checks.items():
    print(f"  {status} {item}")

# Check Python packages
print("\nDEPENDENCY CHECKS:")
dependencies = [
    'cv2', 'numpy', 'pandas', 'torch', 'torchvision',
    'ultralytics', 'paddleocr', 'paddlepaddle', 'easyocr',
    'filterpy', 'sklearn', 'streamlit', 'flask'
]

missing = []
for package in dependencies:
    try:
        __import__(package)
        print(f"  ✓ {package}")
    except ImportError:
        print(f"  ✗ {package} (missing)")
        missing.append(package)

if missing:
    print(f"\n⚠️  MISSING PACKAGES: {', '.join(missing)}")
    print("Install with: pip install -r requirements.txt")

# Configuration
print("\nCONFIGURATION:")
try:
    from utils import config
    print(f"  ✓ Video path: {config.VIDEO_PATH}")
    print(f"  ✓ Model path: {config.MODEL_PATH}")
    print(f"  ✓ Helmet detection: {config.ENABLE_HELMET}")
    print(f"  ✓ ANPR: {config.ENABLE_ANPR}")
    print(f"  ✓ Blur faces: {config.ENABLE_BLUR}")
except Exception as e:
    print(f"  ✗ Error reading config: {e}")

print("\n" + "=" * 70)
print("NEXT STEPS:")
print("=" * 70)
print("1. Install dependencies: pip install -r requirements.txt")
print("2. Download YOLO model or update VIDEO_PATH in utils/config.py")
print("3. Add test video to project directory")
print("4. Run: python main.py")
print("=" * 70 + "\n")
