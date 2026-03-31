# Simple speed estimation based on displacement
import numpy as np

# global dictionary to store position of objects across frames
# id: [last_x, last_y]
_history = {}

def estimate_speed(track_id, center_x, center_y, fps=30):
    global _history
    
    if track_id not in _history:
        _history[track_id] = (center_x, center_y)
        return 0
    
    prev_x, prev_y = _history[track_id]
    
    # Simple distance in pixels
    dist = np.sqrt((center_x - prev_x)**2 + (center_y - prev_y)**2)
    
    # Convert pixels to arbitrary speed factor
    # For demo: 1 pixel/frame at 30fps is ~5km/h?
    speed = dist * (fps / 30) * 10
    
    # Update position
    _history[track_id] = (center_x, center_y)
    
    return speed