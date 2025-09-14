Write-Host "Starting Lecture Schedule Preparation System..." -ForegroundColor Green
Write-Host ""

# Start backend in background job
$backendJob = Start-Job { cd "$pwd\schedule-builder\backend"; python app\main.py }
Write-Host "Backend server job started (ID: $($backendJob.Id))" -ForegroundColor Yellow

# Start frontend in background job
$frontendJob = Start-Job { cd "$pwd\schedule-builder\frontend"; npm start }
Write-Host "Frontend server job started (ID: $($frontendJob.Id))" -ForegroundColor Yellow

Write-Host ""
Write-Host "Both servers are starting..." -ForegroundColor Green
Write-Host "Frontend will be available at http://localhost:3002" -ForegroundColor Cyan
Write-Host "Backend API will be available at http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Documentation at http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Check job status with: Get-Job" -ForegroundColor Gray
Write-Host "View job output with: Receive-Job -Id <JobId>" -ForegroundColor Gray
Write-Host "Stop jobs with: Stop-Job -Id <JobId>" -ForegroundColor Gray