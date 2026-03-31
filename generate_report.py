"""
Generate CSV Report of All Violations (Dynamic Version)
"""
import os
import csv
from datetime import datetime

# Get all violation files
evidence_dir = "outputs/evidence"
if not os.path.exists(evidence_dir):
    os.makedirs(evidence_dir)

# Filename format: violation_{track_id}_{v_label}_{plate}.jpg
violation_files = sorted([f for f in os.listdir(evidence_dir) if f.startswith("violation_") and f.endswith(".jpg")])

print("\n" + "="*80)
print("GENERATING DYNAMIC VIOLATION REPORT")
print("="*80 + "\n")

# Create CSV report
csv_file = "outputs/csv/violations_report.csv"
os.makedirs(os.path.dirname(csv_file), exist_ok=True)

with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    
    # Write header
    writer.writerow([
        'Violation #',
        'Vehicle ID',
        'Violation Types',
        'License Plate',
        'Image File',
        'Evidence Path',
        'File Size (KB)',
        'Detected Time',
        'Status'
    ])
    
    # Write violation data
    for idx, filename in enumerate(violation_files, 1):
        filepath = os.path.join(evidence_dir, filename)
        file_size = os.path.getsize(filepath) / 1024  # Convert to KB
        
        # Parse filename: violation_{track_id}_{v_label}_{plate}.jpg
        parts = filename.replace('.jpg', '').split('_')
        
        vehicle_id = parts[1] if len(parts) > 1 else "Unknown"
        v_label = parts[2] if len(parts) > 2 else "Unknown"
        plate = parts[3] if len(parts) > 3 else "No Plate"
        
        # Clean up v_label (replace - with , )
        v_types = v_label.replace('-', ', ')
        
        writer.writerow([
            idx,                                    # Violation number
            vehicle_id,                             # Vehicle ID
            v_types,                                # Violation types
            plate,                                  # License Plate
            filename,                               # Image filename
            filepath,                               # Full path
            f"{file_size:.2f}",                     # File size
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Timestamp
            'Recorded'                              # Status
        ])

print(f"[OK] CSV Report Created: {csv_file}")
print(f"[OK] Total Violations: {len(violation_files)}")
print(f"\nReport Location: {csv_file}")

# Print sample data
print(f"\n" + "="*80)
print("SAMPLE VIOLATIONS (First 10):")
print("="*80 + "\n")

with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for idx, row in enumerate(reader):
        if idx < 10:
            print(f"  #{row[0]:<3} | ID: {row[1]:<5} | Plate: {row[3]:<12} | Types: {row[2]}")
        else:
            break

if len(violation_files) > 10:
    print(f"\n... and {len(violation_files) - 10} more violations")
print("\n" + "="*80)
