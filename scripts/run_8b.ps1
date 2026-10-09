# Full experiment with Qwen3-VL-8B. Default: 4-bit weights (nf4), about 7 GB of VRAM.
# If test_8b_memory.ps1 failed, run with:  -Model qwen3vl-8b-offload   (bf16 with CPU offload; slow but safe)
# All steps are resumable; re-run after an interruption.
param([string]$Model = "qwen3vl-8b-4bit")
$env:PYTHONUTF8 = "1"; $env:UV_CACHE_DIR = "C:\tmp\uvcache"; $env:HF_HOME = "C:\tmp\hf"; $env:HF_HUB_DISABLE_PROGRESS_BARS = "1"
Set-Location $PSScriptRoot\..
uv run python scripts/run_probes.py --model $Model --subset actant-swap
uv run python scripts/run_probes.py --model $Model --subset action-replacement
uv run python scripts/run_controls.py --model $Model
uv run python scripts/analyze.py --model $Model
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build_paper.ps1
