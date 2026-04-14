from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
P11_RESULTS = ROOT / "project_11" / "results"

SYSTEM_PATH = P11_RESULTS / "transfer_t4_system.json"
IN_DIR = P11_RESULTS / "phase_c3_sat_margin"
HOLDOUT_PATH = IN_DIR / "holdout_points.json"

REPORT_MD = IN_DIR / "report.md"
ARTIFACT_JSON = IN_DIR / "artifact.json"

LABELS = ["family-aware region", "transition region", "universal region"]

H_MIN, H_MAX = 0.0010, 0.0200
P_MIN, P_MAX = 0.2600, 0.4200


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


def ground_truth(system: dict, H: float, P: float) -> Tuple[str, int]:
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

    sat_risk = 0

    for f in system["families"]:
        base = float(f["base_global"])
        sf = float(f["shared_failure"])

        uni_raw = base + P * sf
        fam_raw = base + 0.30 * sf + 0.80 * H

        if (uni_raw >= 1.0) or (fam_raw >= 1.0):
            sat_risk += 1

        uni = clamp01(uni_raw)
        fam = clamp01(fam_raw)

        if uni > fam + margin:
            universal_wins += 1
        elif fam > uni + margin:
            family_aware_wins += 1
        else:
            near_ties += 1

        uni_scores.append(uni)
        fam_scores.append(fam)

    gap = (sum(fam_scores) / len(fam_scores)) - (sum(uni_scores) / len(uni_scores))

    if (family_aware_wins >= fam_wins_ge) and (gap > fam_gap_gt):
        return "family-aware region", sat_risk
    if (universal_wins >= uni_wins_ge) or (gap < uni_gap_lt):
        return "universal region", sat_risk
    return "transition region", sat_risk


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


def main():
    system = load_json(SYSTEM_PATH)
    holdout = load_json(HOLDOUT_PATH)
    points = holdout["points"]

    H_vals_11 = linspace(H_MIN, H_MAX, 11)
    P_vals_11 = linspace(P_MIN, P_MAX, 11)
    grid_11 = [(H, P, ground_truth(system, H, P)[0]) for H in H_vals_11 for P in P_vals_11]

    y_true, y_v3, y_v31, y_nn = [], [], [], []
    sat_flags_true = []
    kinds = []

    for pt in points:
        H = float(pt["H"])
        P = float(pt["P"])
        kinds.append(pt.get("kind", "unknown"))

        gt, sat_risk = ground_truth(system, H, P)
        y_true.append(gt)
        sat_flags_true.append(sat_risk >= 1)

        y_v3.append(v3_predict(system, H, P))
        y_v31.append(v3_1_sat_margin(system, H, P))
        y_nn.append(nn_label(H, P, grid_11))

    def subset(mask):
        yt = [t for t, m in zip(y_true, mask) if m]
        a = {
            "n": len(yt),
            "v3_macro_f1": macro_f1(yt, [p for p, m in zip(y_v3, mask) if m]),
            "v31_macro_f1": macro_f1(yt, [p for p, m in zip(y_v31, mask) if m]),
            "nn11_macro_f1": macro_f1(yt, [p for p, m in zip(y_nn, mask) if m]),
        }
        return a

    mask_uniform = [k == "uniform" for k in kinds]
    mask_boundary = [k == "boundary" for k in kinds]
    mask_sat = sat_flags_true
    mask_nosat = [not x for x in sat_flags_true]

    metrics = {
        "overall": {
            "v3_acc": accuracy(y_true, y_v3),
            "v3_macro_f1": macro_f1(y_true, y_v3),
            "v31_acc": accuracy(y_true, y_v31),
            "v31_macro_f1": macro_f1(y_true, y_v31),
            "nn11_acc": accuracy(y_true, y_nn),
            "nn11_macro_f1": macro_f1(y_true, y_nn),
        },
        "subsets": {
            "uniform": subset(mask_uniform),
            "boundary": subset(mask_boundary),
            "sat_risk_ge1": subset(mask_sat),
            "sat_risk_0": subset(mask_nosat)
        }
    }

    v3_err_sat = sum(1 for t, p, s in zip(y_true, y_v3, sat_flags_true) if (t != p and s))
    v3_err = sum(1 for t, p in zip(y_true, y_v3) if t != p)
    v31_err_sat = sum(1 for t, p, s in zip(y_true, y_v31, sat_flags_true) if (t != p and s))
    v31_err = sum(1 for t, p in zip(y_true, y_v31) if t != p)

    artifact = {
        "test": "phase_c3_sat_margin",
        "seed": holdout.get("seed", None),
        "n_total": len(points),
        "metrics": metrics,
        "error_sat": {
            "v3": {"errors": v3_err, "errors_with_sat": v3_err_sat},
            "v31": {"errors": v31_err, "errors_with_sat": v31_err_sat}
        }
    }
    save_json(ARTIFACT_JSON, artifact)

    lines = []
    lines.append("# PROJECT 11 — PHASE C3 REPORT (Saturation-aware margins)")
    lines.append("")
    lines.append(f"- points: {len(points)}")
    lines.append(f"- seed: {holdout.get('seed', 'unknown')}")
    lines.append("")
    lines.append("## Overall")
    o = metrics["overall"]
    lines.append(f"- V3-hard: acc={o['v3_acc']:.4f} | macro-F1={o['v3_macro_f1']:.4f}")
    lines.append(f"- V3.1 sat-margin: acc={o['v31_acc']:.4f} | macro-F1={o['v31_macro_f1']:.4f}")
    lines.append(f"- NN11: acc={o['nn11_acc']:.4f} | macro-F1={o['nn11_macro_f1']:.4f}")
    lines.append("")
    lines.append("## Subsets (macro-F1)")
    for name, s in metrics["subsets"].items():
        lines.append(f"- {name}: n={s['n']} | V3={s['v3_macro_f1']:.4f} | V3.1={s['v31_macro_f1']:.4f} | NN11={s['nn11_macro_f1']:.4f}")
    lines.append("")
    lines.append("## Saturation-linked errors")
    es = artifact["error_sat"]
    lines.append(f"- V3 errors: {es['v3']['errors']} | errors_with_sat: {es['v3']['errors_with_sat']}")
    lines.append(f"- V3.1 errors: {es['v31']['errors']} | errors_with_sat: {es['v31']['errors_with_sat']}")
    lines.append("")
    lines.append("Artifacts:")
    lines.append(f"- `{ARTIFACT_JSON.as_posix()}`")

    save_text(REPORT_MD, "\n".join(lines))

    print("\n=== PHASE C3 EVALUATION COMPLETE ===")
    print(f"Report: {REPORT_MD}")
    print(f"Artifact: {ARTIFACT_JSON}\n")


if __name__ == "__main__":
    main()
