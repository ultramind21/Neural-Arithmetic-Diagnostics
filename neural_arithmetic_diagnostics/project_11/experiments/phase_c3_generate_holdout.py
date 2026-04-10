from __future__ import annotations

import json
import hashlib
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P11_RESULTS = ROOT / "project_11" / "results"

OUT_DIR = P11_RESULTS / "phase_c3_sat_margin"
HOLDOUT_OUT = OUT_DIR / "holdout_points.json"

SEED = 223311
N_TOTAL = 800
N_UNIFORM = 400
N_BOUNDARY = 400

H_MIN, H_MAX = 0.0010, 0.0200
P_MIN, P_MAX = 0.2600, 0.4200

BOUNDARY_POOL = 90000  # bounded runtime


def save_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def sample_uniform(rng: random.Random):
    return rng.uniform(H_MIN, H_MAX), rng.uniform(P_MIN, P_MAX)


def v3_boundary_score(H: float, P: float, sfs: list[float]) -> float:
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

    # NOTE: boundary score only needs shared_failure values; hardcode from T4 system
    sfs = [0.72, 0.65, 0.30, 0.28]

    # Uniform
    while len(points) < N_UNIFORM:
        H, P = sample_uniform(rng)
        Hr, Pr = round(H, 6), round(P, 6)
        key = (Hr, Pr)
        if key in used:
            continue
        used.add(key)
        points.append({"id": f"c3_u{len(points)+1:04d}", "H": Hr, "P": Pr, "kind": "uniform"})

    # Boundary pool selection
    pool = []
    for _ in range(BOUNDARY_POOL):
        H, P = sample_uniform(rng)
        Hr, Pr = round(H, 6), round(P, 6)
        bs = v3_boundary_score(Hr, Pr, sfs)
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
        points.append({"id": f"c3_b{b_count:04d}", "H": Hr, "P": Pr, "kind": "boundary"})

    if b_count != N_BOUNDARY:
        raise SystemExit(f"FAIL: boundary pool insufficient. got={b_count}")

    holdout = {
        "test": "phase_c3_sat_margin",
        "created_date": "2026-04-10",
        "seed": SEED,
        "n_total": N_TOTAL,
        "n_uniform": N_UNIFORM,
        "n_boundary": N_BOUNDARY,
        "ranges": {"H": [H_MIN, H_MAX], "P": [P_MIN, P_MAX]},
        "points": points
    }

    save_json(HOLDOUT_OUT, holdout)

    print("\n=== PHASE C3 HOLDOUT GENERATED ===")
    print(f"seed: {SEED}")
    print(f"points: {N_TOTAL} (uniform={N_UNIFORM}, boundary={N_BOUNDARY})")
    print("holdout sha256:", sha256_file(HOLDOUT_OUT))
    print(f"saved: {HOLDOUT_OUT}\n")


if __name__ == "__main__":
    main()
