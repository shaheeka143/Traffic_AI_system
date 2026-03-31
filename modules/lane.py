# Wrong side / Lane violation detection
_lane_history = {}

def check_wrong_side(track_id, center_x, center_y, width, height):
    global _lane_history
    
    # Simple lane rule:
    # Vehicles on the left half (x < width/2) should be moving LEFT/DOWN
    # Vehicles on the right half (x > width/2) should be moving RIGHT/UP
    
    if track_id not in _lane_history:
        _lane_history[track_id] = (center_x, center_y)
        return False
        
    prev_x, prev_y = _lane_history[track_id]
    _lane_history[track_id] = (center_x, center_y)
    
    # Determine direction
    dx = center_x - prev_x
    dy = center_y - prev_y
    
    # Basic rule for demo
    if center_x < width / 2: # Left side
        if dx > 5: # moving towards right side is "wrong" OR if dy < 0 (moving up)
            return True
    else: # Right side
        if dx < -5: # moving towards left side is "wrong"
            return True
            
    return False