# Rebuilds everything from scratch: download -> extract -> clocks -> visualization data -> figures.
# Usage (from the repository root):  powershell -ExecutionPolicy Bypass -File .\run_all.ps1
# Optional afterwards: scripts\05_methylclock_crosscheck.R (needs R).
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
if (-not (Test-Path .venv)) {
    python -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
}
$py = ".\.venv\Scripts\python.exe"
foreach ($s in "01_download_data", "02_extract_clock_cpgs", "03_compute_clocks", "04_build_visualization_data", "06_make_figures") {
    Write-Host "=== $s ==="
    & $py -I "scripts\$s.py"
    if ($LASTEXITCODE -ne 0) { throw "$s failed" }
}
Write-Host "Done. Open visualization\index.html in a browser."
