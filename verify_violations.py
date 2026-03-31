#!/usr/bin/env python3
"""
Traffic Violation Verification Tool
Allows manual verification of detected violations to assess accuracy.
"""

import os
import cv2
import pandas as pd
import numpy as np
from datetime import datetime
import json

class ViolationVerifier:
    def __init__(self, csv_path, evidence_dir):
        self.csv_path = csv_path
        self.evidence_dir = evidence_dir
        self.verification_results = []
        self.current_index = 0

        # Load violation data
        try:
            self.df = pd.read_csv(csv_path)
            print(f"Loaded {len(self.df)} violations from CSV")
        except Exception as e:
            print(f"Error loading CSV: {e}")
            self.df = pd.DataFrame()

    def display_violation(self, violation_data):
        """Display a single violation for verification"""
        image_path = os.path.join(self.evidence_dir, violation_data['Image File'])

        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
            return None

        # Load and display image
        img = cv2.imread(image_path)
        if img is None:
            print(f"Could not load image: {image_path}")
            return None

        # Add text overlay with violation details
        overlay = img.copy()
        alpha = 0.7

        # Create text info
        info_lines = [
            f"Violation #{violation_data['Violation #']}",
            f"Vehicle ID: {violation_data['Vehicle ID']}",
            f"Type: {violation_data['Violation Type']}",
            f"Time: {violation_data['Detected Time']}",
            f"File: {violation_data['Image File']}",
            "",
            "Press 'Y' for Correct, 'N' for Incorrect, 'S' to Skip, 'Q' to Quit"
        ]

        # Draw semi-transparent overlay
        cv2.rectangle(overlay, (10, 10), (600, 200), (0, 0, 0), -1)
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

        # Add text
        y_offset = 40
        for line in info_lines:
            cv2.putText(img, line, (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX,
                       0.6, (255, 255, 255), 2)
            y_offset += 25

        return img

    def verify_violations(self, start_index=0, max_violations=None):
        """Main verification loop"""
        if self.df.empty:
            print("No violation data loaded")
            return

        self.current_index = start_index
        total_violations = len(self.df) if max_violations is None else min(max_violations, len(self.df))

        print(f"Starting verification from violation #{start_index + 1}")
        print(f"Total violations to verify: {total_violations}")
        print("Controls: Y=Correct, N=Incorrect, S=Skip, Q=Quit")

        while self.current_index < total_violations:
            violation = self.df.iloc[self.current_index]

            # Display violation
            img = self.display_violation(violation)
            if img is None:
                self.current_index += 1
                continue

            # Show progress
            progress = f"Progress: {self.current_index + 1}/{total_violations}"
            cv2.putText(img, progress, (img.shape[1] - 300, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.imshow('Violation Verification', img)

            # Wait for user input
            key = cv2.waitKey(0) & 0xFF

            if key == ord('q') or key == ord('Q'):
                print("Verification stopped by user")
                break
            elif key == ord('y') or key == ord('Y'):
                self.verification_results.append({
                    'violation_id': violation['Violation #'],
                    'vehicle_id': violation['Vehicle ID'],
                    'violation_type': violation['Violation Type'],
                    'image_file': violation['Image File'],
                    'verified_correct': True,
                    'verified_at': datetime.now().isoformat()
                })
                print(f"✓ Violation #{violation['Violation #']} marked as CORRECT")
            elif key == ord('n') or key == ord('N'):
                self.verification_results.append({
                    'violation_id': violation['Violation #'],
                    'vehicle_id': violation['Vehicle ID'],
                    'violation_type': violation['Violation Type'],
                    'image_file': violation['Image File'],
                    'verified_correct': False,
                    'verified_at': datetime.now().isoformat()
                })
                print(f"✗ Violation #{violation['Violation #']} marked as INCORRECT")
            elif key == ord('s') or key == ord('S'):
                print(f"⚠ Violation #{violation['Violation #']} SKIPPED")
            else:
                print("Invalid key pressed. Use Y/N/S/Q")
                continue

            self.current_index += 1

        cv2.destroyAllWindows()

    def save_verification_results(self, output_path):
        """Save verification results to JSON file"""
        if not self.verification_results:
            print("No verification results to save")
            return

        # Calculate statistics
        total_verified = len(self.verification_results)
        correct = sum(1 for r in self.verification_results if r['verified_correct'])
        incorrect = total_verified - correct
        accuracy = (correct / total_verified * 100) if total_verified > 0 else 0

        results_data = {
            'verification_summary': {
                'total_verified': total_verified,
                'correct': correct,
                'incorrect': incorrect,
                'accuracy_percentage': round(accuracy, 2),
                'verification_date': datetime.now().isoformat()
            },
            'detailed_results': self.verification_results
        }

        try:
            with open(output_path, 'w') as f:
                json.dump(results_data, f, indent=2)
            print(f"Verification results saved to: {output_path}")
            print(f"Accuracy: {accuracy:.2f}% ({correct}/{total_verified} correct)")
        except Exception as e:
            print(f"Error saving results: {e}")

    def generate_verification_report(self, output_path):
        """Generate a detailed verification report"""
        if not self.verification_results:
            print("No verification results available")
            return

        # Group by violation type
        type_stats = {}
        for result in self.verification_results:
            vtype = result['violation_type']
            if vtype not in type_stats:
                type_stats[vtype] = {'total': 0, 'correct': 0, 'incorrect': 0}
            type_stats[vtype]['total'] += 1
            if result['verified_correct']:
                type_stats[vtype]['correct'] += 1
            else:
                type_stats[vtype]['incorrect'] += 1

        # Create report
        report = f"""# Traffic Violation Verification Report

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary Statistics
- Total violations verified: {len(self.verification_results)}
- Correct detections: {sum(1 for r in self.verification_results if r['verified_correct'])}
- Incorrect detections: {sum(1 for r in self.verification_results if not r['verified_correct'])}
- Overall accuracy: {sum(1 for r in self.verification_results if r['verified_correct']) / len(self.verification_results) * 100:.2f}%

## Accuracy by Violation Type
"""

        for vtype, stats in type_stats.items():
            accuracy = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
            report += f"- {vtype}: {accuracy:.2f}% ({stats['correct']}/{stats['total']} correct)\n"

        report += "\n## Incorrect Detections\n"
        incorrect_results = [r for r in self.verification_results if not r['verified_correct']]
        for result in incorrect_results[:20]:  # Show first 20 incorrect
            report += f"- Violation #{result['violation_id']}: {result['violation_type']} (Vehicle {result['vehicle_id']})\n"

        if len(incorrect_results) > 20:
            report += f"- ... and {len(incorrect_results) - 20} more\n"

        try:
            with open(output_path, 'w') as f:
                f.write(report)
            print(f"Verification report saved to: {output_path}")
        except Exception as e:
            print(f"Error saving report: {e}")

def main():
    # Configuration
    csv_path = r"c:\Users\USER\Downloads\traffic_ai_system\outputs\csv\violations_report.csv"
    evidence_dir = r"c:\Users\USER\Downloads\traffic_ai_system\outputs\evidence"
    results_path = r"c:\Users\USER\Downloads\traffic_ai_system\verification_results.json"
    report_path = r"c:\Users\USER\Downloads\traffic_ai_system\verification_report.md"

    # Initialize verifier
    verifier = ViolationVerifier(csv_path, evidence_dir)

    # Ask user how many violations to verify
    print("Traffic Violation Verification Tool")
    print("=" * 40)
    print(f"Total violations available: {len(verifier.df)}")
    print()

    try:
        max_verify = input("How many violations would you like to verify? (press Enter for all): ").strip()
        max_verify = int(max_verify) if max_verify else None

        start_from = input("Start from violation number? (press Enter for 1): ").strip()
        start_from = int(start_from) - 1 if start_from else 0  # Convert to 0-based index

        if start_from < 0 or start_from >= len(verifier.df):
            print("Invalid start position")
            return

        # Start verification
        verifier.verify_violations(start_from, max_verify)

        # Save results
        if verifier.verification_results:
            verifier.save_verification_results(results_path)
            verifier.generate_verification_report(report_path)

    except KeyboardInterrupt:
        print("\nVerification interrupted by user")
    except Exception as e:
        print(f"Error during verification: {e}")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()