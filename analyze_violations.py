#!/usr/bin/env python3
"""
Quick Violation Analysis Script
Provides statistics and sample analysis without full manual verification
"""

import os
import pandas as pd
import random
from collections import Counter

def analyze_violations(csv_path, evidence_dir, sample_size=20):
    """Analyze violation data and show statistics"""

    # Load data
    df = pd.read_csv(csv_path)
    print(f"📊 VIOLATION ANALYSIS REPORT")
    print(f"=" * 50)
    print(f"Total violations detected: {len(df)}")
    print()

    # Violation type distribution
    violation_types = Counter(df['Violation Type'])
    print("🚨 Violation Types Distribution:")
    for vtype, count in violation_types.most_common():
        percentage = (count / len(df)) * 100
        print(".1f")
    print()

    # File size analysis
    file_sizes = df['File Size (KB)']
    print("📁 File Size Statistics:")
    print(f"  Average: {file_sizes.mean():.1f} KB")
    print(f"  Minimum: {file_sizes.min():.1f} KB")
    print(f"  Maximum: {file_sizes.max():.1f} KB")
    print()

    # Time distribution
    df['Detected Time'] = pd.to_datetime(df['Detected Time'])
    time_range = df['Detected Time'].max() - df['Detected Time'].min()
    print("⏰ Detection Time Range:")
    print(f"  From: {df['Detected Time'].min()}")
    print(f"  To: {df['Detected Time'].max()}")
    print(f"  Duration: {time_range}")
    print()

    # Sample some violations for manual check
    print(f"🔍 SAMPLE VIOLATIONS FOR MANUAL CHECK ({sample_size} random samples):")
    print("-" * 70)

    sample_indices = random.sample(range(len(df)), min(sample_size, len(df)))
    for i, idx in enumerate(sample_indices, 1):
        violation = df.iloc[idx]
        print(f"{i:2d}. Violation #{violation['Violation #']:4d} | Vehicle {violation['Vehicle ID']:3d}")
        print(f"    Type: {violation['Violation Type']}")
        print(f"    Image: {violation['Image File']}")
        print(f"    Size: {violation['File Size (KB)']:6.1f} KB")
        print(f"    Time: {violation['Detected Time']}")
        print()

    # Check if evidence files exist
    print("✅ EVIDENCE FILE VERIFICATION:")
    existing_files = 0
    missing_files = 0

    for _, violation in df.iterrows():
        image_path = os.path.join(evidence_dir, violation['Image File'])
        if os.path.exists(image_path):
            existing_files += 1
        else:
            missing_files += 1

    print(f"  Files present: {existing_files}")
    print(f"  Files missing: {missing_files}")
    print(".1f")
    print()

    # Recommendations
    print("💡 RECOMMENDATIONS:")
    if missing_files > 0:
        print(f"  ⚠️  {missing_files} evidence files are missing - check file paths")

    if len(violation_types) == 1:
        print("  📝 Only one violation type detected - system may be focused")
    else:
        print("  📝 Multiple violation types detected - diverse detection capability")

    avg_size = file_sizes.mean()
    if avg_size < 500:
        print("  🖼️  Small image files - good for storage, may lack detail")
    elif avg_size > 2000:
        print("  🖼️  Large image files - high detail but storage intensive")

    print()
    print("🔧 NEXT STEPS:")
    print("  1. Run 'python verify_violations.py' for manual verification")
    print("  2. Check sample images listed above")
    print("  3. Review verification_results.json after manual check")
    print("  4. Read VIOLATION_VERIFICATION_GUIDE.md for detailed instructions")

if __name__ == "__main__":
    csv_path = r"c:\Users\USER\Downloads\traffic_ai_system\outputs\csv\violations_report.csv"
    evidence_dir = r"c:\Users\USER\Downloads\traffic_ai_system\outputs\evidence"

    analyze_violations(csv_path, evidence_dir)