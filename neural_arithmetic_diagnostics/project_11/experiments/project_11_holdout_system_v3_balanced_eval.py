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

POINTS_FILE = EXP / "PROJECT_11_HOLDOUT_POINTS_V3_BALANCED.json"
SUB_FILE = EXP / "PROJECT_11_HOLDOUT_PREDICTIONS_SUBMISSION_V3_BALANCED.json"

OUT_JSON = RES / "project_11_holdout_system_v3_balanced_artifact.json"
OUT_MD = RES / "project_11_holdout_system_v3_balanced_report.md"

FAMILIES = ["A", "B", "C", "D"]
SIGNS = [1, -1, 1, -1]

BASE_GLOBAL = {"A": 0.52, "B": 0.49, "C": 0.47, "D": 0.51}
SHARED_FAIL = {"A": 0.33, "B": 0.36, "C": 0.31, "D": 0.38}


def clamp(x: float) -> float:
    return max(0.0, min(1.0, x))


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def spearman(x: List[float], y: List[float]) -> float:
    if len(x) < 3:
        return float("nan")

    def rank(v):
        s = sorted((val, i) for i, val in enumerate(v))
        r = [0] * len(v)
        for k, (_, i) in enumerate(s):
            r[i] = k + 1
        return r

    rx, ry = rank(x), rank(y)
    n = len(x)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    dx = math.sqrt(sum((rx[i] - mx) ** 2 for i in range(n)))
    dy = math.sqrt(sum((ry[i] - my) ** 2 for i in range(n)))
    return num / (dx * dy) if dx > 0 and dy > 0 else float("nan")


def simulate_point(point: Dict[str, Any]) -> Dict[str, Any]:
    h = float(point["h_scale"])
    u = float(point["u_power"])
    k = float(point["k_signed"])
    sigma = float(point["noise_sigma"])
    n_runs = int(point["n_runs"])

    per_family = {}
    gains_uni = []

    for i, fam in enumerate(FAMILIES):
        mode = SIGNS[i] * h

        base_logit = (BASE_GLOBAL[fam] - 0.5) * 4.0 - 0.8 * SHARED_FAIL[fam]
        base_p = sigmoid(base_logit)

        eff_u = max(0.0, u * (1.0 - k * mode))
        uni_logit_delta = 2.5 * eff_u * (0.5 + SHARED_FAIL[fam])
        uni_p = sigmoid(base_logit + uni_logit_delta)

        fam_logit_delta = 2.0 * 0.30 * (0.5 + SHARED_FAIL[fam]) + 6.0 * (abs(mode) ** 0.85)
        fam_p = sigmoid(base_logit + fam_logit_delta)

        rng = random.Random(2027 + hash((point["id"], fam)) % 10_000_000)
        base_succ = uni_succ = fam_succ = 0

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

    P_obs = sum(gains_uni) / len(gains_uni)
    mean_gain = P_obs
    H_obs = sum((g - mean_gain) ** 2 for g in gains_uni) / len(gains_uni)

    positives = sum(1 for fam in FAMILIES if per_family[fam]["D_fam_minus_uni"] > 0.01)
    negatives = sum(1 for fam in FAMILIES if per_family[fam]["D_fam_minus_uni"] < -0.01)

    if positives >= 3:
        actual_region = "family_aware_region"
    elif negatives >= 3:
        actual_region = "universal_region"
    else:
        actual_region = "transition_region"

    return {"per_family": per_family, "metrics": {"P_obs": P_obs, "H_obs": H_obs}, "actual_region": actual_region}


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

    # stratification store
    strat = {}  # u_power -> list of (h_scale, H_obs, P_obs)
    for pt in points:
        u = float(pt["u_power"])
        strat.setdefault(u, {"h": [], "H": [], "P": []})

        pid = pt["id"]
        sim = simulate_point(pt)
        actual = sim["actual_region"]
        predicted = pred_map[pid]["predicted_region"]
        correct = (actual == predicted)

        H_obs = float(sim["metrics"]["H_obs"])
        P_obs = float(sim["metrics"]["P_obs"])

        strat[u]["h"].append(float(pt["h_scale"]))
        strat[u]["H"].append(H_obs)
        strat[u]["P"].append(P_obs)

        row = {
            "id": pid,
            "inputs": {k: pt[k] for k in ["h_scale", "u_power", "k_signed", "noise_sigma", "n_runs"]},
            "predicted": predicted,
            "actual": actual,
            "correct": correct,
            "observed_metrics": sim["metrics"],
        }
        results.append(row)
        y_true.append(actual)
        y_pred.append(predicted)

    acc = sum(r["correct"] for r in results) / len(results)
    cm = confusion_matrix(labels, y_true, y_pred)

    strat_spearman = {}
    for u, d in sorted(strat.items()):
        strat_spearman[str(u)] = {
            "n": len(d["h"]),
            "spearman_h_vs_Hobs": spearman(d["h"], d["H"]),
            "spearman_h_vs_Pobs": spearman(d["h"], d["P"]),
        }

    artifact = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "system_id": "holdout_system_v3_balanced",
        "summary": {
            "n_points": len(results),
            "accuracy": acc
        },
        "confusion_matrix": cm,
        "stratified_spearman": strat_spearman,
        "results": results,
        "notes": [
            "Balanced design to reduce confounding: multiple h_scale values per u_power.",
            "Primary output: stratified Spearman to test identifiability of H_obs."
        ],
    }

    RES.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(artifact, indent=2), encoding="utf-8")

    lines = [
        "# PROJECT 11 — HOLDOUT SYSTEM V3 BALANCED REPORT",
        "",
        f"- accuracy: {acc:.3f}",
        "",
        "## Stratified Spearman",
        "```json",
        json.dumps(strat_spearman, indent=2),
        "```",
        "",
        "## Confusion Matrix",
        "```json",
        json.dumps(cm, indent=2),
        "```",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("✓ artifact:", OUT_JSON)
    print("✓ report:", OUT_MD)
    print("✓ accuracy:", acc)
    print("✓ stratified_spearman:", strat_spearman)


if __name__ == "__main__":
    main()
