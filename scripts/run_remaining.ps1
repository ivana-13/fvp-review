# Runs everything that follows the actant-swap Qwen3-VL-2B run, in order, on this laptop.
# Safe to re-run: every step is resumable or overwrites its own output.
$env:PYTHONUTF8 = "1"
$env:UV_CACHE_DIR = "C:\tmp\uvcache"
$env:HF_HOME = "C:\tmp\hf"
$env:HF_HUB_DISABLE_PROGRESS_BARS = "1"
Set-Location $PSScriptRoot\..

uv run python scripts/run_probes.py --model qwen3vl-2b --subset action-replacement
uv run python scripts/check_gold_boxes.py --device cuda
uv run python scripts/run_encoder_foils.py --model siglip2-base --subset actant-swap --device cuda
uv run python scripts/run_encoder_foils.py --model siglip2-base --subset action-replacement --device cuda
uv run python scripts/run_encoder_foils.py --model clip-vit-l --subset actant-swap --device cuda
uv run python scripts/run_encoder_foils.py --model clip-vit-l --subset action-replacement --device cuda
uv run python scripts/analyze.py --model qwen3vl-2b
uv run python scripts/run_probes.py --model internvl35-2b --subset actant-swap
uv run python scripts/run_probes.py --model internvl35-2b --subset action-replacement
uv run python scripts/analyze.py --model internvl35-2b
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build_paper.ps1
