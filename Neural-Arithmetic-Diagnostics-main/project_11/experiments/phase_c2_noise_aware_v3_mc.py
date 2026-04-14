from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
P11_RESULTS = ROOT / "project_11" / "results"

SYSTEM_PATH = P11_RESULTS / "transfer_t4_system.json"
HOLDOUT_PATH = P11_RESULTS / "transfer_t4_large" / "holdout_points.json"

OUT_DIR = P11_RESULTS / "phase_c2_noise"
REPORT_MD = OUT_DIR / "report.md"
ARTIFACT_JSON = OUT_DIR / "artifact.json"

LABELS = ["family-aware region", "transition region", "universal region"]

# ranges must match the generation ranges used in T4-Large
H_MIN, H_MAX = 0.0010, 0.0200
P_MIN, P_MAX = 0.2600, 0.4200

REPS = 20
K_MC = 25  # LOCKED
NOISE_SETTINGS = [
    (0.0000, 0.0000),
    (0.0005, 0.0020),
    (0.0010, 0.0040),
    (0.0015, 0.0060),
    (0.0020, 0.0080),
]


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


def clip(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


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
    if n == 1:
        return [a]
    step = (b - a) / (n - 1)
    return [a + i * step for i in range(n)]


def ground_truth(system: dict, H: float, P: float) -> str:
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

    for f in system["families"]:
        base = float(f["base_global"])
        sf = float(f["shared_failure"])

        uni = clamp01(base + P * sf)
        fam = clamp01(base + 0.30 * sf + 0.80 * H)

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
        return "family-aware region"
    if (universal_wins >= uni_wins_ge) or (gap < uni_gap_lt):
        return "universal region"
    return "transition region"


def rule_v3_predict(system: dict, H_obs: float, P_obs: float) -> str:
    sfs = [float(f["shared_failure"]) for f in system["families"]]
    deltas = [0.80 * H_obs + (0.30 - P_obs) * sf for sf in sfs]

    fam_wins_est = sum(1 for d in deltas if d > 0.005)
    uni_wins_est = sum(1 for d in deltas if d < -0.005)
    gap_est = sum(deltas) / len(deltas)

    if (fam_wins_est >= 3) and (gap_est > 0.005):
        return "family-aware region"
    if (uni_wins_est >= 2) or (gap_est < -0.003):
        return "universal region"
    return "transition region"


def v3_mc_predict(system: dict, H_obs: float, P_obs: float, sigma_H: float, sigma_P: float, rng: random.Random) -> str:
    if sigma_H == 0.0 and sigma_P == 0.0:
        return rule_v3_predict(system, H_obs, P_obs)

    votes = {lbl: 0 for lbl in LABELS}
    for _ in range(K_MC):
        Hs = clip(H_obs + rng.gauss(0.0, sigma_H), H_MIN, H_MAX)
        Ps = clip(P_obs + rng.gauss(0.0, sigma_P), P_MIN, P_MAX)
        lbl = rule_v3_predict(system, Hs, Ps)
        votes[lbl] += 1

    best = max(votes.values())
    tied = [k for k, v in votes.items() if v == best]
    if len(tied) == 1:
        return tied[0]
    order = ["transition region", "universal region", "family-aware region"]
    for k in order:
        if k in tied:
            return k
    return "transition region"


def mean(xs: List[float]) -> float:
    return sum(xs) / max(1, len(xs))


def stdev(xs: List[float]) -> float:
    if len(xs) < 2:
        return 0.0
    m = mean(xs)
    return (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5


def main():
    system = load_json(SYSTEM_PATH)
    holdout = load_json(HOLDOUT_PATH)
    points = holdout["points"]

    true_HP = [(float(pt["H"]), float(pt["P"])) for pt in points]
    y_true = [ground_truth(system, H, P) for (H, P) in true_HP]

    H_vals_11 = linspace(H_MIN, H_MAX, 11)
    P_vals_11 = linspace(P_MIN, P_MAX, 11)
    grid_11 = [(H, P, ground_truth(system, H, P)) for H in H_vals_11 for P in P_vals_11]

    results = []

    for sigma_H, sigma_P in NOISE_SETTINGS:
        v3_accs, v3_f1s = [], []
        v3mc_accs, v3mc_f1s = [], []
        nn_accs, nn_f1s = [], []

        for rep in range(REPS):
            base_seed = 12000 + rep * 1000 + int(sigma_H * 1e6) + int(sigma_P * 1e6)
            rng_meas = random.Random(base_seed)
            rng_mc = random.Random(base_seed + 777)

            y_v3 = []
            y_v3mc = []
            y_nn = []

            for (H_true, P_true) in true_HP:
                H_obs = clip(H_true + rng_meas.gauss(0.0, sigma_H), H_MIN, H_MAX)
                P_obs = clip(P_true + rng_meas.gauss(0.0, sigma_P), P_MIN, P_MAX)

                y_v3.append(rule_v3_predict(system, H_obs, P_obs))
                y_v3mc.append(v3_mc_predict(system, H_obs, P_obs, sigma_H, sigma_P, rng_mc))
                y_nn.append(nn_label(H_obs, P_obs, grid_11))

            v3_accs.append(accuracy(y_true, y_v3))
            v3_f1s.append(macro_f1(y_true, y_v3))

            v3mc_accs.append(accuracy(y_true, y_v3mc))
            v3mc_f1s.append(macro_f1(y_true, y_v3mc))

            nn_accs.append(accuracy(y_true, y_nn))
            nn_f1s.append(macro_f1(y_true, y_nn))

        results.append({
            "sigma_H": sigma_H,
            "sigma_P": sigma_P,
            "v3_hard": {
                "acc_mean": mean(v3_accs),
                "acc_sd": stdev(v3_accs),
                "macro_f1_mean": mean(v3_f1s),
                "macro_f1_sd": stdev(v3_f1s),
            },
            "v3_mc": {
                "acc_mean": mean(v3mc_accs),
                "acc_sd": stdev(v3mc_accs),
                "macro_f1_mean": mean(v3mc_f1s),
                "macro_f1_sd": stdev(v3mc_f1s),
                "K": K_MC
            },
            "nn11": {
                "acc_mean": mean(nn_accs),
                "acc_sd": stdev(nn_accs),
                "macro_f1_mean": mean(nn_f1s),
                "macro_f1_sd": stdev(nn_f1s),
            }
        })

    artifact = {
        "test": "phase_c2_noise_aware_v3_mc",
        "reps": REPS,
        "K_mc": K_MC,
        "noise_settings": [{"sigma_H": a, "sigma_P": b} for a, b in NOISE_SETTINGS],
        "results": results
    }
    save_json(ARTIFACT_JSON, artifact)

    lines = []
    lines.append("# PROJECT 11 — PHASE C2 NOISE-AWARE REPORT (V3-MC)")
    lines.append("")
    lines.append(f"- points: {len(points)} (from locked T4-Large holdout)")
    lines.append(f"- reps per setting: {REPS}")
    lines.append(f"- MC samples per point (K): {K_MC}")
    lines.append("")
    lines.append("## Results (means ± sd)")
    lines.append("")
    lines.append("| sigma_H | sigma_P | V3-hard F1 | V3-MC F1 | NN11 F1 |")
    lines.append("|---:|---:|---:|---:|---:|")
    for r in results:
        lines.append(
            f"| {r['sigma_H']:.4f} | {r['sigma_P']:.4f} | "
            f"{r['v3_hard']['macro_f1_mean']:.4f} ± {r['v3_hard']['macro_f1_sd']:.4f} | "
            f"{r['v3_mc']['macro_f1_mean']:.4f} ± {r['v3_mc']['macro_f1_sd']:.4f} | "
            f"{r['nn11']['macro_f1_mean']:.4f} ± {r['nn11']['macro_f1_sd']:.4f} |"
        )
    lines.append("")
    lines.append("Artifacts:")
    lines.append(f"- `{ARTIFACT_JSON.as_posix()}`")

    save_text(REPORT_MD, "\n".join(lines))

    print("\n=== PHASE C2 NOISE-AWARE SWEEP COMPLETE ===")
    print(f"Report: {REPORT_MD}")
    print(f"Artifact: {ARTIFACT_JSON}\n")


if __name__ == "__main__":
    main()
