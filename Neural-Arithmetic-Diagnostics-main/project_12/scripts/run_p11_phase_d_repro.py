from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[0]))

from p12_runlib import (
    load_manifest,
    sha256_text,
    get_git_hash,
    utc_now_iso,
    get_env_info,
    ensure_output_dir_is_safe,
    write_json,
    write_text,
)

ROOT = Path(__file__).resolve().parents[2]
R = ROOT / "project_11" / "results"

SYSTEM_HARD_PATH = R / "transfer_t4_system.json"
SYSTEM_SOFT_PATH = R / "phase_d_soft_clamp" / "system_soft_clamp.json"
HOLDOUT_PATH = R / "phase_c3_sat_margin" / "holdout_points.json"

LABELS = ["family-aware region", "transition region", "universal region"]

H_MIN, H_MAX = 0.0010, 0.0200
P_MIN, P_MAX = 0.2600, 0.4200


def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def clip(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def clamp01(x: float) -> float:
    return clip(x, 0.0, 1.0)


def softplus(x: float) -> float:
    import math
    if x > 50:
        return x
    return math.log1p(math.exp(x))


def soft_clamp_softplus(x: float, k: float) -> float:
    return clamp01(softplus(k * x) / k - softplus(k * (x - 1.0)) / k)


def dist_counts(y: List[str]) -> Dict[str, int]:
    d = {k: 0 for k in LABELS}
    for v in y:
        d[v] += 1
    return d


def accuracy(y_true: List[str], y_pred: List[str]) -> float:
    return sum(1 for t, p in zip(y_true, y_pred) if t == p) / max(1, len(y_true))


def macro_f1_fixed3(y_true: List[str], y_pred: List[str]) -> float:
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


def macro_f1_present(y_true: List[str], y_pred: List[str]) -> float:
    supports = dist_counts(y_true)
    present = [k for k, v in supports.items() if v > 0]
    if not present:
        return 0.0

    f1s = []
    for lbl in present:
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


def merge_system(hard: dict, soft: dict) -> dict:
    out = {}
    out["families"] = hard.get("families", [])
    out["thresholds"] = hard.get("thresholds", {})
    out["soft_clamp"] = soft.get("soft_clamp", soft.get("soft", {"k": 15}))
    return out


def ground_truth_soft(system: dict, H: float, P: float) -> str:
    thr = system["thresholds"]
    k = float(system["soft_clamp"]["k"])

    margin = float(thr["per_family_margin"])
    fam_gap_gt = float(thr["region_family_aware_gap_gt"])
    uni_gap_lt = float(thr["region_universal_gap_lt"])
    fam_wins_ge = int(thr["region_family_aware_wins_ge"])
    uni_wins_ge = int(thr["region_universal_wins_ge"])

    universal_wins = 0
    family_aware_wins = 0

    uni_scores = []
    fam_scores = []

    for f in system["families"]:
        base = float(f["base_global"])
        sf = float(f["shared_failure"])

        uni = soft_clamp_softplus(base + P * sf, k)
        fam = soft_clamp_softplus(base + 0.30 * sf + 0.80 * H, k)

        if uni > fam + margin:
            universal_wins += 1
        elif fam > uni + margin:
            family_aware_wins += 1

        uni_scores.append(uni)
        fam_scores.append(fam)

    gap = (sum(fam_scores) / len(fam_scores)) - (sum(uni_scores) / len(uni_scores))

    if (family_aware_wins >= fam_wins_ge) and (gap > fam_gap_gt):
        return "family-aware region"
    if (universal_wins >= uni_wins_ge) or (gap < uni_gap_lt):
        return "universal region"
    return "transition region"


def v3_predict(system: dict, H: float, P: float, margin=0.005, gap_fam=0.005, gap_uni=-0.003) -> str:
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


def v31_predict(system: dict, H: float, P: float) -> str:
    sat_risk = 0
    for f in system["families"]:
        base = float(f["base_global"])
        sf = float(f["shared_failure"])
        if (base + P * sf >= 1.0) or (base + 0.30 * sf + 0.80 * H >= 1.0):
            sat_risk += 1

    if sat_risk >= 1:
        return v3_predict(system, H, P, margin=0.0065, gap_fam=0.0065, gap_uni=-0.0045)
    return v3_predict(system, H, P, margin=0.005, gap_fam=0.005, gap_uni=-0.003)


def eval_metrics(y_true: List[str], y_pred: List[str]) -> dict:
    return {
        "acc": accuracy(y_true, y_pred),
        "macro_f1_fixed3": macro_f1_fixed3(y_true, y_pred),
        "macro_f1_present": macro_f1_present(y_true, y_pred),
        "pred_dist": dist_counts(y_pred),
    }


def subset(y_true: List[str], y_pred: List[str], mask: List[bool]) -> dict:
    yt = [t for t, m in zip(y_true, mask) if m]
    yp = [p for p, m in zip(y_pred, mask) if m]
    return {
        "n": len(yt),
        "acc": accuracy(yt, yp),
        "macro_f1_fixed3": macro_f1_fixed3(yt, yp),
        "macro_f1_present": macro_f1_present(yt, yp),
        "true_dist": dist_counts(yt),
        "pred_dist": dist_counts(yp),
    }


def main(manifest_path: str):
    manifest = load_manifest(manifest_path)
    output_dir = Path(manifest["output_dir"])
    
    # Safety check
    ensure_output_dir_is_safe(output_dir)
    
    OUT_DIR = output_dir
    OUT_MD = OUT_DIR / "RESOLUTION_SWEEP_EXTENDED.md"
    OUT_JSON = OUT_DIR / "RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json"
    
    hard = load_json(SYSTEM_HARD_PATH)
    soft = load_json(SYSTEM_SOFT_PATH)
    system = merge_system(hard, soft)

    # Read holdout path from manifest, or use default
    fixed_params = manifest.get("fixed_params", {})
    holdout_path = fixed_params.get("holdout_path", str(HOLDOUT_PATH))
    if not holdout_path.startswith("/"):
        holdout_path = ROOT / holdout_path
    else:
        holdout_path = Path(holdout_path)
    
    holdout = load_json(holdout_path)
    pts = holdout["points"]
    
    # Handle both dict and list formats for points
    if pts and isinstance(pts[0], dict):
        # Original format: [{H, P, kind}, ...]
        kinds = [pt.get("kind", "unknown") for pt in pts]
        HP = [(float(pt["H"]), float(pt["P"])) for pt in pts]
    else:
        # New format (re-validation): [[H, P], ...]
        kinds = ["uniform"] * len(pts)  # Default to uniform
        HP = [(float(pt[0]), float(pt[1])) for pt in pts]
    
    mask_u = [k == "uniform" for k in kinds]
    mask_b = [k == "boundary" for k in kinds]

    y_true = [ground_truth_soft(system, H, P) for (H, P) in HP]

    y_v3 = [v3_predict(system, H, P) for (H, P) in HP]
    y_v31 = [v31_predict(system, H, P) for (H, P) in HP]

    nn_grids = {}
    nn_preds = {}
    for n in [11, 21, 41, 81]:
        t0 = time.time()
        Hs = linspace(H_MIN, H_MAX, n)
        Ps = linspace(P_MIN, P_MAX, n)
        grid = [(H, P, ground_truth_soft(system, H, P)) for H in Hs for P in Ps]
        nn_grids[n] = {"n": n, "grid_points": len(grid), "build_seconds": time.time() - t0}
        nn_preds[n] = [nn_label(H, P, grid) for (H, P) in HP]

    artifact = {
        "k": system["soft_clamp"].get("k", None),
        "points": len(pts),
        "true_dist": dist_counts(y_true),
        "rules": {
            "V3": {
                "overall": eval_metrics(y_true, y_v3),
                "uniform": subset(y_true, y_v3, mask_u),
                "boundary": subset(y_true, y_v3, mask_b),
            },
            "V3.1": {
                "overall": eval_metrics(y_true, y_v31),
                "uniform": subset(y_true, y_v31, mask_u),
                "boundary": subset(y_true, y_v31, mask_b),
            }
        },
        "nn": {},
        "nn_grid_build": nn_grids,
    }

    for n, y_nn in nn_preds.items():
        artifact["nn"][f"NN{n}"] = {
            "overall": eval_metrics(y_true, y_nn),
            "uniform": subset(y_true, y_nn, mask_u),
            "boundary": subset(y_true, y_nn, mask_b),
        }

    # Add P12 metadata
    manifest_text = Path(manifest_path).read_text(encoding="utf-8")
    artifact["p12_metadata"] = {
        "git_hash": get_git_hash(),
        "timestamp_utc": utc_now_iso(),
        "env": get_env_info(),
        "manifest_path": str(Path(manifest_path).resolve()),
        "manifest_sha256": sha256_text(manifest_text),
        "entrypoint": "run_p11_phase_d_repro.py",
    }

    write_json(OUT_JSON, artifact)

    lines = []
    lines.append("# PHASE D — Resolution Sweep Extended (soft labels)")
    lines.append("")
    lines.append(f"- points: {artifact['points']}")
    lines.append(f"- soft clamp k: {artifact['k']}")
    lines.append(f"- true label dist: {artifact['true_dist']}")
    lines.append("")
    lines.append("## Overall (macro_f1_present)")
    lines.append("| model | acc | macroF1_present | macroF1_fixed3 |")
    lines.append("|---|---:|---:|---:|")

    def row(name: str, m: dict):
        lines.append(f"| {name} | {m['acc']:.4f} | {m['macro_f1_present']:.4f} | {m['macro_f1_fixed3']:.4f} |")

    row("V3", artifact["rules"]["V3"]["overall"])
    row("V3.1", artifact["rules"]["V3.1"]["overall"])
    for n in [11, 21, 41, 81]:
        row(f"NN{n}", artifact["nn"][f"NN{n}"]["overall"])

    lines.append("")
    lines.append("## Boundary subset (macro_f1_present)")
    lines.append("| model | acc | macroF1_present | macroF1_fixed3 |")
    lines.append("|---|---:|---:|---:|")
    row("V3 (boundary)", artifact["rules"]["V3"]["boundary"])
    row("V3.1 (boundary)", artifact["rules"]["V3.1"]["boundary"])
    for n in [11, 21, 41, 81]:
        row(f"NN{n} (boundary)", artifact["nn"][f"NN{n}"]["boundary"])

    lines.append("")
    lines.append("## NN grid build cost")
    lines.append("| grid | points | build_seconds |")
    lines.append("|---:|---:|---:|")
    for n in [11, 21, 41, 81]:
        g = artifact["nn_grid_build"][n]
        lines.append(f"| {n}x{n} | {g['grid_points']} | {g['build_seconds']:.4f} |")

    lines.append("")
    lines.append("Artifact:")
    lines.append(f"- `{OUT_JSON.as_posix()}`")

    write_text(OUT_MD, "\n".join(lines))
    print("\n=== PHASE D RESOLUTION SWEEP EXTENDED COMPLETE ===")
    print(f"Report: {OUT_MD}")
    print(f"Artifact: {OUT_JSON}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=str, help="Path to manifest JSON")
    args = parser.parse_args()
    main(args.manifest)
