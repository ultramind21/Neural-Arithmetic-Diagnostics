from __future__ import annotations

import json
import hashlib
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
R = ROOT / "project_11" / "results"

OUT_DIR = R / "phase_e1_adaptive_nn"
OUT_PATH = OUT_DIR / "reference_points.json"

SEED = 551122
POOL_SIZE = 50000
N_UNIFORM = 1000
N_BOUNDARY = 1000

H_MIN, H_MAX = 0.0010, 0.0200
P_MIN, P_MAX = 0.2600, 0.4200


def save_json(p: Path, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def sample_uniform(rng: random.Random):
    return rng.uniform(H_MIN, H_MAX), rng.uniform(P_MIN, P_MAX)


def boundary_score_v3(H: float, P: float, sfs: list[float]) -> float:
    deltas = [0.80 * H + (0.30 - P) * sf for sf in sfs]
    gap_est = sum(deltas) / len(deltas)

    d_gap_fam = abs(gap_est - 0.005)
    d_gap_uni = abs(gap_est + 0.003)
    d_delta_fam = min(abs(d - 0.005) for d in deltas)
    d_delta_uni = min(abs(d + 0.005) for d in deltas)

    return min(d_gap_fam, d_gap_uni, d_delta_fam, d_delta_uni)


def main():
    rng = random.Random(SEED)
    used = set()
    points = []

    # shared_failure values from T4 system (fixed for selection; no ground truth used)
    sfs = [0.72, 0.65, 0.30, 0.28]

    # 1) uniform points
    while len(points) < N_UNIFORM:
        H, P = sample_uniform(rng)
        Hr, Pr = round(H, 6), round(P, 6)
        key = (Hr, Pr)
        if key in used:
            continue
        used.add(key)
        points.append({"id": f"e1_u{len(points)+1:04d}", "H": Hr, "P": Pr, "kind": "uniform"})

    # 2) boundary pool
    pool = []
    for _ in range(POOL_SIZE):
        H, P = sample_uniform(rng)
        Hr, Pr = round(H, 6), round(P, 6)
        bs = boundary_score_v3(Hr, Pr, sfs)
        pool.append((bs, Hr, Pr))
    pool.sort(key=lambda x: x[0])

    b_count = 0
    for bs, Hr, Pr in pool:
        if b_count >= N_BOUNDARY:
            break
        key = (Hr, Pr)
        if key in used:
            continue
        used.add(key)
        b_count += 1
        points.append({"id": f"e1_b{b_count:04d}", "H": Hr, "P": Pr, "kind": "boundary"})

    if b_count != N_BOUNDARY:
        raise SystemExit(f"FAIL: insufficient boundary points selected. got={b_count}")

    ref = {
        "test": "phase_e1_adaptive_nn",
        "created_date": "2026-04-10",
        "seed": SEED,
        "pool_size": POOL_SIZE,
        "n_uniform": N_UNIFORM,
        "n_boundary": N_BOUNDARY,
        "ranges": {"H": [H_MIN, H_MAX], "P": [P_MIN, P_MAX]},
        "points": points
    }

    save_json(OUT_PATH, ref)

    print("\n=== PHASE E1 REFERENCE GENERATED ===")
    print(f"seed: {SEED}")
    print(f"points: {len(points)} (uniform={N_UNIFORM}, boundary={N_BOUNDARY})")
    print("reference sha256:", sha256_file(OUT_PATH))
    print(f"saved: {OUT_PATH}\n")


if __name__ == "__main__":
    main()
