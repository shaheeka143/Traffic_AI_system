from ultralytics import YOLO

class Detector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect(self, frame, conf=0.25):
        results = self.model(frame, conf=conf)
        return results[0] 