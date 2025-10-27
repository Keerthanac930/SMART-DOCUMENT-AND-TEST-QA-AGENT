# Start Frontend React Application on Port 3000
# Smart Document & Test QA Agent Frontend

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Starting QA Agent Frontend (Port 3000)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to frontend directory
Set-Location frontend_react

# Check if node_modules exists
if (-Not (Test-Path "node_modules")) {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Green
    npm install
}

Write-Host ""
Write-Host "🚀 Starting React dev server on http://localhost:3000" -ForegroundColor Green
Write-Host "🔗 Backend API: http://localhost:8000" -ForegroundColor Green
Write-Host ""
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the dev server
npm run dev
