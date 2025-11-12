# Start Backend Server
Write-Host "Starting Flask Backend Server..." -ForegroundColor Green
Write-Host "Server will run on http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

cd csr_app
python app.py
