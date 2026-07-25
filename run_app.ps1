param(
    [int]$Port = 8020
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ExistingPython = "C:\Users\anujj\OneDrive\Documents\GitHub\chatapp\.venv\Scripts\python.exe"
$BundledPython = "C:\Users\anujj\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

Set-Location $ProjectRoot

if (Test-Path $ExistingPython) {
    $Python = $ExistingPython
} elseif (Test-Path ".venv\Scripts\python.exe") {
    $Python = ".venv\Scripts\python.exe"
} elseif (Test-Path $BundledPython) {
    $Python = $BundledPython
} else {
    $Python = "python"
}

& $Python manage.py migrate
& $Python manage.py seed_chat
Write-Host "ChatFlow running at http://127.0.0.1:$Port/"
Write-Host "Press Ctrl+C to stop."
& $Python manage.py runserver "127.0.0.1:$Port"
