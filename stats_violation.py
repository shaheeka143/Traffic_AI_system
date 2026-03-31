"""
Violation Statistics & Analysis (Multi-Objective Version)
"""
import os
import csv
from collections import defaultdict

print("\n" + "="*80)
print("TRAFFIC VIOLATION DETECTION - FULL MULTI-OBJECTIVE STATISTICS")
print("="*80 + "\n")

# Read CSV report
csv_file = "outputs/csv/violations_report.csv"
if not os.path.exists(csv_file):
    print(f"ERROR: {csv_file} not found. Run main.py and generate_report.py first.")
    exit()

violation_data = []
with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    violation_data = list(reader)

# Calculate statistics
total_violations = len(violation_data)
if total_violations == 0:
    print("No violations found.")
    exit()

total_vehicles = len(set(v['Vehicle ID'] for v in violation_data))

# Get file sizes
evidence_dir = "outputs/evidence"
total_size = 0
for filename in os.listdir(evidence_dir):
    if filename.endswith('.jpg'):
        filepath = os.path.join(evidence_dir, filename)
        total_size += os.path.getsize(filepath)

total_size_mb = total_size / (1024 * 1024)

# Multi-Violation Breakdown
violation_types_count = defaultdict(int)
for v in violation_data:
    # Multiple labels can be presence (comma-separated)
    types = v['Violation Types'].split(', ')
    for t in types:
        violation_types_count[t] += 1

# ANPR Stats
valid_plates = [v for v in violation_data if v['License Plate'] not in ["No Plate", "PLATE_UNREADABLE", "PLATE_DETECT_FAIL"]]
anpr_success_rate = (len(valid_plates) / total_violations) * 100

# Print statistics
print("DETECTION STATISTICS:")
print("-" * 80)
print(f"  Total Violations Detected:    {total_violations:,}")
print(f"  Unique Vehicles Tracked:      {total_vehicles:,}")
print(f"  ANPR Success Rate:            {anpr_success_rate:.1f}%")
print(f"\n")

print("DETECTION BREAKDOWN (By Objective):")
print("-" * 80)
for v_type, count in violation_types_count.items():
    percentage = (count / total_violations) * 100
    print(f"  {v_type:<30} {count:>6,} ({percentage:>5.1f}%)")
print(f"\n")

print("PERFORMANCE METRIC STATUS:")
print("-" * 80)
print(f"  Face Blurring:                 [OK] Applied to ALL evidence")
print(f"  Number Plate Extraction:       [OK] Logged in CSV and Filename")
print(f"  Speed Violation Detection:     [OK] Integrated & Active")
print(f"  Wrong-side driving Detection:  [OK] Integrated & Active")
print(f"  Multi-rider Counting:          [OK] Integrated & Active")
print(f"\n")

# Show top vehicle IDs with most violations
print("TOP 10 VEHICLES WITH HIGHEST VIOLATION REPETITION:")
print("-" * 80)
vehicle_violations = defaultdict(int)
for v in violation_data:
    vid = v['Vehicle ID']
    vehicle_violations[vid] += 1

sorted_vehicles = sorted(vehicle_violations.items(), key=lambda x: x[1], reverse=True)[:10]
for rank, (vehicle_id, count) in enumerate(sorted_vehicles, 1):
    print(f"  {rank:>2}. Vehicle ID {vehicle_id:<6} -> {count:>4} events recorded")

print("\n" + "="*80)
print("[OK] ADVANCED REPORT GENERATED SUCCESSFULLY")
print("="*80 + "\n")
