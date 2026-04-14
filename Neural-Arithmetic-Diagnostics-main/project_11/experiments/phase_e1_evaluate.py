from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[2]
R = ROOT / "project_11" / "results"

SYSTEM_HARD_PATH = R / "transfer_t4_system.json"
SYSTEM_SOFT_PATH = R / "phase_d_soft_clamp" / "system_soft_clamp.json"
HOLDOUT_PATH = R / "phase_c3_sat_margin" / "holdout_points.json"
REF_PATH = R / "phase_e1_adaptive_nn" / "reference_points.json"

OUT_DIR = R / "phase_e1_adaptive_nn"
OUT_MD = OUT_DIR / "report.md"
OUT_JSON = OUT_DIR / "artifact.json"

LABELS = ["family-aware region", "transition region", "universal region"]

H_MIN, H_MAX = 0.0010, 0.0200
P_MIN, P_MAX = 0.2600, 0.4200


def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def save_text(p: Path, s: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")


def save_json(p: Path, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def clip(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def clamp01(x: float) -> float:
    return clip(x, 0.0, 1.0)


def softplus(x: float) -> float:
    import math
    if x > 50:
        return x
    return math.log1p(math.exp(x))


def soft_clamp_softplus(x: float, k: float) -> float:
    return clamp01(softplus(k * x) / k - softplus(k * (x - 1.0)) / k)


def dist_counts(y: List[str]) -> Dict[str, int]:
    d = {k: 0 for k in LABELS}
    for v in y:
        d[v] += 1
    return d


def accuracy(y_true: List[str], y_pred: List[str]) -> float:
    return sum(1 for t, p in zip(y_true, y_pred) if t == p) / max(1, len(y_true))


def macro_f1_present(y_true: List[str], y_pred: List[str]) -> float:
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
    return {
        "families": hard["families"],
        "thresholds": hard["thresholds"],
        "soft_clamp": soft.get("soft_clamp", {"k": 15})
    }


def ground_truth_soft(system: dict, H: float, P: float) -> str:
    thr = system["thresholds"]
    k = float(system["soft_clamp"]["k"])

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

        uni = soft_clamp_softplus(base + P * sf, k)
        fam = soft_clamp_softplus(base + 0.30 * sf + 0.80 * H, k)

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
    sat_risk = 0
    for f in system["families"]:
        base = float(f["base_global"])
        sf = float(f["shared_failure"])
        if (base + P * sf >= 1.0) or (base + 0.30 * sf + 0.80 * H >= 1.0):
            sat_risk += 1

    if sat_risk >= 1:
        return v3_predict(system, H, P, margin=0.0065, gap_fam=0.0065, gap_uni=-0.0045)
    return v3_predict(system, H, P, margin=0.005, gap_fam=0.005, gap_uni=-0.003)


def eval_model(name: str, y_true: List[str], y_pred: List[str]) -> dict:
    return {"acc": accuracy(y_true, y_pred), "macro_f1_present": macro_f1_present(y_true, y_pred), "pred_dist": dist_counts(y_pred)}


def main():
    hard = load_json(SYSTEM_HARD_PATH)
    soft = load_json(SYSTEM_SOFT_PATH)
    system = merge_system(hard, soft)

    holdout = load_json(HOLDOUT_PATH)
    pts = holdout["points"]
    kinds = [pt.get("kind", "unknown") for pt in pts]
    mask_u = [k == "uniform" for k in kinds]
    mask_b = [k == "boundary" for k in kinds]

    HP = [(float(pt["H"]), float(pt["P"])) for pt in pts]
    y_true = [ground_truth_soft(system, H, P) for (H, P) in HP]

    # V3.1
    y_v31 = [v31_predict(system, H, P) for (H, P) in HP]

    # adaptive reference set -> label by soft ground truth -> NN
    ref = load_json(REF_PATH)
    ref_pts = [(float(p["H"]), float(p["P"])) for p in ref["points"]]
    ref_lbl = [ground_truth_soft(system, H, P) for (H, P) in ref_pts]
    ref_grid = [(H, P, L) for (H, P), L in zip(ref_pts, ref_lbl)]
    y_nn_adapt = [nn_label(H, P, ref_grid) for (H, P) in HP]

    # NN41 and NN81 grids
    def nn_grid(n: int) -> List[str]:
        Hs = linspace(H_MIN, H_MAX, n)
        Ps = linspace(P_MIN, P_MAX, n)
        grid = [(H, P, ground_truth_soft(system, H, P)) for H in Hs for P in Ps]
        return [nn_label(H, P, grid) for (H, P) in HP]

    t0 = time.time()
    y_nn41 = nn_grid(41)
    t41 = time.time() - t0

    t0 = time.time()
    y_nn81 = nn_grid(81)
    t81 = time.time() - t0

    def subset(y_pred, mask):
        yt = [t for t, m in zip(y_true, mask) if m]
        yp = [p for p, m in zip(y_pred, mask) if m]
        return {"n": len(yt), "acc": accuracy(yt, yp), "macro_f1_present": macro_f1_present(yt, yp)}

    metrics = {
        "true_dist": dist_counts(y_true),
        "V3.1": {
            "overall": eval_model("V3.1", y_true, y_v31),
            "uniform": subset(y_v31, mask_u),
            "boundary": subset(y_v31, mask_b),
        },
        "NN_adaptive_2000": {
            "overall": eval_model("NN_adaptive_2000", y_true, y_nn_adapt),
            "uniform": subset(y_nn_adapt, mask_u),
            "boundary": subset(y_nn_adapt, mask_b),
            "ref_points": len(ref_grid),
        },
        "NN41": {
            "overall": eval_model("NN41", y_true, y_nn41),
            "uniform": subset(y_nn41, mask_u),
            "boundary": subset(y_nn41, mask_b),
            "seconds": t41,
            "grid_points": 41 * 41,
        },
        "NN81": {
            "overall": eval_model("NN81", y_true, y_nn81),
            "uniform": subset(y_nn81, mask_u),
            "boundary": subset(y_nn81, mask_b),
            "seconds": t81,
            "grid_points": 81 * 81,
        },
    }

    save_json(OUT_JSON, {"test": "phase_e1_adaptive_nn", "metrics": metrics})

    lines = []
    lines.append("# PHASE E1 — Adaptive NN Report (soft labels)")
    lines.append("")
    lines.append(f"- holdout points: {len(pts)} (from C3 holdout)")
    lines.append(f"- true dist: {metrics['true_dist']}")
    lines.append("")
    lines.append("## Overall (macro_f1_present)")
    lines.append("| model | acc | macroF1 |")
    lines.append("|---|---:|---:|")
    for name in ["V3.1", "NN_adaptive_2000", "NN41", "NN81"]:
        o = metrics[name]["overall"]
        lines.append(f"| {name} | {o['acc']:.4f} | {o['macro_f1_present']:.4f} |")

    lines.append("")
    lines.append("## Boundary subset (macro_f1_present)")
    lines.append("| model | acc | macroF1 |")
    lines.append("|---|---:|---:|")
    for name in ["V3.1", "NN_adaptive_2000", "NN41", "NN81"]:
        b = metrics[name]["boundary"]
        lines.append(f"| {name} | {b['acc']:.4f} | {b['macro_f1_present']:.4f} |")

    lines.append("")
    lines.append("## Cost")
    lines.append(f"- adaptive ref points: {metrics['NN_adaptive_2000']['ref_points']}")
    lines.append(f"- NN41 grid points: {metrics['NN41']['grid_points']} | seconds={metrics['NN41']['seconds']:.2f}")
    lines.append(f"- NN81 grid points: {metrics['NN81']['grid_points']} | seconds={metrics['NN81']['seconds']:.2f}")
    lines.append("")
    lines.append("Artifact:")
    lines.append(f"- `{OUT_JSON.as_posix()}`")

    save_text(OUT_MD, "\n".join(lines))

    print("\n=== PHASE E1 EVALUATION COMPLETE ===")
    print(f"Report: {OUT_MD}")
    print(f"Artifact: {OUT_JSON}\n")


if __name__ == "__main__":
    main()
