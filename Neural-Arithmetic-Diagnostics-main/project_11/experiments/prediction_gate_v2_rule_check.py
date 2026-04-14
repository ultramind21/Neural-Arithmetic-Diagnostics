from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
P11_RESULTS = ROOT / "project_11" / "results"

HOLDOUT_PATH = P11_RESULTS / "prediction_gate_v2_holdout_points.json"
PRED_PATH = P11_RESULTS / "prediction_gate_v2_predictions.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def predict_by_compressed_rule(H: float, P: float) -> str:
    """
    EXACTLY as written in PREDICTION_GATE_V2_PROTOCOL.md:

    D_min(H,P) = 0.80*H + 0.40*(0.30 - P)
    D_max(H,P) = 0.80*H + 0.41*(0.30 - P)
    gap_est    = 0.80*H + 0.405*(0.30 - P)

    Predict:
      - family-aware region if D_min > 0.005 AND gap_est > 0.005
      - universal region if D_max < -0.005 OR gap_est < -0.003
      - else transition region
    """
    d_min = 0.80 * H + 0.40 * (0.30 - P)
    d_max = 0.80 * H + 0.41 * (0.30 - P)
    gap_est = 0.80 * H + 0.405 * (0.30 - P)

    if (d_min > 0.005) and (gap_est > 0.005):
        return "family-aware region"
    if (d_max < -0.005) or (gap_est < -0.003):
        return "universal region"
    return "transition region"


def main():
    holdout = load_json(HOLDOUT_PATH)
    preds = load_json(PRED_PATH)

    points = holdout["points"]
    pred_list = preds["predictions"]
    pred_by_id = {p["id"]: p for p in pred_list}

    # Ensure full coverage + exact H,P match between holdout and predictions
    for pt in points:
        pid = pt["id"]
        if pid not in pred_by_id:
            raise SystemExit(f"FAIL: missing prediction for id={pid}")
        p = pred_by_id[pid]
        if float(p["H"]) != float(pt["H"]) or float(p["P"]) != float(pt["P"]):
            raise SystemExit(f"FAIL: H,P mismatch for id={pid}")

    mismatches = []
    for pt in points:
        pid = pt["id"]
        H = float(pt["H"])
        P = float(pt["P"])

        expected = predict_by_compressed_rule(H, P)
        actual = pred_by_id[pid]["predicted_region"]

        if expected != actual:
            mismatches.append({
                "id": pid,
                "H": H,
                "P": P,
                "expected_by_rule": expected,
                "actual_in_predictions_json": actual
            })

    print("\n=== PREDICTION GATE V2 — RULE COMPLIANCE CHECK ===")
    print(f"points checked: {len(points)}")
    print(f"mismatches: {len(mismatches)}")

    if mismatches:
        print("\nFirst mismatches (up to 10):")
        for m in mismatches[:10]:
            print(m)
        raise SystemExit("FAIL: predictions.json does NOT match the compressed rule in protocol.")
    else:
        print("PASS: predictions.json matches the compressed rule exactly.\n")


if __name__ == "__main__":
    main()
