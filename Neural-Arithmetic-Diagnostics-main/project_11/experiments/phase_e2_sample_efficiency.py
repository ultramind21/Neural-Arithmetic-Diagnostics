from __future__ import annotations

import json
import random
import time
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[2]
R = ROOT / "project_11" / "results"

SYSTEM_HARD_PATH = R / "transfer_t4_system.json"
SYSTEM_SOFT_PATH = R / "phase_d_soft_clamp" / "system_soft_clamp.json"
HOLDOUT_PATH = R / "phase_c3_sat_margin" / "holdout_points.json"

OUT_DIR = R / "phase_e2_sample_efficiency"
OUT_MD = OUT_DIR / "report.md"
OUT_JSON = OUT_DIR / "artifact.json"

LABELS = ["family-aware region", "transition region", "universal region"]

H_MIN, H_MAX = 0.0010, 0.0200
P_MIN, P_MAX = 0.2600, 0.4200

SIZES = [250, 500, 1000, 1500, 2000]
SEEDS = [101, 202, 303]
STRATS = ["uniform", "boundary", "mixed"]

# boundary pool (same for all conditions, built per seed)
POOL_SIZE = 60000


def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def save_text(p: Path, s: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")


def save_json(p: Path, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2), encoding="utf-8")


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
    return {
        "families": hard["families"],
        "thresholds": hard["thresholds"],
        "soft_clamp": soft.get("soft_clamp", {"k": 15}),
    }


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


def boundary_score_v3(H: float, P: float, sfs: list[float]) -> float:
    deltas = [0.80 * H + (0.30 - P) * sf for sf in sfs]
    gap_est = sum(deltas) / len(deltas)
    d_gap_fam = abs(gap_est - 0.005)
    d_gap_uni = abs(gap_est + 0.003)
    d_delta_fam = min(abs(d - 0.005) for d in deltas)
    d_delta_uni = min(abs(d + 0.005) for d in deltas)
    return min(d_gap_fam, d_gap_uni, d_delta_fam, d_delta_uni)


def sample_uniform(rng: random.Random) -> Tuple[float, float]:
    return rng.uniform(H_MIN, H_MAX), rng.uniform(P_MIN, P_MAX)


def build_reference(system: dict, rng: random.Random, N: int, strategy: str) -> List[Tuple[float, float, str]]:
    # shared_failure used only for boundary score selection
    sfs = [float(f["shared_failure"]) for f in system["families"]]

    used = set()
    ref_pts: List[Tuple[float, float]] = []

    def add_point(H: float, P: float):
        Hr, Pr = round(H, 6), round(P, 6)
        key = (Hr, Pr)
        if key in used:
            return False
        used.add(key)
        ref_pts.append((Hr, Pr))
        return True

    if strategy == "uniform":
        while len(ref_pts) < N:
            H, P = sample_uniform(rng)
            add_point(H, P)

    elif strategy == "boundary":
        # build pool and select top N
        pool = []
        for _ in range(POOL_SIZE):
            H, P = sample_uniform(rng)
            Hr, Pr = round(H, 6), round(P, 6)
            bs = boundary_score_v3(Hr, Pr, sfs)
            pool.append((bs, Hr, Pr))
        pool.sort(key=lambda x: x[0])

        for bs, Hr, Pr in pool:
            if len(ref_pts) >= N:
                break
            add_point(Hr, Pr)

        if len(ref_pts) < N:
            raise SystemExit("FAIL: boundary reference selection insufficient")

    elif strategy == "mixed":
        n_u = N // 2
        n_b = N - n_u

        # uniform first
        while len(ref_pts) < n_u:
            H, P = sample_uniform(rng)
            add_point(H, P)

        # boundary pool next
        pool = []
        for _ in range(POOL_SIZE):
            H, P = sample_uniform(rng)
            Hr, Pr = round(H, 6), round(P, 6)
            bs = boundary_score_v3(Hr, Pr, sfs)
            pool.append((bs, Hr, Pr))
        pool.sort(key=lambda x: x[0])

        for bs, Hr, Pr in pool:
            if len(ref_pts) >= N:
                break
            add_point(Hr, Pr)

        if len(ref_pts) < N:
            raise SystemExit("FAIL: mixed reference selection insufficient")

    else:
        raise ValueError("unknown strategy")

    # label reference points using soft ground truth
    ref_grid = [(H, P, ground_truth_soft(system, H, P)) for (H, P) in ref_pts]
    return ref_grid


def eval_one(system: dict, holdout_HP: List[Tuple[float, float]], y_true: List[str], ref_grid: List[Tuple[float, float, str]]) -> dict:
    y_pred = [nn_label(H, P, ref_grid) for (H, P) in holdout_HP]
    return {"acc": accuracy(y_true, y_pred), "macro_f1_present": macro_f1_present(y_true, y_pred)}


