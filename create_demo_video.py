import cv2
import numpy as np
import os

def create_demo_video(output_path="demo_violations.mp4", duration=10, fps=30, width=640, height=480):
    print(f"Creating Demonstration Video: {output_path}")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    total_frames = duration * fps
    
    for frame_num in range(total_frames):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Background
        frame[0:height//3, :] = [135, 206, 235]  # Sky
        frame[height//3:, :] = [70, 70, 70]      # Road
        
        # Lane divider
        cv2.line(frame, (width//2, 0), (width//2, height), (255, 255, 255), 2)
        
        # --- VIOLATION 1: OVERSPEED ---
        # Moving very fast (30 pixels per frame)
        ox = (frame_num * 30) % (width + 100) - 50
        oy = height // 2 - 100
        cv2.rectangle(frame, (ox, oy), (ox+80, oy+40), (255, 255, 0), -1)
        cv2.putText(frame, "car", (ox+5, oy+25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
        
        # --- VIOLATION 2: WRONG SIDE ---
        # Moving right (dx > 0) on the left side
        wx = (frame_num * 5) % (width//2 - 50) + 10
        wy = height // 2 + 50
        cv2.rectangle(frame, (wx, wy), (wx+60, wy+40), (0, 255, 255), -1)
        cv2.putText(frame, "car", (wx+5, wy+25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
        
        # --- VIOLATION 3: MULTI-RIDER ---
        # Stationary or slow motorcycle on right side with 3 persons
        mx, my = width // 2 + 100, height // 2 + 100
        # Slowly moving motorcycle
        mx += (frame_num % 100) 
        cv2.rectangle(frame, (mx, my), (mx+60, my+40), (0, 255, 0), -1)
        cv2.putText(frame, "motorcycle", (mx+2, my+35), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
        
        # 3 Persons inside/near the motorcycle box
        for i in range(3):
            px, py = mx + 20, my + 10 + i*5
            cv2.rectangle(frame, (px, py), (px+10, py+10), (255, 0, 0), -1)
            cv2.putText(frame, "person", (px, py-2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 1)

        out.write(frame)
        
    out.release()
    print(f"Demo video created at {output_path}")

if __name__ == "__main__":
    create_demo_video()
