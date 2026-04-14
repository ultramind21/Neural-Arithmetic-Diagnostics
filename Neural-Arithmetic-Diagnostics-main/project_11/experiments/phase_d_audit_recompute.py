from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
R = ROOT / "project_11" / "results"

# Sources
SYSTEM_SOFT_PATH = R / "phase_d_soft_clamp" / "system_soft_clamp.json"
SYSTEM_HARD_PATH = R / "transfer_t4_system.json"
HOLDOUT_PATH = R / "phase_c3_sat_margin" / "holdout_points.json"

# Output
OUT_DIR = R / "phase_d_soft_clamp"
OUT_MD = OUT_DIR / "AUDIT_RECOMPUTE_REPORT.md"

LABELS = ["family-aware region", "transition region", "universal region"]
H_MIN, H_MAX = 0.0010, 0.0200
P_MIN, P_MAX = 0.2600, 0.4200


def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def save_text(p: Path, s: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")


def clip(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def clamp01(x: float) -> float:
    return clip(x, 0.0, 1.0)


def softplus(x: float) -> float:
    # stable-ish softplus
    import math
    if x > 50:
        return x
    return math.log1p(math.exp(x))


def soft_clamp_softplus(x: float, k: float) -> float:
    # smooth approximation of clamp01:
    # softplus(kx)/k - softplus(k(x-1))/k
    return clamp01(softplus(k * x) / k - softplus(k * (x - 1.0)) / k)


def confusion_counts(y_true: List[str], y_pred: List[str]) -> Dict[str, Dict[str, int]]:
    cm = {t: {p: 0 for p in LABELS} for t in LABELS}
    for t, p in zip(y_true, y_pred):
        cm[t][p] += 1
    return cm


def dist_counts(y: List[str]) -> Dict[str, int]:
    d = {k: 0 for k in LABELS}
    for v in y:
        d[v] += 1
    return d


def accuracy(y_true: List[str], y_pred: List[str]) -> float:
    return sum(1 for t, p in zip(y_true, y_pred) if t == p) / max(1, len(y_true))


def macro_f1_fixed3(y_true: List[str], y_pred: List[str]) -> float:
    # macro-F1 over all 3 labels, even if a label has 0 support (then its F1=0)
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


def macro_f1_present(y_true: List[str], y_pred: List[str]) -> float:
    # macro-F1 only over labels that appear in y_true (support>0)
    supports = dist_counts(y_true)
    present = [k for k, v in supports.items() if v > 0]
    if not present:
        return 0.0

    f1s = []
    for lbl in present:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == lbl and p == lbl)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != lbl and p == lbl)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == lbl and p != lbl)

        prec = tp / (tp + fp) if (tp + fp) else 0.0
        rec = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) else 0.0
        f1s.append(f1)

    return sum(f1s) / len(f1s)


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


def linspace(a: float, b: float, n: int) -> List[float]:
    step = (b - a) / (n - 1)
    return [a + i * step for i in range(n)]


def merge_system(hard: dict, soft: dict) -> dict:
    # We require families + thresholds from hard system, and soft_clamp config from soft system.
    out = {}
    out["families"] = hard.get("families", [])
    out["thresholds"] = hard.get("thresholds", hard.get("threshold", {}))
    out["soft_clamp"] = soft.get("soft_clamp", soft.get("soft", {"k": 15}))
    return out


def ground_truth(system: dict, H: float, P: float, use_soft: bool) -> str:
    thr = system["thresholds"]
    margin = float(thr["per_family_margin"])
    fam_gap_gt = float(thr["region_family_aware_gap_gt"])
    uni_gap_lt = float(thr["region_universal_gap_lt"])
    fam_wins_ge = int(thr["region_family_aware_wins_ge"])
    uni_wins_ge = int(thr["region_universal_wins_ge"])

    if use_soft:
        k = float(system["soft_clamp"]["k"])

    universal_wins = 0
    family_aware_wins = 0
    uni_scores = []
    fam_scores = []

    for f in system["families"]:
        base = float(f["base_global"])
        sf = float(f["shared_failure"])

        uni_raw = base + P * sf
        fam_raw = base + 0.30 * sf + 0.80 * H

        if use_soft:
            uni = soft_clamp_softplus(uni_raw, k)
            fam = soft_clamp_softplus(fam_raw, k)
        else:
            uni = clamp01(uni_raw)
            fam = clamp01(fam_raw)

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


def v3_predict(system: dict, H: float, P: float, margin=0.005, gap_fam=0.005, gap_uni=-0.003) -> str:
    sfs = [float(f["shared_failure"]) for f in system["families"]]
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
    # saturation-aware margins (same as C3)
    sat_risk = 0
    for f in system["families"]:
        base = float(f["base_global"])
        sf = float(f["shared_failure"])
        if (base + P * sf >= 1.0) or (base + 0.30 * sf + 0.80 * H >= 1.0):
            sat_risk += 1

    if sat_risk >= 1:
        return v3_predict(system, H, P, margin=0.0065, gap_fam=0.0065, gap_uni=-0.0045)
    return v3_predict(system, H, P, margin=0.005, gap_fam=0.005, gap_uni=-0.003)


