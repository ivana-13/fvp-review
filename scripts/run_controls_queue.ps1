# Controls for both pointing models, then re-analyse and rebuild the paper.
# Runs after run_remaining.ps1 (which was already executing when this was added).
$env:PYTHONUTF8 = "1"
$env:UV_CACHE_DIR = "C:\tmp\uvcache"
$env:HF_HOME = "C:\tmp\hf"
$env:HF_HUB_DISABLE_PROGRESS_BARS = "1"
Set-Location $PSScriptRoot\..
uv run python scripts/run_blind_ll.py --model qwen3vl-2b --subset actant-swap
uv run python scripts/run_blind_ll.py --model qwen3vl-2b --subset action-replacement
uv run python scripts/run_blind_ll.py --model internvl35-2b --subset actant-swap
uv run python scripts/run_blind_ll.py --model internvl35-2b --subset action-replacement
uv run python scripts/run_controls.py --model qwen3vl-2b
uv run python scripts/run_controls.py --model internvl35-2b
uv run python scripts/analyze.py --model qwen3vl-2b
uv run python scripts/analyze.py --model internvl35-2b
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build_paper.ps1
