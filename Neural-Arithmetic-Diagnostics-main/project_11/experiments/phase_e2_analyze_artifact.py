from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "project_11" / "results" / "phase_e2_sample_efficiency" / "artifact.json"
OUT_MD = ROOT / "project_11" / "results" / "phase_e2_sample_efficiency" / "ANALYSIS.md"


def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def save_text(p: Path, s: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")


def mean(xs):
    return sum(xs) / max(1, len(xs))


def stdev(xs):
    if len(xs) < 2:
        return 0.0
    m = mean(xs)
    return (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5


def main():
    a = load_json(ARTIFACT)
    rows = a["rows"]

    # group by (N,strategy)
    g = defaultdict(list)
    # group by (seed,N,strategy)
    gs = defaultdict(list)

    for r in rows:
        key = (r["N"], r["strategy"])
        g[key].append(r["macro_f1_present"])
        gs[(r["seed"], r["N"], r["strategy"])].append(r["macro_f1_present"])

    Ns = sorted({r["N"] for r in rows})
    strats = ["uniform", "boundary", "mixed"]
    seeds = sorted({r["seed"] for r in rows})

    lines = []
    lines.append("# PHASE E2 — Artifact Analysis")
    lines.append("")
    lines.append(f"- rows: {len(rows)}")
    lines.append(f"- elapsed_seconds: {a.get('elapsed_seconds', 'unknown')}")
    lines.append("")
    lines.append("## Baselines (from artifact)")
    lines.append(f"- true_dist: {a.get('true_dist')}")
    lines.append(f"- V3.1: {a.get('v31')}")
    lines.append(f"- NN41: {a.get('nn41')}")
    lines.append(f"- NN81: {a.get('nn81')}")
    lines.append("")
    lines.append("## Mean ± sd over seeds (macroF1_present)")
    lines.append("| N | strategy | mean | sd |")
    lines.append("|---:|---|---:|---:|")
    for N in Ns:
        for s in strats:
            xs = g[(N, s)]
            lines.append(f"| {N} | {s} | {mean(xs):.4f} | {stdev(xs):.4f} |")

    lines.append("")
    lines.append("## Per-seed table (macroF1_present)")
    lines.append("| seed | N | uniform | boundary | mixed |")
    lines.append("|---:|---:|---:|---:|---:|")
    for seed in seeds:
        for N in Ns:
            vals = {}
            for s in strats:
                xs = gs[(seed, N, s)]
                vals[s] = xs[0] if xs else None
            lines.append(f"| {seed} | {N} | {vals['uniform']:.4f} | {vals['boundary']:.4f} | {vals['mixed']:.4f} |")

    # monotonicity quick check for each strategy (on means)
    def is_non_decreasing(seq):
        return all(seq[i] <= seq[i+1] + 1e-12 for i in range(len(seq)-1))

    lines.append("")
    lines.append("## Monotonicity check on mean curve")
    for s in strats:
        seq = [mean(g[(N, s)]) for N in Ns]
        lines.append(f"- {s}: non-decreasing = {is_non_decreasing(seq)} | means = {[round(x,4) for x in seq]}")

    save_text(OUT_MD, "\n".join(lines))
    print("\n=== PHASE E2 ANALYSIS COMPLETE ===")
    print(f"Artifact: {ARTIFACT}")
    print(f"Analysis: {OUT_MD}\n")


if __name__ == "__main__":
    main()