def eval_block(name: str, y_true: List[str], y_pred: List[str]) -> Dict:
    return {
        "acc": accuracy(y_true, y_pred),
        "macro_f1_fixed3": macro_f1_fixed3(y_true, y_pred),
        "macro_f1_present": macro_f1_present(y_true, y_pred),
        "pred_dist": dist_counts(y_pred),
    }


def main():
    hard_sys = load_json(SYSTEM_HARD_PATH)
    soft_sys = load_json(SYSTEM_SOFT_PATH)
    system = merge_system(hard_sys, soft_sys)

    holdout = load_json(HOLDOUT_PATH)
    pts = holdout["points"]
    kinds = [pt.get("kind", "unknown") for pt in pts]
    mask_u = [k == "uniform" for k in kinds]
    mask_b = [k == "boundary" for k in kinds]

    HP = [(float(pt["H"]), float(pt["P"])) for pt in pts]

    # labels
    y_true_soft = [ground_truth(system, H, P, use_soft=True) for (H, P) in HP]
    y_true_hard = [ground_truth(system, H, P, use_soft=False) for (H, P) in HP]
    label_shift = sum(1 for a, b in zip(y_true_hard, y_true_soft) if a != b)

    # predictors (same predictions regardless of label type)
    y_v3 = [v3_predict(system, H, P) for (H, P) in HP]
    y_v31 = [v31_predict(system, H, P) for (H, P) in HP]

    # NN grids labeled by SOFT ground truth
    def nn_preds(n: int) -> List[str]:
        Hs = linspace(H_MIN, H_MAX, n)
        Ps = linspace(P_MIN, P_MAX, n)
        grid = [(H, P, ground_truth(system, H, P, use_soft=True)) for H in Hs for P in Ps]
        return [nn_label(H, P, grid) for (H, P) in HP]

    y_nn11 = nn_preds(11)
    y_nn21 = nn_preds(21)
    y_nn41 = nn_preds(41)

    # overall eval vs soft labels
    out = []
    out.append("# PHASE D AUDIT — RECOMPUTE (softplus-based soft clamp)")
    out.append("")
    out.append(f"- points: {len(pts)}")
    out.append(f"- k (soft clamp): {system['soft_clamp'].get('k', 'unknown')}")
    out.append(f"- label shift hard→soft: {label_shift} / {len(pts)} = {label_shift/len(pts):.4f}")
    out.append("")
    out.append("## True label distribution (SOFT)")
    out.append(f"- {dist_counts(y_true_soft)}")
    out.append("")
    out.append("## Overall metrics (vs SOFT labels)")
    for name, y in [
        ("V3", y_v3),
        ("V3.1", y_v31),
        ("NN11", y_nn11),
        ("NN21", y_nn21),
        ("NN41", y_nn41),
    ]:
        m = eval_block(name, y_true_soft, y)
        out.append(f"- {name}: acc={m['acc']:.4f} | macroF1_fixed3={m['macro_f1_fixed3']:.4f} | macroF1_present={m['macro_f1_present']:.4f} | pred_dist={m['pred_dist']}")

    out.append("")
    out.append("## Subsets (vs SOFT labels) — macroF1_fixed3")
    def subset(mask):
        yt = [t for t, m in zip(y_true_soft, mask) if m]
        return {
            "n": len(yt),
            "V3": macro_f1_fixed3(yt, [p for p, m in zip(y_v3, mask) if m]),
            "V3.1": macro_f1_fixed3(yt, [p for p, m in zip(y_v31, mask) if m]),
            "NN11": macro_f1_fixed3(yt, [p for p, m in zip(y_nn11, mask) if m]),
            "NN21": macro_f1_fixed3(yt, [p for p, m in zip(y_nn21, mask) if m]),
            "NN41": macro_f1_fixed3(yt, [p for p, m in zip(y_nn41, mask) if m]),
            "true_dist": dist_counts(yt),
        }

    out.append(f"- uniform: {subset(mask_u)}")
    out.append(f"- boundary: {subset(mask_b)}")
    out.append("")
    out.append("## Confusion (NN11 vs SOFT labels)")
    out.append("```json")
    out.append(json.dumps(confusion_counts(y_true_soft, y_nn11), indent=2))
    out.append("```")

    text = "\n".join(out)
    save_text(OUT_MD, text)
    print(text)
    print(f"\nSaved: {OUT_MD}\n")


if __name__ == "__main__":
    main()
