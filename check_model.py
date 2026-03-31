from ultralytics import YOLO
import sys

try:
    model = YOLO('data/models/yolo_helmet.pt')
    print("Classes:", model.names)
except Exception as e:
    print("Error:", e)
