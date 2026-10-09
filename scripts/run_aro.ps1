# ARO queue: the 2B models on the ARO VG-Relation subsets (non-spatial relations, capped at 150 per relation, and a
# 300-item left/right sample): probes on both subsets, blind likelihood, controls on the relation subset, analysis,
# paper rebuild. Every step is resumable; re-run after an interruption (a closed lid ends the run).
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_aro.ps1
# Progress:  uv run python scripts/status.py --watch   (the ARO steps are at the bottom of the list)
$env:PYTHONUTF8 = "1"; $env:UV_CACHE_DIR = "C:\tmp\uvcache"; $env:HF_HOME = "C:\tmp\hf"; $env:HF_HUB_DISABLE_PROGRESS_BARS = "1"
Set-Location $PSScriptRoot\..
$log = "outputs\aro_queue.log"

function Step([string]$name, [string]$cmd) {
    $line = "=== $name  $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ==="
    Write-Host $line
    Add-Content -Path $log -Value $line
    cmd /c "$cmd >> $log 2>&1"
    if ($LASTEXITCODE -ne 0) { $msg = "    step '$name' exited with code $LASTEXITCODE"; Write-Host $msg; Add-Content -Path $log -Value $msg }
}

Add-Content -Path $log -Value "##### ARO queue started $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') #####"
if (-not (Test-Path "data\joined\aro-relation.valid.jsonl")) { Step "ARO join" "uv run python scripts/prepare_aro.py" }
if (-not (Test-Path "data\aro\fetch_done.txt")) { Step "ARO images" "uv run python scripts/fetch_aro_images.py" }

foreach ($m in @("qwen3vl-2b", "internvl35-2b")) {
    foreach ($s in @("aro-relation", "aro-spatial")) {
        Step "$m probes $s" "uv run python scripts/run_probes.py --model $m --subset $s"
        Step "$m blind likelihood $s" "uv run python scripts/run_blind_ll.py --model $m --subset $s"
    }
    Step "$m controls aro-relation" "uv run python scripts/run_controls.py --model $m --subset aro-relation"
    Step "analyse $m" "uv run python scripts/analyze.py --model $m"
}
Step "paper build" "powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build_paper.ps1"
$done = "##### ARO queue finished $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') #####"
Write-Host $done; Add-Content -Path $log -Value $done
