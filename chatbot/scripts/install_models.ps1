# Install recommended local models for Dobot MG400 RAG chatbot
# Stack: Qwen3-14B (Ollama) + Qwen3-Embedding-0.6B (Hugging Face)
# Target: RTX 5070 Ti 16GB

$ErrorActionPreference = "Stop"
$ChatbotDir = Split-Path -Parent $PSScriptRoot
Set-Location $ChatbotDir

Write-Host "==> Dobot MG400 RAG — install recommended models" -ForegroundColor Cyan
Write-Host "    LLM:      qwen3.5:9b (default) + qwen3:14b (quality)"
Write-Host "    Embed:    Qwen/Qwen3-Embedding-0.6B (HF)"
Write-Host "    GPU target: RTX 5070 Ti 16GB"
Write-Host ""

# --- Ollama LLM ---
$ollama = Get-Command ollama -ErrorAction SilentlyContinue
if (-not $ollama) {
    Write-Host "ERROR: ollama not found. Install from https://ollama.com then re-run." -ForegroundColor Red
    exit 1
}

foreach ($model in @("qwen3.5:9b", "qwen3:14b")) {
    Write-Host "==> ollama pull $model ..." -ForegroundColor Yellow
    ollama pull $model
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

Write-Host ""
Write-Host "==> Installed Ollama models:" -ForegroundColor Green
ollama list

# --- Hugging Face embedding (via project venv) ---
$venvPy = Join-Path $ChatbotDir ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPy)) {
    Write-Host "WARN: .venv not found. Create venv and pip install -r requirements.txt first." -ForegroundColor Yellow
    Write-Host "      Embedding will download automatically on first ingest/chat."
    exit 0
}

Write-Host ""
Write-Host "==> Pre-download embedding model into HF cache ..." -ForegroundColor Yellow
$env:HF_HUB_DISABLE_SYMLINKS_WARNING = "1"
& $venvPy -c @"
from sentence_transformers import SentenceTransformer
print('Loading Qwen/Qwen3-Embedding-0.6B ...')
m = SentenceTransformer('Qwen/Qwen3-Embedding-0.6B')
v = m.encode(['MG400 TCP port 29999'], normalize_embeddings=True)
print('OK embedding dim =', len(v[0]))
"@
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "==> Done." -ForegroundColor Green
Write-Host "Next:"
Write-Host "  1. Confirm chatbot\.env uses OLLAMA_MODEL=qwen3.5:9b (or switch in Streamlit sidebar)"
Write-Host "  2. python scripts/preprocess.py"
Write-Host "  3. python scripts/ingest.py --reset"
Write-Host "  4. streamlit run app\streamlit_app.py"