def nn_grid(system: dict, holdout_HP: List[Tuple[float, float]], y_true: List[str], n: int) -> dict:
    Hs = linspace(H_MIN, H_MAX, n)
    Ps = linspace(P_MIN, P_MAX, n)
    grid = [(H, P, ground_truth_soft(system, H, P)) for H in Hs for P in Ps]
    y_pred = [nn_label(H, P, grid) for (H, P) in holdout_HP]
    return {"acc": accuracy(y_true, y_pred), "macro_f1_present": macro_f1_present(y_true, y_pred), "grid_points": n * n}


def main():
    hard = load_json(SYSTEM_HARD_PATH)
    soft = load_json(SYSTEM_SOFT_PATH)
    system = merge_system(hard, soft)

    holdout = load_json(HOLDOUT_PATH)
    pts = holdout["points"]
    holdout_HP = [(float(pt["H"]), float(pt["P"])) for pt in pts]
    y_true = [ground_truth_soft(system, H, P) for (H, P) in holdout_HP]
    true_dist = dist_counts(y_true)

    # baselines once
    v31 = [v31_predict(system, H, P) for (H, P) in holdout_HP]
    v31_metrics = {"acc": accuracy(y_true, v31), "macro_f1_present": macro_f1_present(y_true, v31)}

    nn41 = nn_grid(system, holdout_HP, y_true, 41)
    nn81 = nn_grid(system, holdout_HP, y_true, 81)

    rows = []
    start = time.time()

    for seed in SEEDS:
        for N in SIZES:
            for strat in STRATS:
                rng = random.Random(1000000 + 1000 * seed + 7 * N + {"uniform": 1, "boundary": 2, "mixed": 3}[strat])
                ref_grid = build_reference(system, rng, N, strat)
                m = eval_one(system, holdout_HP, y_true, ref_grid)
                rows.append({"seed": seed, "N": N, "strategy": strat, **m})

    elapsed = time.time() - start

    artifact = {
        "test": "phase_e2_sample_efficiency",
        "true_dist": true_dist,
        "v31": v31_metrics,
        "nn41": nn41,
        "nn81": nn81,
        "rows": rows,
        "elapsed_seconds": elapsed
    }
    save_json(OUT_JSON, artifact)

    # summarize means over seeds
    def mean(xs: List[float]) -> float:
        return sum(xs) / max(1, len(xs))

    # group
    summary = {}
    for N in SIZES:
        for strat in STRATS:
            sel = [r for r in rows if r["N"] == N and r["strategy"] == strat]
            summary[(N, strat)] = {
                "acc_mean": mean([r["acc"] for r in sel]),
                "f1_mean": mean([r["macro_f1_present"] for r in sel]),
            }

    lines = []
    lines.append("# PHASE E2 — Sample Efficiency Report (soft labels)")
    lines.append("")
    lines.append(f"- holdout points: {len(pts)}")
    lines.append(f"- true dist: {true_dist}")
    lines.append(f"- seeds: {SEEDS}")
    lines.append(f"- sizes: {SIZES}")
    lines.append(f"- strategies: {STRATS}")
    lines.append(f"- pool_size: {POOL_SIZE}")
    lines.append(f"- elapsed_seconds: {elapsed:.2f}")
    lines.append("")
    lines.append("## Baselines")
    lines.append(f"- V3.1: acc={v31_metrics['acc']:.4f} | macroF1={v31_metrics['macro_f1_present']:.4f}")
    lines.append(f"- NN41: acc={nn41['acc']:.4f} | macroF1={nn41['macro_f1_present']:.4f}")
    lines.append(f"- NN81: acc={nn81['acc']:.4f} | macroF1={nn81['macro_f1_present']:.4f}")
    lines.append("")
    lines.append("## Results (mean over seeds)")
    lines.append("| N | strategy | acc_mean | macroF1_mean |")
    lines.append("|---:|---|---:|---:|")
    for N in SIZES:
        for strat in STRATS:
            s = summary[(N, strat)]
            lines.append(f"| {N} | {strat} | {s['acc_mean']:.4f} | {s['f1_mean']:.4f} |")

    lines.append("")
    lines.append("Artifact:")
    lines.append(f"- `{OUT_JSON.as_posix()}`")
    save_text(OUT_MD, "\n".join(lines))

    print("\n=== PHASE E2 COMPLETE ===")
    print(f"Report: {OUT_MD}")
    print(f"Artifact: {OUT_JSON}\n")


if __name__ == "__main__":
    main()
