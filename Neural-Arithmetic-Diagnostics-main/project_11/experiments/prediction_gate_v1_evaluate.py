from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


# =============================================================================
# Paths
# =============================================================================
ROOT = Path(__file__).resolve().parents[2]
P11_RESULTS = ROOT / "project_11" / "results"

HOLDOUT_PATH = P11_RESULTS / "prediction_gate_v1_holdout_points.json"
PRED_PATH = P11_RESULTS / "prediction_gate_v1_predictions.json"

REPORT_MD = P11_RESULTS / "prediction_gate_v1_report.md"
ARTIFACT_JSON = P11_RESULTS / "prediction_gate_v1_artifact.json"


# =============================================================================
# Project 10 ground truth (copied from code logic)
# =============================================================================

BASE_CASES = [
    {"family": "A", "base_global": 0.48, "shared_failure": 0.41},
    {"family": "B", "base_global": 0.47, "shared_failure": 0.40},
    {"family": "C", "base_global": 0.46, "shared_failure": 0.41},
    {"family": "D", "base_global": 0.47, "shared_failure": 0.40},
]

RESIDUAL_SIGNS = [1, -1, 1, -1]


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def universal_rescue_score(base_global: float, shared_failure: float, universal_power: float) -> float:
    return clamp(base_global + universal_power * shared_failure)


def family_aware_rescue_score(base_global: float, shared_failure: float, residual_abs: float) -> float:
    return clamp(base_global + 0.30 * shared_failure + 0.80 * residual_abs)


@dataclass
class CellResult:
    H: float
    P: float
    avg_uni: float
    avg_fam: float
    gap: float
    universal_wins: int
    family_aware_wins: int
    near_ties: int
    region: str


def ground_truth_region(residual_abs: float, universal_power: float) -> CellResult:
    rows = []
    universal_wins = 0
    family_aware_wins = 0
    near_ties = 0

    for i, case in enumerate(BASE_CASES):
        residual = RESIDUAL_SIGNS[i] * residual_abs

        uni = universal_rescue_score(case["base_global"], case["shared_failure"], universal_power)
        fam = family_aware_rescue_score(case["base_global"], case["shared_failure"], abs(residual))

        if uni > fam + 0.005:
            universal_wins += 1
        elif fam > uni + 0.005:
            family_aware_wins += 1
        else:
            near_ties += 1

        rows.append((uni, fam))

    avg_uni = sum(u for u, _ in rows) / len(rows)
    avg_fam = sum(f for _, f in rows) / len(rows)
    gap = avg_fam - avg_uni

    # Region rule (from project_10_phase_diagram_refinement_v1.py)
    if family_aware_wins >= 3 and gap > 0.005:
        region = "family-aware region"
    elif universal_wins >= 2 or gap < -0.003:
        region = "universal region"
    else:
        region = "transition region"

    return CellResult(
        H=residual_abs,
        P=universal_power,
        avg_uni=avg_uni,
        avg_fam=avg_fam,
        gap=gap,
        universal_wins=universal_wins,
        family_aware_wins=family_aware_wins,
        near_ties=near_ties,
        region=region,
    )


# =============================================================================
# Metrics (no sklearn)
# =============================================================================

LABELS = ["family-aware region", "transition region", "universal region"]


def confusion_counts(y_true: List[str], y_pred: List[str]) -> Dict[str, Dict[str, int]]:
    cm = {t: {p: 0 for p in LABELS} for t in LABELS}
    for t, p in zip(y_true, y_pred):
        cm[t][p] += 1
    return cm


def accuracy(y_true: List[str], y_pred: List[str]) -> float:
    correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    return correct / max(1, len(y_true))


def macro_f1(y_true: List[str], y_pred: List[str]) -> float:
    # compute TP/FP/FN per class
    f1s = []
    for lbl in LABELS:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == lbl and p == lbl)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != lbl and p == lbl)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == lbl and p != lbl)

        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) > 0 else 0.0
        f1s.append(f1)

    return sum(f1s) / len(f1s)


# =============================================================================
# Baselines
# =============================================================================

def majority_baseline_label_from_project10_grid() -> str:
    # In Project 10 3x3 grid: universal appears in 6/9 cells, family-aware in 2/9, transition in 1/9
    return "universal region"


def build_project10_grid_points() -> List[Tuple[float, float, str]]:
    Hs = [0.003, 0.009, 0.015]
    Ps = [0.30, 0.36, 0.42]
    grid = []
    for H in Hs:
        for P in Ps:
            region = ground_truth_region(H, P).region
            grid.append((H, P, region))
    return grid


def normalized_distance(aH: float, aP: float, bH: float, bP: float) -> float:
    # Normalize by Project 10 grid ranges to avoid P dominating distance scale
    H_range = 0.015 - 0.003  # 0.012
    P_range = 0.42 - 0.30    # 0.12
    return (((aH - bH) / H_range) ** 2 + ((aP - bP) / P_range) ** 2) ** 0.5


def nearest_neighbor_baseline(H: float, P: float, grid_points: List[Tuple[float, float, str]]) -> str:
    best = None
    best_d = None
    for gH, gP, glabel in grid_points:
        d = normalized_distance(H, P, gH, gP)
        if best_d is None or d < best_d:
            best_d = d
            best = glabel
    return best


# =============================================================================
# IO
# =============================================================================

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def save_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


# =============================================================================
# Main
# =============================================================================

