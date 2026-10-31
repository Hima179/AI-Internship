Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host "            UAi PsychePortal Integrated Suite Launcher" -ForegroundColor Cyan
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This launcher will start all 4 components of your AI Internship folder"
Write-Host "in separate terminal jobs:"
Write-Host "1. Counsellor Flask Backend (Port 5000)" -ForegroundColor Green
Write-Host "2. Student Survey Portal Flask App (Port 5001)" -ForegroundColor Green
Write-Host "3. React + Vite Counsellor Dashboard Frontend (Port 5173)" -ForegroundColor Green
Write-Host "4. Psychometric Quiz Desktop Application (Tkinter GUI)" -ForegroundColor Green
Write-Host ""
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to start all components..."

$ProjectRoot = Resolve-Path "$PSScriptRoot\.."

Write-Host "Launching UAi Counsellor Flask Backend..." -ForegroundColor Yellow
Start-Process powershell -WorkingDirectory $ProjectRoot -ArgumentList "-NoExit", "-Command", "`$Host.UI.RawUI.WindowTitle='UAi Flask Counsellor Backend'; python run.py"

Write-Host "Launching UAi Student Survey Portal..." -ForegroundColor Yellow
Start-Process powershell -WorkingDirectory "$ProjectRoot\student-survey-portal" -ArgumentList "-NoExit", "-Command", "`$Host.UI.RawUI.WindowTitle='UAi Flask Student Survey Portal'; python app.py"

Write-Host "Launching React+Vite Counsellor Dashboard..." -ForegroundColor Yellow
Start-Process powershell -WorkingDirectory "$ProjectRoot\uai-counsellor-dashboard" -ArgumentList "-NoExit", "-Command", "`$Host.UI.RawUI.WindowTitle='UAi React Counsellor Dashboard'; npm.cmd run dev -- --force"

Write-Host "Launching Psychometric Quiz Desktop Application..." -ForegroundColor Yellow
Start-Process powershell -WorkingDirectory "$ProjectRoot\UAI_Quiz_App" -ArgumentList "-NoExit", "-Command", "`$Host.UI.RawUI.WindowTitle='UAi Psychometric Quiz App'; python main.py"

Write-Host ""
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host "All 4 components launched in separate PowerShell windows!" -ForegroundColor Green
Write-Host "- Counsellor Backend: http://127.0.0.1:5000/"
Write-Host "- Student Survey Portal: http://127.0.0.1:5001/"
Write-Host "- React Dashboard Frontend: http://localhost:5173/"
Write-Host "====================================================================" -ForegroundColor Cyan
