# 🚦 REAL-TIME TRAFFIC VIOLATION DETECTION VIEWER

## 🎬 WHAT YOU'LL SEE

The real-time viewer shows live video processing with:

### 📺 **Video Window Features:**

1. **Live Video Feed** - Your traffic video playing in real-time
2. **Detection Boxes** - Colored rectangles around detected objects:
   - 🟢 **Green**: Vehicles (cars, motorcycles, trucks)
   - 🔵 **Blue**: Persons
   - 🟠 **Orange**: Motorcycles
   - 🔴 **Red**: VIOLATIONS (helmet violations)

3. **Status Overlay** - Top information bar showing:
   - Current frame number and time
   - Detection statistics
   - Active features status
   - Control instructions

4. **Violation Alerts** - When violations detected:
   - 🚨 "VIOLATION!" text appears
   - Red bounding box around violating vehicle
   - Vehicle ID displayed
   - Console log of violation details

---

## 🎮 **CONTROLS**

| Key | Action |
|-----|--------|
| **ESC** | Stop processing and exit |
| **P** | Pause/Resume video |
| **S** | Save current frame as image |
| **C** | Clear violation statistics |
| **H** | Toggle help overlay |

---

## 📊 **WHAT GETS DETECTED**

### Objects Detected:
- **Persons** (pedestrians, riders)
- **Vehicles** (cars, motorcycles, trucks, buses)
- **Traffic violations** (helmet violations)

### Real-Time Statistics:
- Frame count and processing time
- Number of objects detected
- Vehicles being tracked
- Violations found
- Current FPS (frames per second)

---

## 🚨 **VIOLATION DETECTION**

When a **helmet violation** is detected:

1. **Red Alert Box** - Vehicle gets red bounding box
2. **VIOLATION! Label** - Large red text appears
3. **Vehicle ID** - Unique tracking number
4. **Face Blurring** - Privacy protection (if enabled)
5. **Evidence Saving** - Frame saved to outputs/evidence/
6. **Console Log** - Details printed to terminal

---

## 📈 **PERFORMANCE INDICATORS**

### Real-Time Metrics:
- **FPS**: Processing speed (frames per second)
- **Detections**: Objects found in current frame
- **Tracking**: Vehicles being followed across frames
- **Violations**: Total violations detected so far

### Color Coding:
- 🟢 Green: Normal vehicles
- 🔴 Red: Violations
- 🔵 Blue: Persons
- 🟡 Yellow: Status information

---

## 🎯 **HOW TO USE**

### 1. **Start the Viewer:**
```bash
python real_time_viewer.py
```

### 2. **Watch the Video:**
- Video plays automatically
- Detections appear in real-time
- Statistics update continuously

### 3. **Interact:**
- Press **P** to pause and examine a frame
- Press **S** to save interesting frames
- Press **ESC** when done

### 4. **Monitor Results:**
- Watch console for violation alerts
- Check outputs/evidence/ for saved frames
- Review statistics in status bar

---

## 📱 **WINDOW LAYOUT**

