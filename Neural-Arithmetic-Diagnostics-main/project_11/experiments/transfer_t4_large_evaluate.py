from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
P11_RESULTS = ROOT / "project_11" / "results"

SYSTEM_PATH = P11_RESULTS / "transfer_t4_system.json"

IN_DIR = P11_RESULTS / "transfer_t4_large"
HOLDOUT_PATH = IN_DIR / "holdout_points.json"
PRED_PATH = IN_DIR / "predictions.json"
REPORT_MD = IN_DIR / "report.md"
ARTIFACT_JSON = IN_DIR / "artifact.json"

LABELS = ["family-aware region", "transition region", "universal region"]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def save_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


@dataclass
class CellResult:
    region: str
    gap: float
    universal_wins: int
    family_aware_wins: int
    near_ties: int


def ground_truth_region(system: dict, H: float, P: float) -> CellResult:
    fams = system["families"]
    thr = system["thresholds"]

    margin = float(thr["per_family_margin"])
    fam_gap_gt = float(thr["region_family_aware_gap_gt"])
    uni_gap_lt = float(thr["region_universal_gap_lt"])
    fam_wins_ge = int(thr["region_family_aware_wins_ge"])
    uni_wins_ge = int(thr["region_universal_wins_ge"])

    universal_wins = 0
    family_aware_wins = 0
    near_ties = 0

    uni_scores = []
    fam_scores = []

    for f in fams:
        base = float(f["base_global"])
        sf = float(f["shared_failure"])

        uni = clamp(base + P * sf)
        fam = clamp(base + 0.30 * sf + 0.80 * H)

        if uni > fam + margin:
            universal_wins += 1
        elif fam > uni + margin:
            family_aware_wins += 1
        else:
            near_ties += 1

        uni_scores.append(uni)
        fam_scores.append(fam)

    avg_uni = sum(uni_scores) / len(uni_scores)
    avg_fam = sum(fam_scores) / len(fam_scores)
    gap = avg_fam - avg_uni

    if (family_aware_wins >= fam_wins_ge) and (gap > fam_gap_gt):
        region = "family-aware region"
    elif (universal_wins >= uni_wins_ge) or (gap < uni_gap_lt):
        region = "universal region"
    else:
        region = "transition region"

    return CellResult(
        region=region,
        gap=gap,
        universal_wins=universal_wins,
        family_aware_wins=family_aware_wins,
        near_ties=near_ties,
    )


def confusion_counts(y_true: List[str], y_pred: List[str]) -> Dict[str, Dict[str, int]]:
    cm = {t: {p: 0 for p in LABELS} for t in LABELS}
    for t, p in zip(y_true, y_pred):
        cm[t][p] += 1
    return cm


def accuracy(y_true: List[str], y_pred: List[str]) -> float:
    correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    return correct / max(1, len(y_true))


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
    # normalize to Project 10 ranges
    H_range = 0.015 - 0.003  # 0.012
    P_range = 0.42 - 0.30    # 0.12
    return (((aH - bH) / H_range) ** 2 + ((aP - bP) / P_range) ** 2) ** 0.5


def nn_label(H: float, P: float, grid: List[Tuple[float, float, str]]) -> str:
    best_lbl, best_d = None, None
    for gH, gP, glbl in grid:
        d = normalized_distance(H, P, gH, gP)
        if best_d is None or d < best_d:
            best_d, best_lbl = d, glbl
    return best_lbl


def majority_label(grid: List[Tuple[float, float, str]]) -> str:
    counts = {lbl: 0 for lbl in LABELS}
    for _, _, lbl in grid:
        counts[lbl] += 1
    order = ["universal region", "transition region", "family-aware region"]
    return max(order, key=lambda k: counts[k])


def build_grid(system: dict, H_vals: List[float], P_vals: List[float]) -> List[Tuple[float, float, str]]:
    return [(H, P, ground_truth_region(system, H, P).region) for H in H_vals for P in P_vals]


def linspace(a: float, b: float, n: int) -> List[float]:
    if n == 1:
        return [a]
    step = (b - a) / (n - 1)
    return [a + i * step for i in range(n)]


def subset_metrics(y_true_all: List[str], y_pred_all: List[str], mask: List[bool]) -> dict:
    y_t = [t for t, m in zip(y_true_all, mask) if m]
    y_p = [p for p, m in zip(y_pred_all, mask) if m]
    return {
        "n": len(y_t),
        "accuracy": accuracy(y_t, y_p),
        "macro_f1": macro_f1(y_t, y_p),
        "confusion": confusion_counts(y_t, y_p),
    }


