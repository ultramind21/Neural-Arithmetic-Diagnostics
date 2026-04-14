from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[2]
P11_RESULTS = ROOT / "project_11" / "results"

SYSTEM_PATH = P11_RESULTS / "transfer_t4_system.json"
HOLDOUT_PATH = P11_RESULTS / "phase_c3_sat_margin" / "holdout_points.json"

OUT_DIR = P11_RESULTS / "phase_d_soft_clamp"
REPORT_MD = OUT_DIR / "report.md"
ARTIFACT_JSON = OUT_DIR / "artifact.json"
SOFT_SYS_PATH = OUT_DIR / "system_soft_clamp.json"

LABELS = ["family-aware region", "transition region", "universal region"]

H_MIN, H_MAX = 0.0010, 0.0200
P_MIN, P_MAX = 0.2600, 0.4200

K_SOFT = 15  # LOCKED


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def save_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def softplus(z: float) -> float:
    # numerically stable softplus
    if z > 30.0:
        return z
    return math.log1p(math.exp(z))


def soft_clamp(x: float, k: float) -> float:
    # smooth approx to clamp01 on [0,1]
    y = softplus(k * x) / k - softplus(k * (x - 1.0)) / k
    # safety clip only (for tiny numerical excursions)
    return max(0.0, min(1.0, y))


def confusion_counts(y_true: List[str], y_pred: List[str]) -> Dict[str, Dict[str, int]]:
    cm = {t: {p: 0 for p in LABELS} for t in LABELS}
    for t, p in zip(y_true, y_pred):
        cm[t][p] += 1
    return cm


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


def ground_truth(system: dict, H: float, P: float, clamp_mode: str) -> str:
    thr = system["thresholds"]
    margin = float(thr["per_family_margin"])
    fam_gap_gt = float(thr["region_family_aware_gap_gt"])
    uni_gap_lt = float(thr["region_universal_gap_lt"])
    fam_wins_ge = int(thr["region_family_aware_wins_ge"])
    uni_wins_ge = int(thr["region_universal_wins_ge"])

    uni_wins = 0
    fam_wins = 0

    uni_scores = []
    fam_scores = []

    for f in system["families"]:
        base = float(f["base_global"])
        sf = float(f["shared_failure"])

        uni_raw = base + P * sf
        fam_raw = base + 0.30 * sf + 0.80 * H

        if clamp_mode == "hard":
            uni = clamp01(uni_raw)
            fam = clamp01(fam_raw)
        elif clamp_mode == "soft":
            uni = soft_clamp(uni_raw, K_SOFT)
            fam = soft_clamp(fam_raw, K_SOFT)
        else:
            raise ValueError("clamp_mode must be 'hard' or 'soft'")

        if uni > fam + margin:
            uni_wins += 1
        elif fam > uni + margin:
            fam_wins += 1

        uni_scores.append(uni)
        fam_scores.append(fam)

    gap = (sum(fam_scores) / len(fam_scores)) - (sum(uni_scores) / len(uni_scores))

    if (fam_wins >= fam_wins_ge) and (gap > fam_gap_gt):
        return "family-aware region"
    if (uni_wins >= uni_wins_ge) or (gap < uni_gap_lt):
        return "universal region"
    return "transition region"


def v3_predict(system: dict, H: float, P: float, margin: float = 0.005, gap_fam: float = 0.005, gap_uni: float = -0.003) -> str:
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


def v3_1_sat_margin(system: dict, H: float, P: float) -> str:
    sat_risk = 0
    for f in system["families"]:
        base = float(f["base_global"])
        sf = float(f["shared_failure"])
        if (base + P * sf >= 1.0) or (base + 0.30 * sf + 0.80 * H >= 1.0):
            sat_risk += 1

    if sat_risk >= 1:
        return v3_predict(system, H, P, margin=0.0065, gap_fam=0.0065, gap_uni=-0.0045)
    return v3_predict(system, H, P, margin=0.005, gap_fam=0.005, gap_uni=-0.003)


def subset_mask(kinds: List[str], which: str) -> List[bool]:
    return [k == which for k in kinds]


