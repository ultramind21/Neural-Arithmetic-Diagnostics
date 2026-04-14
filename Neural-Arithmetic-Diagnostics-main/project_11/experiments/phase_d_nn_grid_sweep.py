from __future__ import annotations

import json
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parents[2]
P11_RESULTS = ROOT / "project_11" / "results"

SYSTEM_PATH = P11_RESULTS / "transfer_t4_system.json"
SOFT_META_PATH = P11_RESULTS / "phase_d_soft_clamp" / "system_soft_clamp.json"
HOLDOUT_PATH = P11_RESULTS / "phase_c3_sat_margin" / "holdout_points.json"
OUT_DIR = P11_RESULTS / "phase_d_soft_clamp"
OUT_MD = OUT_DIR / "nn_grid_sweep.md"

LABELS = ["family-aware region", "transition region", "universal region"]

H_MIN, H_MAX = 0.0010, 0.0200
P_MIN, P_MAX = 0.2600, 0.4200


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def clip(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def normalized_distance(aH: float, aP: float, bH: float, bP: float) -> float:
    H_range = 0.015 - 0.003
    P_range = 0.42 - 0.30
    return (((aH - bH) / H_range) ** 2 + ((aP - bP) / P_range) ** 2) ** 0.5


def nn_label(H: float, P: float, grid: List[Tuple[float, float, str]]) -> str:
    best_lbl, best_d = None, None
    for gH, gP, glbl in grid:
        d = normalized_distance(H, P, gH, gP)
        if best_d is None or d < best_d:
            best_d, best_lbl = d, glbl
    return best_lbl


def accuracy(y_true, y_pred) -> float:
    return sum(1 for t, p in zip(y_true, y_pred) if t == p) / max(1, len(y_true))


def macro_f1(y_true, y_pred) -> float:
    f1s = []
    for lbl in LABELS:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == lbl and p == lbl)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != lbl and p == lbl)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == lbl and p != lbl)
        prec = tp / (tp + fp) if (tp + fp) else 0.0
        rec = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) else 0.0
        f1s.append(f1)
    return sum(f1s) / len(f1s)


def linspace(a: float, b: float, n: int) -> List[float]:
    step = (b - a) / (n - 1)
    return [a + i * step for i in range(n)]


def soft_clamp(x: float, k: float) -> float:
    import math
    s1 = 1.0 / (1.0 + math.exp(-k * x))
    s2 = 1.0 / (1.0 + math.exp(-k * (x - 1.0)))
    return clip(s1 - s2, 0.0, 1.0)


def ground_truth_soft(system: dict, H: float, P: float, k: float) -> str:
    thr = system["thresholds"]

    margin = float(thr["per_family_margin"])
    fam_gap_gt = float(thr["region_family_aware_gap_gt"])
    uni_gap_lt = float(thr["region_universal_gap_lt"])
    fam_wins_ge = int(thr["region_family_aware_wins_ge"])
    uni_wins_ge = int(thr["region_universal_wins_ge"])

    universal_wins = 0
    family_aware_wins = 0
    uni_scores = []
    fam_scores = []

    for f in system["families"]:
        base = float(f["base_global"])
        sf = float(f["shared_failure"])

        uni = soft_clamp(base + P * sf, k)
        fam = soft_clamp(base + 0.30 * sf + 0.80 * H, k)

        if uni > fam + margin:
            universal_wins += 1
        elif fam > uni + margin:
            family_aware_wins += 1

        uni_scores.append(uni)
        fam_scores.append(fam)

    gap = (sum(fam_scores) / len(fam_scores)) - (sum(uni_scores) / len(uni_scores))

    if (family_aware_wins >= fam_wins_ge) and (gap > fam_gap_gt):
        return "family-aware region"
    if (universal_wins >= uni_wins_ge) or (gap < uni_gap_lt):
        return "universal region"
    return "transition region"


def main():
    system = load_json(SYSTEM_PATH)
    soft_meta = load_json(SOFT_META_PATH)
    k_soft = float(soft_meta["soft_clamp"]["k"])
    
    holdout = load_json(HOLDOUT_PATH)
    pts = holdout["points"]

    y_true = [ground_truth_soft(system, float(pt["H"]), float(pt["P"]), k_soft) for pt in pts]

    lines = []
    lines.append("# PHASE D — NN GRID RESOLUTION SWEEP (soft labels)")
    lines.append("")
    lines.append(f"- points: {len(pts)}")
    lines.append(f"- k: {k_soft}")
    lines.append("")
    lines.append("| grid | NN acc | NN macro-F1 |")
    lines.append("|---:|---:|---:|")

    for n in [11, 21, 41]:
        Hs = linspace(H_MIN, H_MAX, n)
        Ps = linspace(P_MIN, P_MAX, n)
        grid = [(H, P, ground_truth_soft(system, H, P, k_soft)) for H in Hs for P in Ps]

        y_pred = [nn_label(float(pt["H"]), float(pt["P"]), grid) for pt in pts]
        lines.append(f"| {n}x{n} | {accuracy(y_true, y_pred):.4f} | {macro_f1(y_true, y_pred):.4f} |")

    out = "\n".join(lines)
    save_text(OUT_MD, out)
    print(out)
    print(f"\nSaved: {OUT_MD}\n")


if __name__ == "__main__":
    main()
