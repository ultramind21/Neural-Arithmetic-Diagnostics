from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[2]
P11_RESULTS = ROOT / "project_11" / "results"

SYSTEM_PATH = P11_RESULTS / "transfer_t3_system.json"
HOLDOUT_PATH = P11_RESULTS / "transfer_t3_holdout_points.json"
PRED_PATH = P11_RESULTS / "transfer_t3_predictions.json"

REPORT_MD = P11_RESULTS / "transfer_t3_report.md"
ARTIFACT_JSON = P11_RESULTS / "transfer_t3_artifact.json"

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
    H: float
    P: float
    avg_uni: float
    avg_fam: float
    gap: float
    universal_wins: int
    family_aware_wins: int
    near_ties: int
    region: str


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

    return CellResult(H=H, P=P, avg_uni=avg_uni, avg_fam=avg_fam, gap=gap,
                      universal_wins=universal_wins, family_aware_wins=family_aware_wins,
                      near_ties=near_ties, region=region)


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

        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) > 0 else 0.0
        f1s.append(f1)

    return sum(f1s) / len(f1s)


def normalized_distance(aH: float, aP: float, bH: float, bP: float) -> float:
    H_range = 0.015 - 0.003  # 0.012
    P_range = 0.42 - 0.30    # 0.12
    return (((aH - bH) / H_range) ** 2 + ((aP - bP) / P_range) ** 2) ** 0.5


def build_grid(system: dict) -> List[Tuple[float, float, str]]:
    Hs = [0.003, 0.009, 0.015]
    Ps = [0.30, 0.36, 0.42]
    grid = []
    for H in Hs:
        for P in Ps:
            grid.append((H, P, ground_truth_region(system, H, P).region))
    return grid


def majority_label_from_grid(grid: List[Tuple[float, float, str]]) -> str:
    counts = {lbl: 0 for lbl in LABELS}
    for _, _, lbl in grid:
        counts[lbl] += 1
    order = ["universal region", "transition region", "family-aware region"]
    return max(order, key=lambda k: counts[k])


def nearest_neighbor_label(H: float, P: float, grid: List[Tuple[float, float, str]]) -> str:
    best_lbl = None
    best_d = None
    for gH, gP, glbl in grid:
        d = normalized_distance(H, P, gH, gP)
        if best_d is None or d < best_d:
            best_d = d
            best_lbl = glbl
    return best_lbl


