# 🚀 QUICK START GUIDE

Follow these steps to get the Traffic Violation Detection System running.

## Step 1: Install Dependencies (2 minutes)
```bash
pip install -r requirements.txt
```

## Step 2: Verify Installation (1 minute)
```bash
python check_setup.py
```
This will show what's installed and what's missing.

## Step 3: Prepare Video Input (3 options)

### Option A: Create a Test Video (Recommended for First Run)
```bash
python create_test_video.py
```
This generates a sample `temp.mp4` video with moving vehicles.

### Option B: Use Your Own Video
Place your MP4 video file at the project root:
```
c:\Users\USER\Downloads\traffic_ai_system\temp.mp4
```

Or update the path in `utils/config.py`:
```python
VIDEO_PATH = "path/to/your/video.mp4"
```

### Option C: Use a Video from data/videos
```python
# In utils/config.py, update:
VIDEO_PATH = "data/videos/your_video.mp4"
```

## Step 4: Get YOLO Model

The system needs a YOLO model at `data/models/yolo_helmet.pt`.

### Option A: Use Existing Model
If you have a pre-trained YOLO model, place it at:
```
data/models/yolo_helmet.pt
```

### Option B: Download Pre-trained Model
```bash
# Create directory
mkdir -p data\models

# Download a YOLO model (example)
# You can download from: https://docs.ultralytics.com/
```

### Option C: Use Default YOLOv8
The system will auto-download YOLOv8 on first run if the model path is missing.

## Step 5: Configure Settings (Optional)

Edit `utils/config.py` to enable/disable features:

```python
ENABLE_HELMET = True        # ✓ Enable helmet detection
ENABLE_ANPR = True          # ✓ Enable license plate reading
ENABLE_BLUR = True          # ✓ Enable face blurring
ENABLE_SPEED = True         # ✓ Enable speed estimation
ENABLE_LANE = True          # ✓ Enable lane detection
ENABLE_POTHOLE = False      # ✗ Disable pothole detection

VIDEO_PATH = "temp.mp4"     # Your video file
MODEL_PATH = "data/models/yolo_helmet.pt"
```

## Step 6: Run the System! 🎮

```bash
python main.py
```

### During Execution:
- **Watch** real-time detection in the video window
- **Press ESC** to stop processing
- **Check console** for violation alerts

### After Execution:
Violations and evidence saved to:
- **evidences**: `outputs/evidence/violation_*.jpg`
- **Logs**: `outputs/logs/`
- **CSV reports**: `outputs/csv/`

## Step 7: View Results

```bash
# Windows
explorer outputs\evidence

# Or check the files:
dir outputs\evidence
dir outputs\csv
dir outputs\logs
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Module not found error | Run `pip install -r requirements.txt` |
| Video file not found | Run `python create_test_video.py` first |
| Model file not found | Download YOLO model or use auto-download |
| No violations detected | Ensure video has moving objects and config is correct |
| Slow processing | Use GPU or disable unused features |

## Web Interfaces (Optional)

### View Results in Web Dashboard
```bash
streamlit run app\streamlit_app.py
```
Then open: http://localhost:8501

### REST API Server (Optional)
```bash
python app\flask_api.py
```

---

## File Structure After Setup

```
traffic_ai_system/
├── temp.mp4                          ← YOUR VIDEO FILE
├── main.py                           ← MAIN SCRIPT
├── check_setup.py                    ← VERIFY SETUP
├── create_test_video.py              ← CREATE TEST VIDEO
├── requirements.txt
├── README.md
│
├── data/
│   └── models/
│       └── yolo_helmet.pt            ← YOLO MODEL
│
├── utils/
│   └── config.py                     ← SETTINGS
│
└── outputs/                          ← RESULTS
    ├── evidence/                     ← Violation Images
    ├── csv/                          ← CSV Logs
    └── logs/                         ← Text Logs
```

---

## Example Output

After running `python main.py`, you'll see:

```
============================================================
Traffic Violation Detection System - Starting...
============================================================
✓ Video file found: temp.mp4
✓ Model file found: data/models/yolo_helmet.pt
✓ Models loaded successfully

Opening video: temp.mp4
✓ Video loaded: 300 frames @ 30.0 fps

============================================================
Processing video...
============================================================

[VIOLATION #1] ID:1 Plate:AB1234CD
[VIOLATION #2] ID:2 Plate:XY5678ZW

============================================================
Processing Complete!
============================================================
Total violations detected: 2
Evidence saved to: outputs/evidence/
Logs saved to: outputs/logs/
============================================================
```

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Create test video
3. ✅ Run main script
4. ✅ Check results in outputs/
5. 📚 Read README.md for detailed documentation
6. 🎯 Customize config.py for your needs
7. 🌐 Try web interface (optional)

---

## Commands Reference

```bash
# Check setup
python check_setup.py

# Create sample video
python create_test_video.py

# Run main system
python main.py

# View dashboard (web)
streamlit run app\streamlit_app.py

# List violations
dir outputs\evidence

# View logs
type outputs\logs\*.log
```

---

**Questions?** Check README.md for detailed documentation.
