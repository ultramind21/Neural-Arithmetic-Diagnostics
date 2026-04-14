# VALIDATION_PROTOCOL — Project 12
Neural-Arithmetic-Diagnostics

## Purpose
Convert Projects 4–11 into reproducible, baseline-grounded, statistically reported claims.

## Non-negotiable rules
1) **Claim-lock before experiments**
   - No experiment is "valid" unless it maps to a Claim ID in FORMAL_CLAIMS.md.

2) **Baseline-first**
   - Every claim must be evaluated against at least one external/standard baseline:
     - random / uniform / dense (as applicable)
     - kNN standard retrieval baseline (where retrieval exists)
     - naive heuristics baseline (only if relevant & explicitly defined)

3) **Read-only legacy projects**
   - `project_4/` ... `project_11/` are treated as read-only.
   - Any required bug fix requires:
     - minimal patch
     - documented justification
     - re-freeze tag/commit note in Project 12 docs

4) **Manifest-driven execution**
   - Every run must have a manifest describing:
     - claim_id, experiment_id
     - dataset/task spec
     - method variant (sampling, clamp, k, noise, etc.)
     - seed list
     - number of runs
     - output directory

5) **Reproducibility logging**
   Each run must record:
   - git commit hash
   - timestamp
   - python version
   - torch version
   - device info (cpu/gpu if available)
   - manifest content hash

6) **Statistical reporting**
   - Never report single-run results as conclusions.
   - Minimum: mean ± std over runs.
   - Prefer: bootstrap CI for key metrics (when feasible).

7) **Result destinations**
   - Raw artifacts: `project_12/results/<experiment_id>/raw/`
   - Summaries:     `project_12/results/<experiment_id>/summary.md`
   - Aggregations:  `project_12/reports/`

## Definition of Done (Project 12)
Project 12 is complete when:
- Every claim has: baselines + metrics + acceptance criteria + run count + evidence pointers.
- A "Validated Results" snapshot exists (evidence-only).
- Rejected/conditional claims are explicitly listed.
