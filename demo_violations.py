"""
DEMO SCRIPT - Simulates the violation detection pipeline
Shows what happens when violations are detected
"""
import cv2
import os
import random
import numpy as np
from datetime import datetime

print("\n" + "="*70)
print("TRAFFIC VIOLATION DETECTION SYSTEM - DEMO")
print("="*70 + "\n")

# Create output directories
os.makedirs("outputs/evidence", exist_ok=True)
os.makedirs("outputs/csv", exist_ok=True)
os.makedirs("outputs/logs", exist_ok=True)

# Simulate video processing
print("SIMULATING VIDEO PROCESSING...")
print("-" * 70)

violation_count = 0
violations_data = []

# Simulate 10 vehicles detected in the video
for vehicle_id in range(1, 11):
    # Random chance of violation
    if random.random() < 0.6:  # 60% chance of violation
        violation_count += 1
        
        # Generate random violation data
        plate_number = f"MH{random.randint(1, 99):02d}{chr(random.randint(65, 90))}{random.randint(1000, 9999)}"
        speed = random.randint(40, 120)
        
        # Create a simple violation image (for demo)
        # In real system, this would be frame from video
        
        # Create a simple demo image using numpy
        height, width = 480, 640
        img = np.ones((height, width, 3), dtype=np.uint8) * 100  # Gray background
        
        # Add text overlay
        cv2.putText(img, f"VIOLATION - Vehicle ID: {vehicle_id}", (50, 100), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(img, f"Plate: {plate_number}", (50, 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        cv2.putText(img, f"Speed: {speed} km/h", (50, 200), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        cv2.putText(img, "NO HELMET DETECTED", (50, 250),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
        
        # Save "evidence" image
        evidence_file = f"outputs/evidence/violation_{vehicle_id}.jpg"
        cv2.imwrite(evidence_file, img)
        print(f"✓ [VIOLATION #{violation_count}] ID:{vehicle_id} Plate:{plate_number} Speed:{speed}km/h")
        violations_data.append({
            'id': vehicle_id,
            'plate': plate_number,
            'speed': speed,
            'violation_type': 'helmet_violation' if random.random() < 0.5 else 'speed_violation'
        })

print("\n" + "="*70)
print("DEMO COMPLETE!")
print("="*70)
print(f"\nTotal violations simulated: {violation_count}")
print(f"\nOUTPUT FILES CREATED:")
print(f"  • Evidence images: outputs/evidence/violation_*.jpg ({violation_count} files)")
print(f"  • Logs: outputs/logs/")
print(f"\n" + "="*70)
print("\nWHAT THIS DEMO SHOWS:")
print("-" * 70)
print("1. DETECTION: YOLO model finds vehicles in video")
print("2. TRACKING: System assigns each vehicle an ID")
print("3. ANALYSIS: System checks each vehicle for violations:")
print("   - Helmet detection")
print("   - License plate reading")
print("   - Speed estimation")
print("4. EVIDENCE: Saves violation images to outputs/evidence/")
print("5. LOGGING: Records violation details in logs")
print("\n" + "="*70)
print("\nTO SEE REAL VIOLATIONS:")
print("-" * 70)
print("1. Provide a real traffic video (with actual vehicles)")
print("2. Run: python main.py")
print("3. Check outputs/evidence/ for violation images")
print("4. Check outputs/logs/ for violation details")
print("\n" + "="*70 + "\n")
