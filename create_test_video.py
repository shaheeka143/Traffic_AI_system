"""
Test video generator - Creates a simple test video for system testing
"""
import cv2
import numpy as np
import os

def create_test_video(output_path="temp.mp4", duration=10, fps=30, width=640, height=480):
    """
    Creates a simple test video with moving shapes to simulate vehicles
    
    Args:
        output_path: Path to save the video
        duration: Duration in seconds
        fps: Frames per second
        width: Video width
        height: Video height
    """
    print(f"\n{'='*60}")
    print("CREATING TEST VIDEO")
    print(f"{'='*60}")
    print(f"Output: {output_path}")
    print(f"Duration: {duration}s @ {fps} fps")
    print(f"Resolution: {width}x{height}")
    
    # Video codec and writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    if not out.isOpened():
        print("❌ Failed to create video writer!")
        return False
    
    total_frames = duration * fps
    
    print(f"\nGenerating {total_frames} frames...")
    for frame_num in range(total_frames):
        # Create frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Add background (sky and road)
        frame[0:height//3, :] = [135, 206, 235]  # Sky (blue)
        frame[height//3:, :] = [100, 100, 100]   # Road (gray)
        
        # Add lane markings
        for y in range(height//3, height, 30):
            cv2.line(frame, (width//2, y), (width//2, y+15), (255, 255, 255), 2)
        
        # Simulate moving vehicles (rectangles)
        # Vehicle 1: Moving left to right
        x1 = (frame_num * 2) % (width + 100) - 50
        y1 = height // 2 - 30
        cv2.rectangle(frame, (x1, y1), (x1 + 80, y1 + 40), (0, 0, 255), -1)  # Red rectangle
        cv2.putText(frame, "Vehicle", (x1 + 5, y1 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Vehicle 2: Moving right to left
        x2 = width - ((frame_num * 2) % (width + 100)) + 50
        y2 = height // 2 + 50
        cv2.rectangle(frame, (x2, y2), (x2 + 80, y2 + 40), (0, 255, 0), -1)  # Green rectangle
        cv2.putText(frame, "Bike", (x2 + 5, y2 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Add frame info
        cv2.putText(frame, f"Frame: {frame_num+1}/{total_frames}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Road Scene for Traffic Detection", (10, height-20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Write frame
        out.write(frame)
        
        # Progress bar
        if (frame_num + 1) % (total_frames // 10) == 0:
            progress = int(((frame_num + 1) / total_frames) * 100)
            print(f"  [{progress}%] {frame_num + 1}/{total_frames} frames generated")
    
    out.release()
    
    # Verify file was created
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # Size in MB
        print(f"\n✓ Test video created successfully!")
        print(f"  File: {output_path}")
        print(f"  Size: {file_size:.2f} MB")
        print(f"\n{'='*60}")
        print("You can now run: python main.py")
        print(f"{'='*60}\n")
        return True
    else:
        print("❌ Failed to create video file!")
        return False

if __name__ == "__main__":
    # Create test video
    create_test_video()
