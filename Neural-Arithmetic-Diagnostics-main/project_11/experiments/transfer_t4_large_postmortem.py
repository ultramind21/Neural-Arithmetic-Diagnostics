from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[2]
P11_RESULTS = ROOT / "project_11" / "results"

SYSTEM_PATH = P11_RESULTS / "transfer_t4_system.json"
IN_DIR = P11_RESULTS / "transfer_t4_large"
HOLDOUT_PATH = IN_DIR / "holdout_points.json"
PRED_PATH = IN_DIR / "predictions.json"

LABELS = ["family-aware region", "transition region", "universal region"]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


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


def linspace(a: float, b: float, n: int) -> List[float]:
    if n == 1:
        return [a]
    step = (b - a) / (n - 1)
    return [a + i * step for i in range(n)]


def ground_truth(system: dict, H: float, P: float) -> dict:
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

    sat_uni = 0
    sat_fam = 0

    for f in system["families"]:
        base = float(f["base_global"])
        sf = float(f["shared_failure"])

        uni_raw = base + P * sf
        fam_raw = base + 0.30 * sf + 0.80 * H

        if uni_raw >= 1.0:
            sat_uni += 1
        if fam_raw >= 1.0:
            sat_fam += 1

        uni = clamp(uni_raw)
        fam = clamp(fam_raw)

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

    return {
        "region": region,
        "gap": gap,
        "uni_wins": universal_wins,
        "fam_wins": family_aware_wins,
        "near_ties": near_ties,
        "sat_uni": sat_uni,
        "sat_fam": sat_fam,
    }


def main():
    system = load_json(SYSTEM_PATH)
    holdout = load_json(HOLDOUT_PATH)
    preds = load_json(PRED_PATH)

    points = holdout["points"]
    pred_by_id = {p["id"]: p for p in preds["predictions"]}

    # Build 11x11 baseline grid over the same ranges used in eval
    H_vals_11 = linspace(0.001, 0.020, 11)
    P_vals_11 = linspace(0.260, 0.420, 11)
    grid_11 = [(H, P, ground_truth(system, H, P)["region"]) for H in H_vals_11 for P in P_vals_11]

    rows = []
    y_true, y_pred, y_nn11 = [], [], []
    mask_u, mask_b = [], []

    for pt in points:
        pid = pt["id"]
        if pid not in pred_by_id:
            raise SystemExit(f"Missing prediction for id={pid}")
        pr = pred_by_id[pid]["predicted_region"]

        H = float(pt["H"])
        P = float(pt["P"])
        kind = pt.get("kind", "unknown")

        gt = ground_truth(system, H, P)
        nn = nn_label(H, P, grid_11)

        y_true.append(gt["region"])
        y_pred.append(pr)
        y_nn11.append(nn)

        mask_u.append(kind == "uniform")
        mask_b.append(kind == "boundary")

        rows.append({
            "id": pid,
            "kind": kind,
            "H": H,
            "P": P,
            "true": gt["region"],
            "pred": pr,
            "nn11": nn,
            "gap": gt["gap"],
            "uni_wins": gt["uni_wins"],
            "fam_wins": gt["fam_wins"],
            "near_ties": gt["near_ties"],
            "sat_uni": gt["sat_uni"],
            "sat_fam": gt["sat_fam"],
        })

    def subset(mask: List[bool], yA: List[str], yB: List[str]) -> dict:
        yt = [t for t, m in zip(yA, mask) if m]
        yp = [p for p, m in zip(yB, mask) if m]
        return {"n": len(yt), "acc": accuracy(yt, yp), "macro_f1": macro_f1(yt, yp)}

    overall_model = {"acc": accuracy(y_true, y_pred), "macro_f1": macro_f1(y_true, y_pred)}
    overall_nn = {"acc": accuracy(y_true, y_nn11), "macro_f1": macro_f1(y_true, y_nn11)}

    print("\n=== T4-LARGE POSTMORTEM ===")
    print(f"points: {len(rows)}")
    print("model overall:", overall_model)
    print("nn11 overall:", overall_nn)
    print("model uniform:", subset(mask_u, y_true, y_pred))
    print("model boundary:", subset(mask_b, y_true, y_pred))
    print("nn11 uniform:", subset(mask_u, y_true, y_nn11))
    print("nn11 boundary:", subset(mask_b, y_true, y_nn11))

    # Error lists
    model_errors = [r for r in rows if r["pred"] != r["true"]]
    nn_errors = [r for r in rows if r["nn11"] != r["true"]]

    print("\ncounts:")
    print("model errors:", len(model_errors))
    print("nn11 errors:", len(nn_errors))

    # Where model wrong but nn correct
    diff = [r for r in rows if (r["pred"] != r["true"]) and (r["nn11"] == r["true"])]
    print("model wrong & nn correct:", len(diff))

    # Show first 30 model errors sorted by closeness to boundary thresholds (gap proximity)
    # closer to {+0.005, -0.003} => harder boundary
    def gap_hardness(r):
        return min(abs(r["gap"] - 0.005), abs(r["gap"] + 0.003))

    model_errors_sorted = sorted(model_errors, key=gap_hardness)

    print("\n=== FIRST 30 MODEL ERRORS (most boundary-like) ===")
    for r in model_errors_sorted[:30]:
        print({
            "id": r["id"],
            "kind": r["kind"],
            "H": round(r["H"], 6),
            "P": round(r["P"], 6),
            "true": r["true"],
            "pred": r["pred"],
            "nn11": r["nn11"],
            "gap": round(r["gap"], 6),
            "uni_wins": r["uni_wins"],
            "fam_wins": r["fam_wins"],
            "near_ties": r["near_ties"],
            "sat_uni": r["sat_uni"],
            "sat_fam": r["sat_fam"],
        })

    # Saturation correlation quick check
    sat_related = [r for r in model_errors if (r["sat_uni"] > 0 or r["sat_fam"] > 0)]
    print("\nmodel errors with any saturation (uni or fam clamped raw>=1):", len(sat_related))
    print("done.\n")


if __name__ == "__main__":
    main()
