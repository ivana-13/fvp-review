import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from analyze import boot_ci, ci_pct, kappa, stat_cond, stat_kappa, stat_rate  # noqa: E402


def test_constant_sample_has_degenerate_interval():
    assert boot_ci([1.0] * 50, stat_rate) == (1.0, 1.0)


def test_rate_interval_covers_sample_mean_and_narrows_with_n():
    rng = random.Random(0)
    small = [float(rng.random() < 0.3) for _ in range(100)]
    large = [float(rng.random() < 0.3) for _ in range(4000)]
    lo_s, hi_s = boot_ci(small, stat_rate, n_boot=500)
    lo_l, hi_l = boot_ci(large, stat_rate, n_boot=500)
    assert lo_s <= sum(small) / len(small) <= hi_s
    assert lo_l <= sum(large) / len(large) <= hi_l
    assert (hi_l - lo_l) < (hi_s - lo_s)


def test_conditional_and_kappa_statistics():
    import numpy as np

    rows = np.array([[1, 1], [1, 0], [1, 1], [0, 1], [0, 0]], dtype=float)
    assert abs(stat_cond(rows) - 2 / 3) < 1e-9
    a = [True, True, False, False, True]
    b = [True, False, False, True, True]
    assert abs(stat_kappa(np.array(list(zip(a, b)), dtype=float)) - kappa(a, b)) < 1e-9
    assert stat_kappa(np.array([[1, 1], [0, 0], [1, 1]], dtype=float)) == 1.0


def test_ci_pct_format_and_empty():
    assert ci_pct([], stat_rate) == "--"
    s = ci_pct([1.0, 0.0, 1.0, 1.0], stat_rate)
    assert s.startswith("[") and s.endswith("]") and "," in s