def main():
    system = load_json(SYSTEM_PATH)
    holdout = load_json(HOLDOUT_PATH)
    points = holdout["points"]
    kinds = [pt.get("kind", "unknown") for pt in points]

    # Soft ground truth labels for evaluation
    y_soft = [ground_truth(system, float(pt["H"]), float(pt["P"]), "soft") for pt in points]
    # Hard labels for diagnostics only
    y_hard = [ground_truth(system, float(pt["H"]), float(pt["P"]), "hard") for pt in points]

    # Label shift diagnostic
    shift = sum(1 for a, b in zip(y_hard, y_soft) if a != b)
    shift_rate = shift / max(1, len(points))

    # Predictors
    y_v3 = [v3_predict(system, float(pt["H"]), float(pt["P"])) for pt in points]
    y_v31 = [v3_1_sat_margin(system, float(pt["H"]), float(pt["P"])) for pt in points]

    # NN11 labeled by SOFT ground truth
    H_vals_11 = linspace(H_MIN, H_MAX, 11)
    P_vals_11 = linspace(P_MIN, P_MAX, 11)
    grid_11 = [(H, P, ground_truth(system, H, P, "soft")) for H in H_vals_11 for P in P_vals_11]
    y_nn = [nn_label(float(pt["H"]), float(pt["P"]), grid_11) for pt in points]

    def metrics(y_true: List[str], y_pred: List[str]) -> dict:
        return {
            "accuracy": accuracy(y_true, y_pred),
            "macro_f1": macro_f1(y_true, y_pred),
            "confusion": confusion_counts(y_true, y_pred),
        }

    overall = {
        "v3": metrics(y_soft, y_v3),
        "v31": metrics(y_soft, y_v31),
        "nn11": metrics(y_soft, y_nn),
        "label_shift_hard_to_soft": {"count": shift, "rate": shift_rate}
    }

    mask_u = subset_mask(kinds, "uniform")
    mask_b = subset_mask(kinds, "boundary")

    def sub(m: List[bool], y_pred: List[str]) -> dict:
        yt = [t for t, mm in zip(y_soft, m) if mm]
        yp = [p for p, mm in zip(y_pred, m) if mm]
        return {"n": len(yt), "accuracy": accuracy(yt, yp), "macro_f1": macro_f1(yt, yp)}

    subsets = {
        "uniform": {
            "v3": sub(mask_u, y_v3),
            "v31": sub(mask_u, y_v31),
            "nn11": sub(mask_u, y_nn),
        },
        "boundary": {
            "v3": sub(mask_b, y_v3),
            "v31": sub(mask_b, y_v31),
            "nn11": sub(mask_b, y_nn),
        }
    }

    artifact = {
        "test": "phase_d_soft_clamp",
        "k_soft": K_SOFT,
        "n_points": len(points),
        "overall": overall,
        "subsets": subsets
    }

    save_json(ARTIFACT_JSON, artifact)

    # Report
    lines = []
    lines.append("# PROJECT 11 — PHASE D REPORT (Soft-Clamp ground truth)")
    lines.append("")
    lines.append(f"- points: {len(points)} (reusing locked C3 holdout)")
    lines.append(f"- soft clamp k: {K_SOFT}")
    lines.append("")
    ls = overall["label_shift_hard_to_soft"]
    lines.append(f"- label shift hard→soft: {ls['count']} / {len(points)} = {ls['rate']:.4f}")
    lines.append("")
    lines.append("## Overall (evaluated vs SOFT labels)")
    lines.append(f"- V3: acc={overall['v3']['accuracy']:.4f} | macro-F1={overall['v3']['macro_f1']:.4f}")
    lines.append(f"- V3.1: acc={overall['v31']['accuracy']:.4f} | macro-F1={overall['v31']['macro_f1']:.4f}")
    lines.append(f"- NN11: acc={overall['nn11']['accuracy']:.4f} | macro-F1={overall['nn11']['macro_f1']:.4f}")
    lines.append("")
    lines.append("## Subsets (evaluated vs SOFT labels)")
    for name in ["uniform", "boundary"]:
        lines.append(f"- {name}:")
        lines.append(f"  - V3:    n={subsets[name]['v3']['n']} | acc={subsets[name]['v3']['accuracy']:.4f} | macro-F1={subsets[name]['v3']['macro_f1']:.4f}")
        lines.append(f"  - V3.1:  n={subsets[name]['v31']['n']} | acc={subsets[name]['v31']['accuracy']:.4f} | macro-F1={subsets[name]['v31']['macro_f1']:.4f}")
        lines.append(f"  - NN11:  n={subsets[name]['nn11']['n']} | acc={subsets[name]['nn11']['accuracy']:.4f} | macro-F1={subsets[name]['nn11']['macro_f1']:.4f}")

    lines.append("")
    lines.append("Artifacts:")
    lines.append(f"- `{ARTIFACT_JSON.as_posix()}`")
    save_text(REPORT_MD, "\n".join(lines))

    print("\n=== PHASE D SOFT-CLAMP EVALUATION COMPLETE ===")
    print(f"Report: {REPORT_MD}")
    print(f"Artifact: {ARTIFACT_JSON}\n")


if __name__ == "__main__":
    main()
