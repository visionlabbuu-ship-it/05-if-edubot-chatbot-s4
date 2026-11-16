# Start Dobot MG400 local RAG chatbot (Streamlit)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "Creating venv and installing dependencies..."
    python -m venv .venv
    .\.venv\Scripts\python.exe -m pip install --upgrade pip
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
}

# Ensure Ollama is up (optional)
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
try {
    $null = Invoke-RestMethod "http://127.0.0.1:11434/api/tags" -TimeoutSec 2
} catch {
    $ollama = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"
    if (Test-Path $ollama) {
        Write-Host "Starting Ollama..."
        Start-Process $ollama -WindowStyle Hidden
        Start-Sleep -Seconds 3
    }
}

Write-Host "Launching Streamlit on http://localhost:8501"
& .\.venv\Scripts\streamlit.exe run app\streamlit_app.py --server.headless true
