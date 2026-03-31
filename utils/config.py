# ============================================================================
# TRAFFIC VIOLATION DETECTION SYSTEM - CONFIGURATION
# ============================================================================

# FEATURE TOGGLES
ENABLE_HELMET = True
ENABLE_ANPR = True
ENABLE_BLUR = True
ENABLE_SPEED = True
ENABLE_LANE = True
ENABLE_POTHOLE = False

# MAXIMUM RIDERS ALLOWED
MAX_RIDERS = 2

# SPEED LIMIT (KM/H)
SPEED_LIMIT = 60

# FILE PATHS
MODEL_PATH = "data/models/yolo_helmet.pt"
POTHOLE_MODEL_PATH = None # Set to "data/models/pothole.pt" if you have it!
VIDEO_PATH = "temp.mp4"

# OUTPUT SETTINGS
OUTPUT_DIR = "outputs"
EVIDENCE_DIR = "outputs/evidence"

# ADVANCED SETTINGS
CONFIDENCE_THRESHOLD = 0.75
FRAME_SKIP = 1