# Phase 3 v2: Cross‑Distribution Evaluation

## Overview

Phase 3 v2 introduces **cross-distribution evaluation**: a trained model's ability to generalize from one problem distribution (no_carry or carry_heavy) to another without retraining.

## Experiments

For each training mode (no_carry or carry_heavy), we:
1. Train a Transformer policy on that mode (e.g., 3000 examples).
2. Evaluate on both in-distribution and out-of-distribution modes (1000 examples each).

This measures **transfer learning** within the addition domain.

## Output Artifacts

- `artifact.json`: Contains train/eval modes, per-mode accuracies, and git traceability.
- `report.md`: Markdown table of per-mode results.

## Note

This is **exploratory work**, not a validated claim. Results inform future decision-making on environment design.
