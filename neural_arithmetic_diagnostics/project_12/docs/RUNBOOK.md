# RUNBOOK — Project 12 Execution Checklist

## Step 0 — Freeze
- Create a dedicated branch: project12-validation
- Record:
  - git commit hash
  - python/torch versions
  - device info

## Step 1 — Claim locking
- Populate FORMAL_CLAIMS.md for Projects 4–11.
- Each claim must define baselines + acceptance criteria.

## Step 2 — Baseline verification
- Implement or reuse baselines.
- Verify baseline correctness on small sanity tasks.

## Step 3 — Controlled grid runs
- Run manifest-driven grid with fixed seeds.
- Store all outputs under project_12/results/.

## Step 4 — Stability & failure analysis
- Aggregate mean ± std
- Failure per family
- Worst-family stats

## Step 5 — Ablations
- Remove one component at a time (as per claim scope).
- Re-run minimal grid.

## Step 6 — Compression
- Produce:
  - Validated claims
  - Conditional claims (with conditions)
  - Rejected claims
