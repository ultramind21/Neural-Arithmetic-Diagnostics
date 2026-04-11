# EVALUATION_SPEC — Unified Metrics & Rules
Project 12

## 1) Core metrics (required)
### Performance
- Accuracy (for discrete correctness tasks)
- Macro-F1 (only when class imbalance or family classification is primary)

### Efficiency / cost proxies
- #samples used (reference points / retrieval pool size / training samples used by method)
- #forward passes (if measured)
- optional: wall-clock time (must specify hardware)

### Stability
- Mean ± std over runs (required)
- Failure rate variance across seeds (required)

### Failure structure (required in this project)
- Failure rate per family (or per regime bucket)
- Worst-family performance (min across families)
- Generalization gap (train vs test, or in-distribution vs holdout)

## 2) Baseline definitions (must be explicit)
When comparing:
- "dense" means: fixed grid at specified resolution
- "uniform" means: random uniform sampling from specified bounds with fixed N
- "boundary" means: sampling concentrated near defined discontinuities / boundary bands
- "mixed/structured" means: explicitly weighted mixture, weights must be recorded
- "kNN standard" means: define embedding/feature space + k + retrieval set membership (train-only)

## 3) Leakage prevention rules (non-negotiable)
- Test/holdout points must never be used to:
  - build retrieval memory
  - tune hyperparameters
  - select thresholds
  - choose sampling weights
- Any selection must be based on:
  - train set only, or
  - a separate validation set (explicitly labeled)

## 4) Run policy
- Each evaluated point must run with a fixed seed list.
- Default: 10 runs unless compute forces reduction; if reduced, must justify in summary.

## 5) Reporting format (standard)
Each experiment must output:
- artifact.json (raw metrics + config + run metadata)
- report.md (short, evidence-only)
- summary table row (for aggregation)

## 6) Acceptance criteria style
All claims must define pass/fail in terms of:
- Δ performance threshold and/or ≤ ε degradation constraint
- ≥ X% efficiency gain constraint
- stability constraint (e.g., std below threshold or failure rate not exploding)
