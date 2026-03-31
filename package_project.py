
import os
import zipfile

def zip_project(output_filename):
    # Files/Dirs to EXCLUDE (too large or not needed)
    # We include 'outputs/csv' to show reports, but exclude 'outputs/evidence' and video files.
    exclude_dirs = {'.venv', 'venv', '__pycache__', 'runs', '.git', '.gemini', '.antigravity', 'evidence'}
    exclude_exts = {'.mp4', '.avi', '.pt', '.zip'}

    print(f"Creating COMPLETE project package: {output_filename}")
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            # Prune exclude_dirs
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if any(file.endswith(ext) for ext in exclude_exts):
                    continue
                
                file_path = os.path.join(root, file)
                if os.path.abspath(file_path) == os.path.abspath(output_filename):
                    continue
                    
                rel_path = os.path.relpath(file_path, '.')
                print(f"  + Adding: {rel_path}")
                zipf.write(file_path, rel_path)

if __name__ == "__main__":
    zip_project('../traffic_ai_system_final_results.zip')
    print("\n[OK] Project successfully zipped in the parent folder: ../traffic_ai_system_final_results.zip")
