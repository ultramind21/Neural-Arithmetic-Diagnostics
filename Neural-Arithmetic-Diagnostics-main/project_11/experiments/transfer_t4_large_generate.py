from __future__ import annotations

import json
import hashlib
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
P11_RESULTS = ROOT / "project_11" / "results"

SYSTEM_PATH = P11_RESULTS / "transfer_t4_system.json"

OUT_DIR = P11_RESULTS / "transfer_t4_large"
HOLDOUT_OUT = OUT_DIR / "holdout_points.json"
PRED_OUT = OUT_DIR / "predictions.json"

SEED = 114211  # LOCKED
N_TOTAL = 500
N_UNIFORM = 250
N_BOUNDARY = 250

# Holdout sampling ranges
H_MIN, H_MAX = 0.0010, 0.0200
P_MIN, P_MAX = 0.2600, 0.4200

# Boundary pool approach (bounded runtime)
BOUNDARY_POOL = 60000  # LOCKED


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


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


def boundary_score(system: dict, H: float, P: float) -> float:
    """
    Smaller => closer to internal Rule V3 boundaries.
    Uses ONLY Rule V3 quantities (no ground truth).
    """
    sfs = [float(f["shared_failure"]) for f in system["families"]]
    deltas = [0.80 * H + (0.30 - P) * sf for sf in sfs]
    gap_est = sum(deltas) / len(deltas)

    # Distance to key thresholds
    d_gap_fam = abs(gap_est - 0.005)
    d_gap_uni = abs(gap_est + 0.003)
    d_delta_fam = min(abs(d - 0.005) for d in deltas)
    d_delta_uni = min(abs(d + 0.005) for d in deltas)

    return min(d_gap_fam, d_gap_uni, d_delta_fam, d_delta_uni)


def sample_uniform(rng: random.Random) -> tuple[float, float]:
    H = rng.uniform(H_MIN, H_MAX)
    P = rng.uniform(P_MIN, P_MAX)
    return H, P


def sample_boundary_pool(system: dict, rng: random.Random, pool_size: int) -> List[Tuple[float, float]]:
    """
    Generate a pool of candidates and return the closest-to-boundary ones.
    Bounded by pool_size to ensure reasonable runtime.
    """
    pool = []
    for _ in range(pool_size):
        H, P = sample_uniform(rng)
        Hr, Pr = round(H, 6), round(P, 6)
        bs = boundary_score(system, Hr, Pr)
        pool.append((bs, Hr, Pr))
    pool.sort(key=lambda x: x[0])  # Sort by boundary score ascending
    return pool


def main():
    system = load_json(SYSTEM_PATH)
    rng = random.Random(SEED)

    used = set()  # (H,P) rounded to 6 decimals
    points = []

    # 1) Uniform points
    while len(points) < N_UNIFORM:
        H, P = sample_uniform(rng)
        Hr, Pr = round(H, 6), round(P, 6)
        key = (Hr, Pr)
        if key in used:
            continue
        used.add(key)
        points.append({"id": f"t4L_u{len(points)+1:03d}", "H": Hr, "P": Pr, "kind": "uniform"})

    # 2) Boundary-focused via pool selection (bounded)
    pool = sample_boundary_pool(system, rng, BOUNDARY_POOL)

    b_count = 0
    for bs, Hr, Pr in pool:
        if b_count >= N_BOUNDARY:
            break
        key = (Hr, Pr)
        if key in used:
            continue
        used.add(key)
        b_count += 1
        points.append({"id": f"t4L_b{b_count:03d}", "H": Hr, "P": Pr, "kind": "boundary"})

    if b_count != N_BOUNDARY:
        raise SystemExit(f"FAIL: boundary pool insufficient unique points. got={b_count}, need={N_BOUNDARY}")

    if len(points) != N_TOTAL:
        raise SystemExit(f"FAIL: point count mismatch. got={len(points)}, need={N_TOTAL}")

    # Build holdout
    holdout = {
        "test": "transfer_t4_large_rule_v3",
        "created_date": "2026-04-10",
        "seed": SEED,
        "n_total": N_TOTAL,
        "n_uniform": N_UNIFORM,
        "n_boundary_focused": N_BOUNDARY,
        "ranges": {"H": [H_MIN, H_MAX], "P": [P_MIN, P_MAX]},
        "boundary_pool": BOUNDARY_POOL,
        "points": points
    }

    # Build predictions (Rule V3 only)
    preds = []
    counts = {"family-aware region": 0, "transition region": 0, "universal region": 0}

    for pt in points:
        H = float(pt["H"])
        P = float(pt["P"])
        lbl = rule_v3_predict(system, H, P)
        counts[lbl] += 1
        preds.append({
            "id": pt["id"],
            "H": pt["H"],
            "P": pt["P"],
            "predicted_region": lbl,
            "confidence": "high" if pt["kind"] == "uniform" else "medium"
        })

    pred_obj = {
        "test": "transfer_t4_large_rule_v3",
        "created_date": "2026-04-10",
        "lock_note": "Generated by Rule V3 only. Do not edit after generation.",
        "seed": SEED,
        "predictions": preds
    }

    save_json(HOLDOUT_OUT, holdout)
    save_json(PRED_OUT, pred_obj)

    print("\n=== T4-LARGE GENERATION COMPLETE ===")
    print(f"seed: {SEED}")
    print(f"points: {N_TOTAL} (uniform={N_UNIFORM}, boundary={N_BOUNDARY})")
    print("predicted label counts:", counts)
    print("holdout sha256:", sha256_file(HOLDOUT_OUT))
    print("preds   sha256:", sha256_file(PRED_OUT))
    print(f"saved: {HOLDOUT_OUT}")
    print(f"saved: {PRED_OUT}\n")


if __name__ == "__main__":
    main()
