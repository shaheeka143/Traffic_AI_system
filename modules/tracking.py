import numpy as np

class Tracker:
    def __init__(self):
        self.id_counter = 0
        self.tracked_objects = {}  # {id: (bbox_tensor, last_frame_seen)}

    def update(self, results):
        if results.boxes is None or len(results.boxes.data) == 0:
            return []

        # Convert to numpy for distance calculation
        current_detections = []
        for det in results.boxes.data:
            x1, y1, x2, y2, conf, cls = det.tolist()
            center = np.array([(x1 + x2) / 2, (y1 + y2) / 2])
            current_detections.append({'bbox': det, 'center': center})

        new_tracks = []
        
        # Simple distance-based matching
        for det in current_detections:
            matched_id = None
            min_dist = 100 # Match within 100 pixels
            
            for tid, (tbbox, _) in self.tracked_objects.items():
                tx1, ty1, tx2, ty2, _, _ = tbbox.tolist()
                tcenter = np.array([(tx1 + tx2) / 2, (ty1 + ty2) / 2])
                dist = np.linalg.norm(det['center'] - tcenter)
                
                if dist < min_dist:
                    min_dist = dist
                    matched_id = tid
            
            if matched_id is not None:
                self.tracked_objects[matched_id] = (det['bbox'], 0) # Update spot
                new_tracks.append((matched_id, det['bbox']))
            else:
                self.id_counter += 1
                self.tracked_objects[self.id_counter] = (det['bbox'], 0)
                new_tracks.append((self.id_counter, det['bbox']))
                
        # Optional: Cleanup tracks (omitting for simplicity)
        return new_tracks