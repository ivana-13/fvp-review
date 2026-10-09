# Queue of 2026-09-11. Runs, in order, on the laptop GPU:
#   checkpoint 0: re-analyse both 2B models (controls now complete) and rebuild the paper
#   Qwen3-VL-8B (4-bit): yes/no diagnostic, probes on both subsets, controls, blind likelihood, wording check
#   wording check for the two 2B models
#   checkpoint 1: analyse + paper
#   structured verification for Qwen3-VL-2B, InternVL3.5-2B, Qwen3-VL-8B
#   checkpoint 2: analyse + paper
#   Qwen3-VL-4B (4-bit): probes, controls, blind likelihood, wording, verification
#   final: analyse all + paper
# Every step is resumable, so re-run this script after an interruption (a closed lid ends the run):
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_queue_full.ps1
# Progress and ETA:  uv run python scripts/status.py --watch
$env:PYTHONUTF8 = "1"; $env:UV_CACHE_DIR = "C:\tmp\uvcache"; $env:HF_HOME = "C:\tmp\hf"; $env:HF_HUB_DISABLE_PROGRESS_BARS = "1"
Set-Location $PSScriptRoot\..
$log = "outputs\queue_full.log"

function Step([string]$name, [string]$cmd, [string]$out = "") {
    $line = "=== $name  $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ==="
    Write-Host $line
    Add-Content -Path $log -Value $line
    if ($out) { cmd /c "$cmd > $out 2>&1" } else { cmd /c "$cmd >> $log 2>&1" }
    if ($LASTEXITCODE -ne 0) { $msg = "    step '$name' exited with code $LASTEXITCODE"; Write-Host $msg; Add-Content -Path $log -Value $msg }
}
function Analyse([string[]]$models) {
    foreach ($m in $models) { Step "analyse $m" "uv run python scripts/analyze.py --model $m" }
}
function Paper() { Step "paper build" "powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build_paper.ps1" }
function ModelBlock([string]$m, [string]$label) {
    Step "$label probes actant-swap" "uv run python scripts/run_probes.py --model $m --subset actant-swap"
    Step "$label probes action-replacement" "uv run python scripts/run_probes.py --model $m --subset action-replacement"
    Step "$label controls" "uv run python scripts/run_controls.py --model $m"
    Step "$label blind likelihood actant-swap" "uv run python scripts/run_blind_ll.py --model $m --subset actant-swap"
    Step "$label blind likelihood action-replacement" "uv run python scripts/run_blind_ll.py --model $m --subset action-replacement"
    Step "$label wording check" "uv run python scripts/run_wording.py --model $m"
}

Add-Content -Path $log -Value "##### queue started $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') #####"

# checkpoint 0
Analyse @("qwen3vl-2b", "internvl35-2b"); Paper

# Qwen3-VL-8B (4-bit)
$m8 = "qwen3vl-8b-4bit"
if (-not (Test-Path "outputs\diag_yesno_$m8.log")) {
    Step "8B yes/no diagnostic" "uv run python scripts/diag_yesno.py --model $m8 --n 5" "outputs\diag_yesno_$m8.log"
}
ModelBlock $m8 "8B"
Step "2B wording check qwen3vl-2b" "uv run python scripts/run_wording.py --model qwen3vl-2b"
Step "2B wording check internvl35-2b" "uv run python scripts/run_wording.py --model internvl35-2b"
Analyse @("qwen3vl-2b", "internvl35-2b", $m8); Paper   # checkpoint 1

# structured verification
Step "verification qwen3vl-2b" "uv run python scripts/run_verify.py --model qwen3vl-2b"
Step "verification internvl35-2b" "uv run python scripts/run_verify.py --model internvl35-2b"
Step "verification $m8" "uv run python scripts/run_verify.py --model $m8"
Analyse @("qwen3vl-2b", "internvl35-2b", $m8); Paper   # checkpoint 2

# Qwen3-VL-4B (4-bit)
$m4 = "qwen3vl-4b-4bit"
ModelBlock $m4 "4B"
Step "verification $m4" "uv run python scripts/run_verify.py --model $m4"
Analyse @("qwen3vl-2b", "internvl35-2b", $m8, $m4); Paper   # final

$done = "##### queue finished $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') #####"
Write-Host $done; Add-Content -Path $log -Value $done
