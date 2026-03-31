# Traffic Violation Verification Guide

## How to Verify if Violations are Correct

I've created a verification tool that allows you to manually check the accuracy of the detected violations. The system detected **1,189 violations** from your video.

## Running the Verification Tool

The verification script is currently running. Here's how to use it:

### Step 1: Choose How Many Violations to Verify
- Press Enter to verify ALL 1,189 violations (this will take a long time)
- Or enter a number like `50` to verify just the first 50 violations
- Or enter `100` to verify the first 100 violations

### Step 2: Choose Starting Point (Optional)
- Press Enter to start from violation #1
- Or enter a number like `500` to start from violation #500

### Step 3: Review Each Violation
For each violation, you'll see:
- The violation image with bounding boxes
- Violation details (ID, type, time, vehicle ID)
- Progress counter

### Step 4: Make Your Judgment
Press these keys:
- **`Y`** = Mark as CORRECT (violation is real)
- **`N`** = Mark as INCORRECT (false positive)
- **`S`** = SKIP this violation
- **`Q`** = Quit verification

## What to Look For

### Correct Violations Should Show:
- A motorcycle/bicycle rider **without a helmet**
- Clear view of the rider's head
- No helmet visible on the head
- Proper bounding box around the rider

### False Positives (Incorrect) Might Be:
- Rider actually wearing a helmet (helmet not detected)
- Poor image quality making it hard to tell
- Rider's head not clearly visible
- Detection error (wrong object detected as person)

## Output Files

After verification, the tool creates:
- **`verification_results.json`** - Detailed results of your verification
- **`verification_report.md`** - Summary report with accuracy statistics

## Tips for Efficient Verification

1. **Start Small**: Begin with 20-50 violations to get a sense of accuracy
2. **Focus on Clear Cases**: Skip ambiguous images initially
3. **Look at Patterns**: Note if certain violation types are more accurate
4. **Check Statistics**: The report will show overall accuracy percentage

## Expected Results

Based on typical AI system performance, you might expect:
- **80-95% accuracy** for clear, well-lit images
- **Lower accuracy** for poor lighting, motion blur, or distant objects
- **Helmet detection** is challenging due to helmet colors, angles, and styles

## Quick Verification Option

If you want a faster check, you can manually open some violation images in the `outputs/evidence/` folder to spot-check accuracy without the full verification tool.

Would you like me to help you analyze the verification results once you're done?