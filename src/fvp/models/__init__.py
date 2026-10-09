"""Model registry. Every wrapper exposes:

    yes_prob(image | None, caption) -> float          P(Yes) vs P(No)
    choose_sym(image | None, a, b) -> float            order-debiased P(a)
    generate(image | None, prompt, max_new_tokens) -> str
    ground(image, target_phrase) -> GroundResult       with .raw and .boxes_px (original pixels)
"""

from __future__ import annotations

REGISTRY = {
    "qwen3vl-2b": ("fvp.models.qwen3vl", "Qwen3VL", {"model_id": "Qwen/Qwen3-VL-2B-Instruct"}),
    "qwen3vl-4b": ("fvp.models.qwen3vl", "Qwen3VL", {"model_id": "Qwen/Qwen3-VL-4B-Instruct"}),
    "qwen3vl-8b": ("fvp.models.qwen3vl", "Qwen3VL", {"model_id": "Qwen/Qwen3-VL-8B-Instruct"}),
    # 8B on an 8 GB laptop GPU: 4-bit weights (about 7 GB) or bf16 with CPU offload (slow but safe)
    "qwen3vl-8b-4bit": ("fvp.models.qwen3vl", "Qwen3VL", {"model_id": "Qwen/Qwen3-VL-8B-Instruct", "quantization": "nf4", "max_pixels": 640 * 32 * 32}),
    "qwen3vl-8b-offload": ("fvp.models.qwen3vl", "Qwen3VL", {"model_id": "Qwen/Qwen3-VL-8B-Instruct", "offload_gpu_gib": 6.5, "max_pixels": 640 * 32 * 32}),
    "qwen3vl-4b-4bit": ("fvp.models.qwen3vl", "Qwen3VL", {"model_id": "Qwen/Qwen3-VL-4B-Instruct", "quantization": "nf4", "max_pixels": 640 * 32 * 32}),
    "qwen3vl-2b-4bit": ("fvp.models.qwen3vl", "Qwen3VL", {"model_id": "Qwen/Qwen3-VL-2B-Instruct", "quantization": "nf4"}),
    "internvl35-2b": ("fvp.models.internvl", "InternVL", {"model_id": "OpenGVLab/InternVL3_5-2B-HF"}),
    "internvl35-1b": ("fvp.models.internvl", "InternVL", {"model_id": "OpenGVLab/InternVL3_5-1B-HF"}),
    # --- larger and other models for a 40-80 GB GPU (see README "Running on the VM"); not run on the laptop ---
    "internvl35-8b": ("fvp.models.internvl", "InternVL", {"model_id": "OpenGVLab/InternVL3_5-8B-HF"}),
    "qwen3vl-32b": ("fvp.models.qwen3vl", "Qwen3VL", {"model_id": "Qwen/Qwen3-VL-32B-Instruct", "device_map": "auto"}),
    # MoE flagship (471 GB bf16, 22B active): one 8-GPU H200 node on the cluster, weights split evenly over the cards
    "qwen3vl-235b": ("fvp.models.qwen3vl", "Qwen3VL", {"model_id": "Qwen/Qwen3-VL-235B-A22B-Instruct", "device_map": "balanced"}),
    # 32B on a 24 GB card: nf4 language model (about 20 GB), vision tower bf16, same image cap as the laptop 4-bit runs
    "qwen3vl-32b-4bit": ("fvp.models.qwen3vl", "Qwen3VL", {"model_id": "Qwen/Qwen3-VL-32B-Instruct", "quantization": "nf4", "max_pixels": 640 * 32 * 32}),
    "internvl35-38b": ("fvp.models.internvl", "InternVL", {"model_id": "OpenGVLab/InternVL3_5-38B-HF", "device_map": "auto"}),
    "molmo-7b-d": ("fvp.models.molmo", "Molmo", {"model_id": "allenai/Molmo-7B-D-0924"}),            # points
    "paligemma2-10b": ("fvp.models.paligemma", "PaliGemma", {"model_id": "google/paligemma2-10b-mix-448"}),  # gated
    "florence2-large": ("fvp.models.florence", "Florence2", {"model_id": "florence-community/Florence-2-large"}),  # pointing only, native class
    "gemma3-12b": ("fvp.models.gemma3", "Gemma3", {"model_id": "google/gemma-3-12b-it"}),             # foil only, gated
}


def load_model(name: str, **overrides):
    import importlib

    if name not in REGISTRY:
        raise KeyError(f"unknown model {name!r}; known: {sorted(REGISTRY)}")
    module, cls, kwargs = REGISTRY[name]
    kwargs = {**kwargs, **overrides}
    return getattr(importlib.import_module(module), cls)(**kwargs)
