
import os
import subprocess

def run_all():
    print("=" * 60)
    print("🚦 STARTING TRAFFIC AI COMPLETE PIPELINE (Auto-Save Active)")
    print("=" * 60)
    
    # 1. Main Detection
    print("\n[1/4] Running Objective-Based Detection...")
    # Limiting to 500 frames for speed, user can change to 0 for full video
    subprocess.run(["python", "main.py"], check=True)
    
    # 2. Report Generation
    print("\n[2/4] Generating Violation CSV Report...")
    subprocess.run(["python", "generate_report.py"], check=True)
    
    # 3. Stats Calculation
    print("\n[3/4] Calculating Performance Percentages...")
    subprocess.run(["python", "stats_violation.py"], check=True)
    
    # 4. Final Packaging
    print("\n[4/4] Creating Final Project ZIP...")
    subprocess.run(["python", "package_project.py"], check=True)
    
    print("\n" + "=" * 60)
    print("🏁 PIPELINE COMPLETE. ALL FOLDERS UPDATED AND SAVED")
    print("=" * 60)

if __name__ == "__main__":
    run_all()