def main():
    system = load_json(SYSTEM_PATH)
    holdout = load_json(HOLDOUT_PATH)
    preds = load_json(PRED_PATH)

    points = holdout["points"]
    pred_by_id = {p["id"]: p for p in preds["predictions"]}

    # Baseline grids (11x11 over generation ranges; 3x3 reference)
    H_vals_11 = linspace(0.001, 0.020, 11)
    P_vals_11 = linspace(0.260, 0.420, 11)
    grid_11 = build_grid(system, H_vals_11, P_vals_11)
    maj_11 = majority_label(grid_11)

    H_vals_3 = [0.003, 0.009, 0.015]
    P_vals_3 = [0.30, 0.36, 0.42]
    grid_3 = build_grid(system, H_vals_3, P_vals_3)
    maj_3 = majority_label(grid_3)

    y_true: List[str] = []
    y_pred: List[str] = []

    y_maj11: List[str] = []
    y_nn11: List[str] = []

    y_maj3: List[str] = []
    y_nn3: List[str] = []

    mask_uniform: List[bool] = []
    mask_boundary: List[bool] = []

    # Evaluate all points
    for pt in points:
        pid = pt["id"]
        if pid not in pred_by_id:
            raise SystemExit(f"Missing prediction for id={pid}")

        p = pred_by_id[pid]
        if float(p["H"]) != float(pt["H"]) or float(p["P"]) != float(pt["P"]):
            raise SystemExit(f"H,P mismatch for id={pid}")

        H = float(pt["H"])
        P = float(pt["P"])
        kind = pt.get("kind", "unknown")

        gt = ground_truth_region(system, H, P).region
        pr = p["predicted_region"]

        nn11 = nn_label(H, P, grid_11)
        nn3 = nn_label(H, P, grid_3)

        y_true.append(gt)
        y_pred.append(pr)

        y_maj11.append(maj_11)
        y_nn11.append(nn11)

        y_maj3.append(maj_3)
        y_nn3.append(nn3)

        mask_uniform.append(kind == "uniform")
        mask_boundary.append(kind == "boundary")

    # Metrics
    m_model = {
        "accuracy": accuracy(y_true, y_pred),
        "macro_f1": macro_f1(y_true, y_pred),
        "confusion": confusion_counts(y_true, y_pred),
    }
    m_maj11 = {"accuracy": accuracy(y_true, y_maj11), "macro_f1": macro_f1(y_true, y_maj11)}
    m_nn11 = {"accuracy": accuracy(y_true, y_nn11), "macro_f1": macro_f1(y_true, y_nn11)}
    m_maj3 = {"accuracy": accuracy(y_true, y_maj3), "macro_f1": macro_f1(y_true, y_maj3)}
    m_nn3 = {"accuracy": accuracy(y_true, y_nn3), "macro_f1": macro_f1(y_true, y_nn3)}

    best_baseline_f1 = max(m_maj11["macro_f1"], m_nn11["macro_f1"], m_maj3["macro_f1"], m_nn3["macro_f1"])
    passed = (m_model["macro_f1"] >= best_baseline_f1 + 0.10) and (m_model["macro_f1"] >= 0.80)

    sub_uniform = subset_metrics(y_true, y_pred, mask_uniform)
    sub_boundary = subset_metrics(y_true, y_pred, mask_boundary)

    metrics = {
        "model": m_model,
        "baseline_majority_11x11": {"label": maj_11, **m_maj11},
        "baseline_nn_11x11": m_nn11,
        "baseline_majority_3x3_reference": {"label": maj_3, **m_maj3},
        "baseline_nn_3x3_reference": m_nn3,
    }

    artifact = {
        "test": "transfer_t4_large_rule_v3",
        "n_total": len(points),
        "subset": {"uniform": sub_uniform, "boundary": sub_boundary},
        "metrics": metrics,
        "best_baseline_macro_f1": best_baseline_f1,
        "pass_condition": {
            "required": "macro-F1 >= best_baseline + 0.10 AND macro-F1 >= 0.80",
            "passed": bool(passed),
        },
    }

    save_json(ARTIFACT_JSON, artifact)

    # Report
    lines = []
    lines.append("# PROJECT 11 — TRANSFER T4-LARGE REPORT (Rule V3)")
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- points: {len(points)}")
    lines.append(f"- model accuracy: {metrics['model']['accuracy']:.4f}")
    lines.append(f"- model macro-F1: {metrics['model']['macro_f1']:.4f}")
    lines.append(f"- best baseline macro-F1: {best_baseline_f1:.4f}")
    lines.append(f"- PASS: {passed}")
    lines.append("")
    lines.append("## Subset performance (by generator kind)")
    lines.append(f"- uniform: n={sub_uniform['n']} | acc={sub_uniform['accuracy']:.4f} | macro-F1={sub_uniform['macro_f1']:.4f}")
    lines.append(f"- boundary: n={sub_boundary['n']} | acc={sub_boundary['accuracy']:.4f} | macro-F1={sub_boundary['macro_f1']:.4f}")
    lines.append("")
    lines.append("## Baselines (macro-F1)")
    lines.append(f"- majority 11x11: {metrics['baseline_majority_11x11']['macro_f1']:.4f} (label={maj_11})")
    lines.append(f"- NN 11x11: {metrics['baseline_nn_11x11']['macro_f1']:.4f}")
    lines.append(f"- majority 3x3: {metrics['baseline_majority_3x3_reference']['macro_f1']:.4f} (label={maj_3})")
    lines.append(f"- NN 3x3: {metrics['baseline_nn_3x3_reference']['macro_f1']:.4f}")
    lines.append("")
    lines.append("Artifacts saved in:")
    lines.append(f"- `{IN_DIR.as_posix()}`")

    save_text(REPORT_MD, "\n".join(lines))

    print("\n=== TRANSFER T4-LARGE RESULT (Rule V3) ===")
    print(f"points: {len(points)}")
    print(f"model accuracy: {metrics['model']['accuracy']:.4f}")
    print(f"model macro-F1: {metrics['model']['macro_f1']:.4f}")
    print(f"best baseline macro-F1: {best_baseline_f1:.4f}")
    print(f"PASS: {passed}")
    print(f"Report: {REPORT_MD}")
    print(f"Artifact: {ARTIFACT_JSON}\n")


if __name__ == "__main__":
    main()