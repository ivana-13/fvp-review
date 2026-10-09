# Joint-box control on the laptop GPU for the models cached here, then a paper rebuild. Resumable.
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_jointbox_laptop.ps1
$env:PYTHONUTF8 = "1"; $env:UV_CACHE_DIR = "C:\tmp\uvcache"; $env:HF_HOME = "C:\tmp\hf"; $env:HF_HUB_DISABLE_PROGRESS_BARS = "1"
Set-Location $PSScriptRoot\..
$log = "outputs\jointbox_queue.log"
function Step([string]$name, [string]$cmd) {
    $line = "=== $name  $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ==="
    Write-Host $line; Add-Content -Path $log -Value $line
    cmd /c "$cmd >> $log 2>&1"
    if ($LASTEXITCODE -ne 0) { $msg = "    step '$name' exited with code $LASTEXITCODE"; Write-Host $msg; Add-Content -Path $log -Value $msg }
}
Add-Content -Path $log -Value "##### joint-box queue started $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') #####"
foreach ($m in @("qwen3vl-2b", "internvl35-2b", "qwen3vl-4b-4bit", "qwen3vl-8b-4bit")) {
    Step "joint-box $m actant-swap" "uv run python scripts/run_jointbox.py --model $m --subset actant-swap"
}
Step "paper build" "powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build_paper.ps1"
$done = "##### joint-box queue finished $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') #####"
Write-Host $done; Add-Content -Path $log -Value $done