def main():
    holdout = load_json(HOLDOUT_PATH)
    preds = load_json(PRED_PATH)

    points = holdout["points"]
    pred_list = preds["predictions"]

    pred_by_id = {p["id"]: p for p in pred_list}

    # Integrity checks: ids + H,P match exactly
    for pt in points:
        pid = pt["id"]
        if pid not in pred_by_id:
            raise ValueError(f"Missing prediction for point id={pid}")
        p = pred_by_id[pid]
        if float(p["H"]) != float(pt["H"]) or float(p["P"]) != float(pt["P"]):
            raise ValueError(f"Prediction H,P mismatch for id={pid}: holdout({pt['H']},{pt['P']}) vs pred({p['H']},{p['P']})")

    y_true = []
    y_pred = []
    y_major = []
    y_nn = []

    grid = build_project10_grid_points()
    majority_label = majority_baseline_label_from_project10_grid()

    table_rows = []

    for pt in points:
        H = float(pt["H"])
        P = float(pt["P"])
        pid = pt["id"]

        gt = ground_truth_region(H, P)
        true_label = gt.region

        pred_label = pred_by_id[pid]["predicted_region"]
        conf = pred_by_id[pid].get("confidence", "low")

        nn_label = nearest_neighbor_baseline(H, P, grid)

        y_true.append(true_label)
        y_pred.append(pred_label)
        y_major.append(majority_label)
        y_nn.append(nn_label)

        table_rows.append({
            "id": pid,
            "H": H,
            "P": P,
            "predicted": pred_label,
            "confidence": conf,
            "true": true_label,
            "baseline_majority": majority_label,
            "baseline_nearest_neighbor": nn_label,
            "avg_uni": gt.avg_uni,
            "avg_fam": gt.avg_fam,
            "gap": gt.gap,
            "uni_wins": gt.universal_wins,
            "fam_wins": gt.family_aware_wins,
            "near_ties": gt.near_ties
        })

    # Metrics
    m = {
        "model": {
            "accuracy": accuracy(y_true, y_pred),
            "macro_f1": macro_f1(y_true, y_pred),
            "confusion": confusion_counts(y_true, y_pred),
        },
        "baseline_majority_from_project10_grid": {
            "label": majority_label,
            "accuracy": accuracy(y_true, y_major),
            "macro_f1": macro_f1(y_true, y_major),
            "confusion": confusion_counts(y_true, y_major),
        },
        "baseline_nearest_neighbor_project10_grid": {
            "accuracy": accuracy(y_true, y_nn),
            "macro_f1": macro_f1(y_true, y_nn),
            "confusion": confusion_counts(y_true, y_nn),
        },
    }

    best_baseline_f1 = max(
        m["baseline_majority_from_project10_grid"]["macro_f1"],
        m["baseline_nearest_neighbor_project10_grid"]["macro_f1"],
    )

    pass_condition = (m["model"]["macro_f1"] >= best_baseline_f1 + 0.15) and (m["model"]["macro_f1"] >= 0.60)

    artifact = {
        "gate": "prediction_gate_v1",
        "paths": {
            "holdout_points": str(HOLDOUT_PATH),
            "predictions": str(PRED_PATH),
        },
        "metrics": m,
        "best_baseline_macro_f1": best_baseline_f1,
        "pass_condition": {
            "required": "macro_f1 >= best_baseline + 0.15 AND macro_f1 >= 0.60",
            "passed": bool(pass_condition),
        },
        "per_point": table_rows
    }

    save_json(ARTIFACT_JSON, artifact)

    # Markdown report
    lines = []
    lines.append("# PROJECT 11 — PREDICTION GATE V1 REPORT")
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- points: {len(points)}")
    lines.append(f"- model accuracy: {m['model']['accuracy']:.4f}")
    lines.append(f"- model macro-F1: {m['model']['macro_f1']:.4f}")
    lines.append(f"- best baseline macro-F1: {best_baseline_f1:.4f}")
    lines.append(f"- PASS: {pass_condition}")
    lines.append("")
    lines.append("## Baselines")
    lines.append(f"- majority label (from Project 10 grid): `{majority_label}`")
    lines.append(f"- majority baseline macro-F1: {m['baseline_majority_from_project10_grid']['macro_f1']:.4f}")
    lines.append(f"- nearest-neighbor baseline macro-F1: {m['baseline_nearest_neighbor_project10_grid']['macro_f1']:.4f}")
    lines.append("")
    lines.append("## Per-point table")
    lines.append("")
    lines.append("| id | H | P | predicted | conf | true | maj | nn | gap | uni_wins | fam_wins | near_ties |")
    lines.append("|---:|---:|---:|---|---|---|---|---|---:|---:|---:|---:|")
    for r in table_rows:
        lines.append(
            f"| {r['id']} | {r['H']:.4f} | {r['P']:.3f} | {r['predicted']} | {r['confidence']} | "
            f"{r['true']} | {r['baseline_majority']} | {r['baseline_nearest_neighbor']} | "
            f"{r['gap']:.4f} | {r['uni_wins']} | {r['fam_wins']} | {r['near_ties']} |"
        )

    lines.append("")
    lines.append("## Notes")
    lines.append("- Ground truth uses the exact Project 10 phase-diagram rule (wins + gap thresholds).")
    lines.append("- Predictions were loaded from the locked JSON file; integrity checks enforce id and H,P match.")
    lines.append("")
    lines.append("Artifact JSON saved to:")
    lines.append(f"- `{ARTIFACT_JSON.as_posix()}`")

    save_text(REPORT_MD, "\n".join(lines))

    # Terminal summary (boss-friendly)
    print("\n=== PREDICTION GATE V1 RESULT ===")
    print(f"points: {len(points)}")
    print(f"model accuracy: {m['model']['accuracy']:.4f}")
    print(f"model macro-F1: {m['model']['macro_f1']:.4f}")
    print(f"best baseline macro-F1: {best_baseline_f1:.4f}")
    print(f"PASS: {pass_condition}")
    print(f"Report: {REPORT_MD}")
    print(f"Artifact: {ARTIFACT_JSON}\n")


if __name__ == "__main__":
    main()
