@echo off
title UAi PsychePortal Integrated Suite Launcher
echo ====================================================================
echo             UAi PsychePortal Integrated Suite Launcher
echo ====================================================================
echo.
echo This launcher will start all 4 components of your AI Internship folder
echo in separate, dedicated command windows.
echo.
echo 1. Counsellor Flask Backend (Port 5000)
echo 2. Student Survey Portal Flask App (Port 5001)
echo 3. React + Vite Counsellor Dashboard Frontend (Port 5173)
echo 4. Psychometric Quiz Desktop Application (Tkinter GUI)
echo.
echo ====================================================================
echo.
pause

echo.
set "PROJECT_ROOT=%~dp0.."

echo [1/4] Starting UAi Counsellor Flask Backend on Port 5000...
start "UAi Flask Counsellor Backend" /D "%PROJECT_ROOT%" cmd /c "echo === UAi Flask Counsellor Backend === && python run.py"

echo [2/4] Starting UAi Student Survey Portal on Port 5001...
start "UAi Flask Student Survey Portal" /D "%PROJECT_ROOT%\student-survey-portal" cmd /c "echo === UAi Flask Student Survey Portal === && python app.py"

echo [3/4] Starting React+Vite Counsellor Dashboard Frontend on Port 5173...
start "UAi React Counsellor Dashboard" /D "%PROJECT_ROOT%\uai-counsellor-dashboard" cmd /c "echo === UAi React Counsellor Dashboard === && npm.cmd run dev -- --force"

echo [4/4] Starting Psychometric Quiz Desktop Application (Tkinter)...
start "UAi Psychometric Quiz App" /D "%PROJECT_ROOT%\UAI_Quiz_App" cmd /c "echo === UAi Psychometric Quiz Desktop App === && python main.py"

echo.
echo ====================================================================
echo All 4 components have been successfully launched!
echo.
echo - Counsellor Backend: http://127.0.0.1:5000/
echo - Student Survey Portal: http://127.0.0.1:5001/
echo - React Dashboard Frontend: http://localhost:5173/
echo ====================================================================
echo.
pause
