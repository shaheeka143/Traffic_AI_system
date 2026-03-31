from ultralytics import YOLO
from utils import config

_helmet_model = None


def _get_helmet_model():
    global _helmet_model
    if _helmet_model is None:
        _helmet_model = YOLO(config.MODEL_PATH)
    return _helmet_model


def check_helmet(crop):
    """Detects if a person is wearing a helmet.

    Returns:
      - "helmet" when helmet is detected in crop
      - "no_helmet" when helmet is missing (or no detection)

    Uses the YOLO model at utils/config.py:MODEL_PATH (default data/models/yolo_helmet.pt).
    """
    if crop is None or crop.size == 0:
        return "no_helmet"

    model = _get_helmet_model()

    # Run the helmet model on the cropped rider region.
    # Lower imgsz for speed if needed.
    results = model(crop, imgsz=320, conf=0.25)

    if not results or not results[0].boxes:
        return "no_helmet"

    # If model has an explicit helmet class, use it, otherwise any detection is considered helmet.
    class_names = results[0].names
    for box in results[0].boxes:
        cls = int(box.cls[0])
        label = class_names.get(cls, "").lower()
        if "helmet" in label:
            return "helmet"

    # Fallback: if there is at least one box, assume a helmet was detected (model should be trained for helmet)
    return "helmet" if len(results[0].boxes) > 0 else "no_helmet"