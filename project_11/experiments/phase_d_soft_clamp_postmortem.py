from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
P11_RESULTS = ROOT / "project_11" / "results"

# Full system config (has thresholds and families)
SYSTEM_PATH = P11_RESULTS / "transfer_t4_system.json"
# Soft clamp meta config (has k value)
SOFT_META_PATH = P11_RESULTS / "phase_d_soft_clamp" / "system_soft_clamp.json"
# Holdout points
HOLDOUT_PATH = P11_RESULTS / "phase_c3_sat_margin" / "holdout_points.json"

OUT_DIR = P11_RESULTS / "phase_d_soft_clamp"
OUT_TXT = OUT_DIR / "postmortem.txt"

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


def confusion_counts(y_true: List[str], y_pred: List[str]) -> Dict[str, Dict[str, int]]:
    cm = {t: {p: 0 for p in LABELS} for t in LABELS}
    for t, p in zip(y_true, y_pred):
        cm[t][p] += 1
    return cm


def dist_counts(y: List[str]) -> Dict[str, int]:
    out = {k: 0 for k in LABELS}
    for v in y:
        out[v] += 1
    return out


def accuracy(y_true: List[str], y_pred: List[str]) -> float:
    return sum(1 for t, p in zip(y_true, y_pred) if t == p) / max(1, len(y_true))


def macro_f1(y_true: List[str], y_pred: List[str]) -> float:
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
    # Stable-ish soft clamp using logistic-based smoothing:
    # maps R -> (0,1) but behaves like clamp around [0,1] when k is large
    # NOTE: This must match what Phase D evaluator used. We read k from system config.
    import math
    # two sigmoids to approximate rectangular window integration:
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


def v3_predict(H: float, P: float, sfs: List[float], margin=0.005, gap_fam=0.005, gap_uni=-0.003) -> str:
    deltas = [0.80 * H + (0.30 - P) * sf for sf in sfs]
    gap_est = sum(deltas) / len(deltas)
    fam_wins_est = sum(1 for d in deltas if d > margin)
    uni_wins_est = sum(1 for d in deltas if d < -margin)

    if (fam_wins_est >= 3) and (gap_est > gap_fam):
        return "family-aware region"
    if (uni_wins_est >= 2) or (gap_est < gap_uni):
        return "universal region"
    return "transition region"


def v31_predict(system: dict, H: float, P: float) -> str:
    # mimic earlier V3.1 concept: saturation-aware expanded margins
    sat = 0
    for f in system["families"]:
        base = float(f["base_global"])
        sf = float(f["shared_failure"])
        if (base + P * sf >= 1.0) or (base + 0.30 * sf + 0.80 * H >= 1.0):
            sat += 1

    sfs = [float(f["shared_failure"]) for f in system["families"]]
    if sat >= 1:
        return v3_predict(H, P, sfs, margin=0.0065, gap_fam=0.0065, gap_uni=-0.0045)
    return v3_predict(H, P, sfs, margin=0.005, gap_fam=0.005, gap_uni=-0.003)


def main():
    system = load_json(SYSTEM_PATH)
    soft_meta = load_json(SOFT_META_PATH)
    k_soft = float(soft_meta["soft_clamp"]["k"])
    
    holdout = load_json(HOLDOUT_PATH)
    pts = holdout["points"]

    # build NN11 grid labeled by SOFT ground truth
    H_vals_11 = linspace(H_MIN, H_MAX, 11)
    P_vals_11 = linspace(P_MIN, P_MAX, 11)
    grid_11 = [(H, P, ground_truth_soft(system, H, P, k_soft)) for H in H_vals_11 for P in P_vals_11]

    y_true = []
    y_v3 = []
    y_v31 = []
    y_nn = []
    kinds = []

    sfs = [float(f["shared_failure"]) for f in system["families"]]

    for pt in pts:
        H = float(pt["H"])
        P = float(pt["P"])
        kinds.append(pt.get("kind", "unknown"))

        t = ground_truth_soft(system, H, P, k_soft)
        y_true.append(t)

        y_v3.append(v3_predict(H, P, sfs))
        y_v31.append(v31_predict(system, H, P))
        y_nn.append(nn_label(H, P, grid_11))

    def subset(mask):
        yt = [t for t, m in zip(y_true, mask) if m]
        a = {
            "n": len(yt),
            "v3": {"acc": accuracy(yt, [p for p, m in zip(y_v3, mask) if m]), "f1": macro_f1(yt, [p for p, m in zip(y_v3, mask) if m])},
            "v31": {"acc": accuracy(yt, [p for p, m in zip(y_v31, mask) if m]), "f1": macro_f1(yt, [p for p, m in zip(y_v31, mask) if m])},
            "nn11": {"acc": accuracy(yt, [p for p, m in zip(y_nn, mask) if m]), "f1": macro_f1(yt, [p for p, m in zip(y_nn, mask) if m])},
            "true_dist": dist_counts(yt),
            "nn_dist": dist_counts([p for p, m in zip(y_nn, mask) if m]),
        }
        return a

    mask_u = [k == "uniform" for k in kinds]
    mask_b = [k == "boundary" for k in kinds]

    lines = []
    lines.append("=== PHASE D POSTMORTEM (soft labels) ===")
    lines.append(f"points: {len(pts)}")
    lines.append("")
    lines.append(f"overall true dist: {dist_counts(y_true)}")
    lines.append(f"overall nn pred dist: {dist_counts(y_nn)}")
    lines.append("")
    lines.append(f"overall V3   acc={accuracy(y_true,y_v3):.4f} f1={macro_f1(y_true,y_v3):.4f}")
    lines.append(f"overall V3.1 acc={accuracy(y_true,y_v31):.4f} f1={macro_f1(y_true,y_v31):.4f}")
    lines.append(f"overall NN11 acc={accuracy(y_true,y_nn):.4f} f1={macro_f1(y_true,y_nn):.4f}")
    lines.append("")
    lines.append("confusion NN11:")
    lines.append(json.dumps(confusion_counts(y_true, y_nn), indent=2))
    lines.append("")
    lines.append("subset uniform:")
    lines.append(json.dumps(subset(mask_u), indent=2))
    lines.append("")
    lines.append("subset boundary:")
    lines.append(json.dumps(subset(mask_b), indent=2))
    lines.append("")

    out = "\n".join(lines)
    save_text(OUT_TXT, out)
    print(out)
    print(f"\nSaved: {OUT_TXT}\n")


if __name__ == "__main__":
    main()
