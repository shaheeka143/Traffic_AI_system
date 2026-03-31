@echo off
echo ============================================================
echo   TRAFFIC AI SYSTEM - QUICK START SCRIPT
echo ============================================================
echo.
echo 1. Run Complete Analysis (main.py)
echo 2. Run Headless Mode (Fast - main_headless.py)
echo 3. Run Web Dashboard (Streamlit)
echo 4. Generate Late-Summary Report
echo 5. EXIT
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" python main.py
if "%choice%"=="2" python main_headless.py
if "%choice%"=="3" streamlit run app/streamlit_app.py
if "%choice%"=="4" python generate_report.py
if "%choice%"=="5" exit

pause
