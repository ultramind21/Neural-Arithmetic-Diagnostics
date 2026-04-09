from __future__ import annotations

import json
import math
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List

ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "project_11" / "experiments"
RES = ROOT / "project_11" / "results"

POINTS_FILE = EXP / "PROJECT_11_HOLDOUT_POINTS_V1.json"
SUB_FILE = EXP / "PROJECT_11_HOLDOUT_PREDICTIONS_SUBMISSION_V1.json"

OUT_JSON = RES / "project_11_holdout_system_v1_artifact.json"
OUT_MD = RES / "project_11_holdout_system_v1_report.md"

FAMILIES = ["A", "B", "C", "D"]
SIGNS = [1, -1, 1, -1]

# Structural-OOD base parameters (not Project 10 numbers)
BASE_GLOBAL = {"A": 0.52, "B": 0.49, "C": 0.47, "D": 0.51}
SHARED_FAIL = {"A": 0.33, "B": 0.36, "C": 0.31, "D": 0.38}


def clamp(x: float) -> float:
    return max(0.0, min(1.0, x))


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def simulate_point(point: Dict[str, Any]) -> Dict[str, Any]:
    """
    Structural-OOD system:
    - stochastic outcomes via Bernoulli trials
    - universal-interference depends on heterogeneity and family mode
    - nonlinear response curves
    """
    h = float(point["h_scale"])
    u = float(point["u_power"])
    k = float(point["k_interference"])
    sigma = float(point["noise_sigma"])
    n_runs = int(point["n_runs"])

    per_family = {}
    gains_uni = []

    for i, fam in enumerate(FAMILIES):
        mode = SIGNS[i] * h

        # baseline success probability (stochastic, nonlinear)
        base_logit = (BASE_GLOBAL[fam] - 0.5) * 4.0 - 0.8 * SHARED_FAIL[fam]
        base_p = sigmoid(base_logit)

        # universal rescue: power u but suppressed by interference ~ k*|mode|
        eff_u = max(0.0, u - k * abs(mode))
        uni_logit_delta = 2.5 * eff_u * (0.5 + SHARED_FAIL[fam])
        uni_p = sigmoid(base_logit + uni_logit_delta)

        # family-aware rescue: baseline + mode-capture with different nonlinearity
        fam_logit_delta = 2.0 * 0.30 * (0.5 + SHARED_FAIL[fam]) + 6.0 * (abs(mode) ** 0.85)
        fam_p = sigmoid(base_logit + fam_logit_delta)

        # Monte Carlo simulation with noise
        rng = random.Random(1337 + hash((point["id"], fam)) % 10_000_000)
        base_succ = 0
        uni_succ = 0
        fam_succ = 0

        for _ in range(n_runs):
            nb = rng.gauss(0.0, sigma)
            nu = rng.gauss(0.0, sigma)
            nf = rng.gauss(0.0, sigma)

            base_succ += 1 if rng.random() < clamp(base_p + nb) else 0
            uni_succ += 1 if rng.random() < clamp(uni_p + nu) else 0
            fam_succ += 1 if rng.random() < clamp(fam_p + nf) else 0

        G_base = base_succ / n_runs
        G_uni = uni_succ / n_runs
        G_fam = fam_succ / n_runs

        per_family[fam] = {
            "mode": mode,
            "G_base": G_base,
            "G_uni": G_uni,
            "G_fam": G_fam,
            "D_fam_minus_uni": (G_fam - G_uni),
        }
        gains_uni.append(G_uni - G_base)

    # observed metrics (exportable)
    P_obs = sum(gains_uni) / len(gains_uni)
    mean_gain = P_obs
    H_obs = sum((g - mean_gain) ** 2 for g in gains_uni) / len(gains_uni)  # population var

    # region decision (win-pattern based, not Project 10 gap rule)
    positives = sum(1 for fam in FAMILIES if per_family[fam]["D_fam_minus_uni"] > 0.01)
    negatives = sum(1 for fam in FAMILIES if per_family[fam]["D_fam_minus_uni"] < -0.01)

    if positives >= 3:
        actual_region = "family_aware_region"
    elif negatives >= 3:
        actual_region = "universal_region"
    else:
        actual_region = "transition_region"

    return {
        "per_family": per_family,
        "metrics": {"P_obs": P_obs, "H_obs": H_obs},
        "actual_region": actual_region
    }


def confusion_matrix(labels: List[str], y_true: List[str], y_pred: List[str]) -> Dict[str, Dict[str, int]]:
    m = {a: {b: 0 for b in labels} for a in labels}
    for t, p in zip(y_true, y_pred):
        m[t][p] += 1
    return m


def main():
    points = json.loads(POINTS_FILE.read_text(encoding="utf-8"))["points"]
    sub = json.loads(SUB_FILE.read_text(encoding="utf-8"))
    labels = sub["region_labels"]
    pred_map = {p["id"]: p for p in sub["predictions"]}

    results = []
    y_true = []
    y_pred = []
    boundary_pts = []

    for pt in points:
        pid = pt["id"]
        sim = simulate_point(pt)
        actual = sim["actual_region"]
        predicted = pred_map[pid]["predicted_region"]
        correct = (actual == predicted)

        row = {
            "id": pid,
            "inputs": {
                "h_scale": pt["h_scale"],
                "u_power": pt["u_power"],
                "k_interference": pt["k_interference"],
                "noise_sigma": pt["noise_sigma"],
                "n_runs": pt["n_runs"]
            },
            "predicted": predicted,
            "actual": actual,
            "correct": correct,
            "is_boundary_probe": bool(pt.get("is_boundary_probe", False)),
            "observed_metrics": sim["metrics"],
            "per_family": sim["per_family"]
        }
        results.append(row)
        y_true.append(actual)
        y_pred.append(predicted)
        if row["is_boundary_probe"]:
            boundary_pts.append(row)

    acc = sum(r["correct"] for r in results) / len(results)
    boundary_acc = sum(r["correct"] for r in boundary_pts) / len(boundary_pts) if boundary_pts else None

    cm = confusion_matrix(labels, y_true, y_pred)

    artifact = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "system_id": "holdout_system_v1_structural_ood",
        "summary": {
            "n_points": len(results),
            "accuracy": acc,
            "boundary_n": len(boundary_pts),
            "boundary_accuracy": boundary_acc
        },
        "confusion_matrix": cm,
        "results": results,
        "notes": [
            "Structural-OOD holdout system: stochastic, nonlinear, interference-based.",
            "No direct H,P inputs; H_obs and P_obs computed from outcomes."
        ]
    }

    RES.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(artifact, indent=2), encoding="utf-8")

    lines = [
        "# PROJECT 11 — HOLDOUT SYSTEM V1 REPORT",
        "",
        f"- accuracy: {acc:.3f}",
        f"- boundary_accuracy: {boundary_acc if boundary_acc is not None else 'N/A'}",
        "",
        "## Confusion Matrix",
        "```json",
        json.dumps(cm, indent=2),
        "```",
        "",
        "## Per-Point",
    ]
    for r in results:
        lines.append(f"- {r['id']}: pred={r['predicted']} actual={r['actual']} correct={r['correct']} boundary={r['is_boundary_probe']} H_obs={r['observed_metrics']['H_obs']:.6f} P_obs={r['observed_metrics']['P_obs']:.6f}")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("✓ artifact:", OUT_JSON)
    print("✓ report:", OUT_MD)
    print("✓ accuracy:", acc)
    print("✓ boundary_accuracy:", boundary_acc)


if __name__ == "__main__":
    main()