def main():
    system = load_json(SYSTEM_PATH)
    holdout = load_json(HOLDOUT_PATH)
    preds = load_json(PRED_PATH)

    points = holdout["points"]
    pred_by_id = {p["id"]: p for p in preds["predictions"]}

    for pt in points:
        pid = pt["id"]
        if pid not in pred_by_id:
            raise SystemExit(f"Missing prediction for id={pid}")
        p = pred_by_id[pid]
        if float(p["H"]) != float(pt["H"]) or float(p["P"]) != float(pt["P"]):
            raise SystemExit(f"H,P mismatch for id={pid}")

    grid = build_grid(system)
    majority_lbl = majority_label_from_grid(grid)

    y_true, y_pred, y_major, y_nn = [], [], [], []
    rows = []

    for pt in points:
        pid = pt["id"]
        H = float(pt["H"])
        P = float(pt["P"])

        gt = ground_truth_region(system, H, P)
        pred = pred_by_id[pid]["predicted_region"]
        conf = pred_by_id[pid].get("confidence", "low")
        nn = nearest_neighbor_label(H, P, grid)

        y_true.append(gt.region)
        y_pred.append(pred)
        y_major.append(majority_lbl)
        y_nn.append(nn)

        rows.append({
            "id": pid, "H": H, "P": P,
            "predicted": pred, "confidence": conf,
            "true": gt.region,
            "baseline_majority": majority_lbl,
            "baseline_nearest_neighbor": nn,
            "gap": gt.gap,
            "uni_wins": gt.universal_wins,
            "fam_wins": gt.family_aware_wins,
            "near_ties": gt.near_ties
        })

    metrics = {
        "model": {
            "accuracy": accuracy(y_true, y_pred),
            "macro_f1": macro_f1(y_true, y_pred),
            "confusion": confusion_counts(y_true, y_pred),
        },
        "baseline_majority_from_t3_grid": {
            "label": majority_lbl,
            "accuracy": accuracy(y_true, y_major),
            "macro_f1": macro_f1(y_true, y_major),
            "confusion": confusion_counts(y_true, y_major),
        },
        "baseline_nearest_neighbor_t3_grid": {
            "accuracy": accuracy(y_true, y_nn),
            "macro_f1": macro_f1(y_true, y_nn),
            "confusion": confusion_counts(y_true, y_nn),
        },
        "t3_grid_counts": {
            "family-aware region": sum(1 for _, _, l in grid if l == "family-aware region"),
            "transition region": sum(1 for _, _, l in grid if l == "transition region"),
            "universal region": sum(1 for _, _, l in grid if l == "universal region")
        }
    }

    best_baseline_f1 = max(
        metrics["baseline_majority_from_t3_grid"]["macro_f1"],
        metrics["baseline_nearest_neighbor_t3_grid"]["macro_f1"],
    )

    passed = (metrics["model"]["macro_f1"] >= best_baseline_f1 + 0.10) and (metrics["model"]["macro_f1"] >= 0.70)

    artifact = {
        "test": "transfer_t3_rule_v3",
        "paths": {"system": str(SYSTEM_PATH), "holdout": str(HOLDOUT_PATH), "predictions": str(PRED_PATH)},
        "metrics": metrics,
        "best_baseline_macro_f1": best_baseline_f1,
        "pass_condition": {
            "required": "macro-F1 >= best_baseline + 0.10 AND macro-F1 >= 0.70",
            "passed": bool(passed)
        },
        "per_point": rows
    }

    save_json(ARTIFACT_JSON, artifact)

    lines = []
    lines.append("# PROJECT 11 — TRANSFER T3 REPORT (Rule V3)")
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- points: {len(points)}")
    lines.append(f"- model accuracy: {metrics['model']['accuracy']:.4f}")
    lines.append(f"- model macro-F1: {metrics['model']['macro_f1']:.4f}")
    lines.append(f"- best baseline macro-F1: {best_baseline_f1:.4f}")
    lines.append(f"- PASS: {passed}")
    lines.append("")
    lines.append("## T3 grid label counts (3x3)")
    lines.append(f"- {metrics['t3_grid_counts']}")
    lines.append("")
    lines.append("## Baselines")
    lines.append(f"- majority label (from T3 grid): `{majority_lbl}`")
    lines.append(f"- majority macro-F1: {metrics['baseline_majority_from_t3_grid']['macro_f1']:.4f}")
    lines.append(f"- nearest-neighbor macro-F1: {metrics['baseline_nearest_neighbor_t3_grid']['macro_f1']:.4f}")
    lines.append("")
    lines.append("## Per-point table")
    lines.append("")
    lines.append("| id | H | P | predicted | conf | true | maj | nn | gap | uni_wins | fam_wins | near_ties |")
    lines.append("|---:|---:|---:|---|---|---|---|---|---:|---:|---:|---:|")
    for r in rows:
        lines.append(
            f"| {r['id']} | {r['H']:.4f} | {r['P']:.3f} | {r['predicted']} | {r['confidence']} | "
            f"{r['true']} | {r['baseline_majority']} | {r['baseline_nearest_neighbor']} | "
            f"{r['gap']:.4f} | {r['uni_wins']} | {r['fam_wins']} | {r['near_ties']} |"
        )
    lines.append("")
    lines.append("Artifact JSON saved to:")
    lines.append(f"- `{ARTIFACT_JSON.as_posix()}`")

    save_text(REPORT_MD, "\n".join(lines))

    print("\n=== TRANSFER T3 RESULT (Rule V3) ===")
    print(f"points: {len(points)}")
    print(f"model accuracy: {metrics['model']['accuracy']:.4f}")
    print(f"model macro-F1: {metrics['model']['macro_f1']:.4f}")
    print(f"best baseline macro-F1: {best_baseline_f1:.4f}")
    print(f"PASS: {passed}")
    print(f"Report: {REPORT_MD}")
    print(f"Artifact: {ARTIFACT_JSON}\n")


if __name__ == "__main__":
    main()
