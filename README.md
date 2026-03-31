# Traffic Violation Detection System

AI-powered traffic monitoring system that detects vehicle violations including helmet violations, license plate reading, speed violations, and pothole detection.

## Prerequisites

- Python 3.8+
- GPU (CUDA) recommended for faster processing
- Webcam or video file

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup YOLO Model
The system uses YOLO for vehicle detection. The model should be at: `data/models/yolo_helmet.pt`

**Option A: Use Existing Model**
If you have the model file, place it at `data/models/yolo_helmet.pt`

**Option B: Download or Train**
```bash
# Create the directory if it doesn't exist
mkdir -p data/models

# Download a pre-trained YOLO model (optional)
# Or train your own: https://docs.ultralytics.com/
```

### 3. Prepare Video Input
Place your video file at one of these locations:
- `temp.mp4` (default)
- `data/videos/sample.mp4` (update `VIDEO_PATH` in `utils/config.py`)
- Any path (update `VIDEO_PATH` in `utils/config.py`)

## Quick Start

### 1. Verify Setup
```bash
python check_setup.py
```
This checks all dependencies and file requirements.

### 2. Configure Settings
Edit `utils/config.py` to enable/disable features:
```python
ENABLE_HELMET = True        # Detect missing helmets
ENABLE_ANPR = True          # Read license plates
ENABLE_BLUR = True          # Blur faces in output
ENABLE_SPEED = True         # Estimate vehicle speed
ENABLE_LANE = True          # Detect wrong-way driving
ENABLE_POTHOLE = False      # Detect potholes

VIDEO_PATH = "temp.mp4"     # Path to your video
MODEL_PATH = "data/models/yolo_helmet.pt"
```

### 3. Run the System
```bash
python main.py
```

**Controls:**
- Press `ESC` to stop processing
- Frame window shows real-time detection

## Output

Results are saved in the `outputs/` directory:

```
outputs/
├── evidence/        # Violation screenshots
├── csv/            # Violation logs (CSV)
└── logs/           # Detailed logs
```

## Features

### 1. **Helmet Detection**
Detects motorcyclists without helmets

### 2. **Automatic Number Plate Recognition (ANPR)**
Reads and recognizes license plates from detected vehicles

### 3. **Speed Estimation**
Estimates vehicle speed (requires calibration)

### 4. **Lane Detection**
Detects vehicles driving on wrong side of road

### 5. **Pothole Detection**
Identifies road hazards and potholes

### 6. **Face Blurring**
Auto-blurs faces in evidence photos for privacy

## Troubleshooting

### ❌ "Video file not found"
- Ensure video path is correct in `utils/config.py`
- Check file exists at the specified path

### ❌ "Model file not found"
- Download/place YOLO model at `data/models/yolo_helmet.pt`
- Or update `MODEL_PATH` in `utils/config.py`

### ❌ "Missing packages"
```bash
pip install -r requirements.txt
```

### ❌ No violations detected
- Check video has moving vehicles
- Verify `ENABLE_HELMET = True` in config
- Video quality affects detection

### ❌ Low FPS / Slow processing
- Use GPU: Install CUDA version of PyTorch
- Reduce video resolution
- Disable unused features in config

## Web Interfaces

### Streamlit Dashboard
```bash
streamlit run app/streamlit_app.py
```
Open: http://localhost:8501

### Flask REST API
```bash
python app/flask_api.py
```

## Project Structure

```
├── main.py                 # Main processing script
├── requirements.txt        # Python dependencies
├── check_setup.py         # Setup verification
│
├── app/
│   ├── flask_api.py       # REST API
│   └── streamlit_app.py   # Web dashboard
│
├── data/
│   ├── models/
│   │   └── yolo_helmet.pt # YOLO model
│   └── videos/
│
├── modules/
│   ├── detection.py       # YOLO detection
│   ├── tracking.py        # Vehicle tracking
│   ├── helmet.py          # Helmet detection
│   ├── anpr.py           # License plate reading
│   ├── blur.py           # Face blurring
│   ├── speed.py          # Speed estimation
│   ├── lane.py           # Lane detection
│   └── pothole.py        # Pothole detection
│
├── utils/
│   ├── config.py         # Configuration
│   ├── helpers.py        # Utility functions
│   └── visualization.py  # Visualization utilities
│
└── outputs/
    ├── evidence/         # Violation images
    ├── csv/             # CSV logs
    └── logs/            # Text logs
```

## Configuration Reference

**utils/config.py:**
```python
# Feature Toggles
ENABLE_HELMET = True        # Helmet violation detection
ENABLE_ANPR = True          # License plate recognition
ENABLE_BLUR = True          # Privacy-preserving face blur
ENABLE_SPEED = True         # Speed estimation
ENABLE_LANE = True          # Wrong-way driving detection
ENABLE_POTHOLE = False      # Pothole detection (experimental)

# File Paths
MODEL_PATH = "data/models/yolo_helmet.pt"  # YOLO model path
VIDEO_PATH = "temp.mp4"                    # Input video path

# Parameters
MAX_RIDERS = 2              # Max riders per vehicle
SPEED_LIMIT = 60            # Speed limit (km/h)
```

## Performance Tips

1. **Use GPU**: Install CUDA-enabled PyTorch for 5-10x speed improvement
2. **Lower Resolution**: Process at 480p instead of 1080p
3. **Skip Optional Features**: Disable unused detection modules
4. **Decrease FPS**: Process every Nth frame for batch processing

## Common Issues

| Issue | Solution |
|-------|----------|
| Module not found | Run `pip install -r requirements.txt` |
| CUDA out of memory | Reduce video resolution or batch size |
| No detections | Video too blurry or model needs tuning |
| Slow processing | Use GPU or decrease resolution |

## License

[Your License Here]

## Support

For issues or questions, check:
1. Run `python check_setup.py` to verify setup
2. Check logs in `outputs/logs/`
3. Review error messages in console output
