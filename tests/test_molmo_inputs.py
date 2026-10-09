import torch

from fvp.models.molmo import Molmo


class _Processor:
    """Stand-in for Molmo's processor: it returns float32 image tensors whatever dtype the model runs in."""

    def process(self, images, text):
        if images is not None and len(images) == 0:  # what allenai/Molmo-7B-D-0924 does with images=[]
            raise ValueError("need at least one array to concatenate")
        # the real processor returns int32 ids for text-only prompts and int64 ids when an image is present
        out = {"input_ids": torch.tensor([1, 2, 3], dtype=torch.int64 if images else torch.int32)}
        if images:
            out["images"] = torch.zeros(2, 4, dtype=torch.float32)
            out["image_masks"] = torch.ones(2, 4, dtype=torch.float32)
            out["image_input_idx"] = torch.zeros(2, 4, dtype=torch.long)
        return out


class _Model:
    device = torch.device("cpu")
    dtype = torch.bfloat16


def _wrapper():
    m = Molmo.__new__(Molmo)  # skip the weight download; only _inputs is under test
    m.processor = _Processor()
    m.model = _Model()
    m.dtype = torch.bfloat16
    return m


def test_molmo_inputs_cast_float_tensors_to_model_dtype():
    out = _wrapper()._inputs(object(), "Point to the dog.")
    assert out["images"].dtype == torch.bfloat16
    assert out["image_masks"].dtype == torch.bfloat16
    assert out["image_input_idx"].dtype == torch.long
    assert out["input_ids"].dtype == torch.long
    assert out["input_ids"].shape == (1, 3)  # the batch dimension is still added


def test_molmo_inputs_text_only_has_no_image_keys():
    out = _wrapper()._inputs(None, "Is the sky blue?")
    assert set(out) == {"input_ids"}
    assert out["input_ids"].shape == (1, 3)
    assert out["input_ids"].dtype == torch.long  # generation appends int64 tokens to the ids