```
┌─────────────────────────────────────────────────┐
│ 🚦 Real-Time Traffic Violation Detection        │
│ Frame: 150/300 | Time: 5.0s | FPS: 29.8        │
│ Detections: 8 | Vehicles: 3 | Violations: 2    │
│ Helmet:ON | ANPR:ON | Blur:ON | Paused:NO      │
│ Controls: ESC=Exit | P=Pause | S=Save | H=Help │
├─────────────────────────────────────────────────┤
│                                                 │
│          [VIDEO FRAME WITH DETECTIONS]          │
│                                                 │
│  🟢 Vehicle ID:1                                │
│  🔴 🚨 VIOLATION! ID:2                          │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 🔍 **DETECTION DETAILS**

### What Gets Tracked:
- **Vehicle IDs**: Each vehicle gets unique number
- **Movement**: Vehicles tracked across frames
- **Violations**: Helmet checks on motorcycles
- **Evidence**: Automatic saving of violation frames

### Visual Indicators:
- **Bounding Boxes**: Show object locations
- **Confidence Scores**: Detection certainty (0.00-1.00)
- **Class Labels**: Person, car, motorcycle, etc.
- **Violation Markers**: Special red highlighting

---

## 💾 **OUTPUT FILES**

### Evidence Images:
- **Location:** `outputs/evidence/`
- **Naming:** `rt_violation_[ID]_f[frame].jpg`
- **Content:** Full frame with detections
- **Frequency:** Saved every 60 frames (~2 seconds)

### Console Output:
```
[VIOLATION #1] ID:2 | Plate:MH02AB1234 | Frame:45
[VIOLATION #2] ID:5 | Plate:DL01CD5678 | Frame:89
```

---

## ⚙️ **CONFIGURATION**

### Active Features:
- **Helmet Detection**: ✅ ON (detects no-helmet violations)
- **ANPR**: ✅ ON (reads license plates)
- **Face Blurring**: ✅ ON (privacy protection)
- **Real-Time Display**: ✅ ON (live video window)

### Video Settings:
- **Source:** `data/videos/sample.mp4`
- **Resolution:** Auto-detected
- **FPS:** Original video FPS
- **Display:** 1280x720 window

---

## 🎬 **EXAMPLE SCENARIO**

### Frame 45 - Normal Traffic:
```
Objects: 6 persons, 2 cars, 1 motorcycle
Vehicles Tracked: 3
Violations: 0
Status: Normal traffic flow
```

### Frame 67 - Violation Detected:
```
🚨 VIOLATION DETECTED!
Vehicle ID: 2 (motorcycle)
Status: No helmet
Plate: MH02AB1234
Action: Face blurred, evidence saved
```

### Frame 89 - Another Violation:
```
🚨 VIOLATION DETECTED!
Vehicle ID: 5 (motorcycle)
Status: No helmet
Plate: DL01CD5678
Action: Face blurred, evidence saved
```

---

## 📊 **STATISTICS TRACKING**

### Live Metrics:
- **Frame Counter**: Current frame / total frames
- **Time Elapsed**: Seconds since start
- **Detection Count**: Objects found this frame
- **Tracking Count**: Vehicles being followed
- **Violation Count**: Total violations found
- **Processing FPS**: Real-time speed

### Historical Data:
- **Total Frames**: All frames processed
- **Peak Detections**: Maximum objects in one frame
- **Violation Rate**: Violations per minute
- **Evidence Files**: Images saved to disk

---

## 🚨 **VIOLATION WORKFLOW**

1. **Detection**: YOLO finds motorcycle
2. **Tracking**: Assigns unique ID
3. **Analysis**: Checks for helmet
4. **Decision**: No helmet = VIOLATION
5. **Alert**: Red box + VIOLATION text
6. **Privacy**: Face blurring applied
7. **Evidence**: Frame saved to disk
8. **Logging**: Details printed to console

---

## 🎯 **TROUBLESHOOTING**

### If Video Doesn't Play:
- Check video file exists: `data/videos/sample.mp4`
- Verify video format (MP4 recommended)
- Check file permissions

### If No Detections:
- Video might be too dark/blurry
- Objects might be too small
- Try different video angle

### If Slow Performance:
- Close other applications
- Lower video resolution
- Disable ANPR for faster processing

### If Window Doesn't Show:
- Check graphics drivers
- Try running without background processes
- Use smaller window size

---

## 🎬 **NEXT STEPS**

### After Viewing:
1. **Stop the viewer** (press ESC)
2. **Check evidence** in `outputs/evidence/`
3. **Review statistics** from console output
4. **Process another video** by updating config
5. **Export results** for reports

### Advanced Usage:
- **Pause and analyze** specific frames
- **Save key moments** with 'S' key
- **Monitor performance** via FPS counter
- **Adjust settings** in `utils/config.py`

---

**The real-time viewer is now running! Watch the live video with detections and violations displayed in real-time!** 🚦📹