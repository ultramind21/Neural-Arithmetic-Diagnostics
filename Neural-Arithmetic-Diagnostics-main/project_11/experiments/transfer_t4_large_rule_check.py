from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P11_RESULTS = ROOT / "project_11" / "results"

SYSTEM_PATH = P11_RESULTS / "transfer_t4_system.json"

IN_DIR = P11_RESULTS / "transfer_t4_large"
HOLDOUT_PATH = IN_DIR / "holdout_points.json"
PRED_PATH = IN_DIR / "predictions.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def rule_v3_predict(system: dict, H: float, P: float) -> str:
    sfs = [float(f["shared_failure"]) for f in system["families"]]
    deltas = [0.80 * H + (0.30 - P) * sf for sf in sfs]

    fam_wins_est = sum(1 for d in deltas if d > 0.005)
    uni_wins_est = sum(1 for d in deltas if d < -0.005)
    gap_est = sum(deltas) / len(deltas)

    if (fam_wins_est >= 3) and (gap_est > 0.005):
        return "family-aware region"
    if (uni_wins_est >= 2) or (gap_est < -0.003):
        return "universal region"
    return "transition region"


def main():
    system = load_json(SYSTEM_PATH)
    holdout = load_json(HOLDOUT_PATH)
    preds = load_json(PRED_PATH)

    points = holdout["points"]
    pred_by_id = {p["id"]: p for p in preds["predictions"]}

    mismatches = []
    for pt in points:
        pid = pt["id"]
        if pid not in pred_by_id:
            raise SystemExit(f"FAIL: missing prediction for id={pid}")
        p = pred_by_id[pid]
        if float(p["H"]) != float(pt["H"]) or float(p["P"]) != float(pt["P"]):
            raise SystemExit(f"FAIL: H,P mismatch for id={pid}")

        expected = rule_v3_predict(system, float(pt["H"]), float(pt["P"]))
        actual = p["predicted_region"]
        if expected != actual:
            mismatches.append({"id": pid, "expected": expected, "actual": actual})

    print("\n=== T4-LARGE — RULE V3 COMPLIANCE CHECK ===")
    print(f"points checked: {len(points)}")
    print(f"mismatches: {len(mismatches)}")
    if mismatches:
        print("first mismatches (up to 10):", mismatches[:10])
        raise SystemExit("FAIL: predictions do not match Rule V3.")
    print("PASS: predictions match Rule V3 exactly.\n")


if __name__ == "__main__":
    main()
