from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Tuple

ROOT = Path(__file__).resolve().parents[2]
GATE_DIR = ROOT / "meta" / "project_11_gate"
SUBMISSION = GATE_DIR / "PROJECT_11_PREDICTIONS_SUBMISSION_V1.json"

OUT_DIR = GATE_DIR / "outputs"
OUT_JSON = OUT_DIR / "project_11_prediction_gate_v1_artifact.json"
OUT_MD = OUT_DIR / "project_11_prediction_gate_v1_report.md"

BASE_CASES = [
    {"family": "A", "base_global": 0.48, "shared_failure": 0.41},
    {"family": "B", "base_global": 0.47, "shared_failure": 0.40},
    {"family": "C", "base_global": 0.46, "shared_failure": 0.41},
    {"family": "D", "base_global": 0.47, "shared_failure": 0.40},
]
RESIDUAL_SIGNS = [1, -1, 1, -1]


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def universal_score(base_global: float, shared_failure: float, P: float) -> float:
    return clamp(base_global + P * shared_failure)


def family_aware_score(base_global: float, shared_failure: float, H: float) -> float:
    # consistent with Project 10 Phase 2 mapping
    return clamp(base_global + 0.30 * shared_failure + 0.80 * abs(H))


def evaluate_region(H: float, P: float) -> Tuple[str, Dict[str, Any]]:
    universal_wins = 0
    family_aware_wins = 0
    near_ties = 0

    rows = []
    for i, case in enumerate(BASE_CASES):
        residual = RESIDUAL_SIGNS[i] * H
        uni = universal_score(case["base_global"], case["shared_failure"], P)
        fam = family_aware_score(case["base_global"], case["shared_failure"], residual)

        if uni > fam + 0.005:
            universal_wins += 1
            winner = "universal"
        elif fam > uni + 0.005:
            family_aware_wins += 1
            winner = "family_aware"
        else:
            near_ties += 1
            winner = "near_tie"

        rows.append({"family": case["family"], "uni": uni, "fam": fam, "winner": winner})

    avg_uni = sum(r["uni"] for r in rows) / len(rows)
    avg_fam = sum(r["fam"] for r in rows) / len(rows)
    gap = avg_fam - avg_uni

    # region decision (aligned with phase-diagram refinement style)
    if family_aware_wins >= 3 and gap > 0.005:
        region = "family_aware_region"
    elif universal_wins >= 2 or gap < -0.003:
        region = "universal_region"
    else:
        region = "transition_region"

    debug = {
        "avg_uni": avg_uni,
        "avg_fam": avg_fam,
        "gap_fam_minus_uni": gap,
        "universal_wins": universal_wins,
        "family_aware_wins": family_aware_wins,
        "near_ties": near_ties,
        "rows": rows,
    }
    return region, debug


def confusion_matrix(labels: List[str], y_true: List[str], y_pred: List[str]) -> Dict[str, Dict[str, int]]:
    m = {a: {b: 0 for b in labels} for a in labels}
    for t, p in zip(y_true, y_pred):
        m[t][p] += 1
    return m


def main():
    if not SUBMISSION.exists():
        raise FileNotFoundError(f"Missing submission file: {SUBMISSION}")

    sub = json.loads(SUBMISSION.read_text(encoding="utf-8"))
    points = sub["points"]
    labels = sub["region_labels"]

    results = []
    y_true = []
    y_pred = []
    boundary_mask = []

    for pt in points:
        H = float(pt["H"])
        P = float(pt["P"])
        pred = pt["predicted_region"]

        true_region, dbg = evaluate_region(H, P)

        results.append({
            "id": pt["id"],
            "H": H,
            "P": P,
            "predicted": pred,
            "actual": true_region,
            "correct": pred == true_region,
            "confidence": pt.get("confidence", "unknown"),
            "is_boundary_probe": bool(pt.get("is_boundary_probe", False)),
            "debug": dbg,
        })

        y_true.append(true_region)
        y_pred.append(pred)
        boundary_mask.append(bool(pt.get("is_boundary_probe", False)))

    acc = sum(r["correct"] for r in results) / len(results)

    # baselines
    random_baseline = 1.0 / 3.0
    majority_class = max(set(y_true), key=y_true.count)
    majority_baseline = sum(1 for t in y_true if t == majority_class) / len(y_true)

    # boundary accuracy
    boundary_points = [r for r in results if r["is_boundary_probe"]]
    if boundary_points:
        boundary_acc = sum(r["correct"] for r in boundary_points) / len(boundary_points)
    else:
        boundary_acc = None

    cm = confusion_matrix(labels, y_true, y_pred)

    verdict = "FAIL"
    if acc >= 0.66 and (boundary_acc is None or boundary_acc >= 0.50):
        verdict = "PASS"

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "gate_version": sub.get("gate_version", "unknown"),
        "submission_file": str(SUBMISSION),
        "summary": {
            "n_points": len(results),
            "accuracy": acc,
            "random_baseline": random_baseline,
            "majority_class": majority_class,
            "majority_baseline": majority_baseline,
            "boundary_n": len(boundary_points),
            "boundary_accuracy": boundary_acc,
            "verdict": verdict,
        },
        "confusion_matrix": cm,
        "results": results,
        "notes": [
            "This gate is meaningful only if predictions were committed before running.",
            "PASS allows creating project_11/. FAIL blocks project_11/ and requires theory revision first."
        ],
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(artifact, indent=2), encoding="utf-8")

    # markdown report
    lines = [
        "# PROJECT 11 PREDICTION GATE V1 — REPORT",
        "",
        f"**Verdict:** {verdict}",
        "",
        "## Summary",
        f"- n_points: {artifact['summary']['n_points']}",
        f"- accuracy: {artifact['summary']['accuracy']:.3f}",
        f"- random_baseline: {artifact['summary']['random_baseline']:.3f}",
        f"- majority_class: {artifact['summary']['majority_class']}",
        f"- majority_baseline: {artifact['summary']['majority_baseline']:.3f}",
        f"- boundary_n: {artifact['summary']['boundary_n']}",
        f"- boundary_accuracy: {artifact['summary']['boundary_accuracy'] if artifact['summary']['boundary_accuracy'] is not None else 'N/A'}",
        "",
        "## Confusion Matrix",
        "```json",
        json.dumps(cm, indent=2),
        "```",
        "",
        "## Point Results",
    ]
    for r in results:
        lines.append(f"- {r['id']}: H={r['H']}, P={r['P']}, pred={r['predicted']}, actual={r['actual']}, correct={r['correct']}, boundary={r['is_boundary_probe']}")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("✓ Gate artifact:", OUT_JSON)
    print("✓ Gate report:", OUT_MD)
    print("✓ Verdict:", verdict)
    print("✓ Accuracy:", acc)
    print("✓ Boundary accuracy:", boundary_acc)


if __name__ == "__main__":
    main()
