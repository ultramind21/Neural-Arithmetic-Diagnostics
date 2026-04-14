# Project 12 — Phase 2 Diversification (Tiny Transformer)

## Goal

Run a minimal Transformer policy baseline on the existing Soroban addition environment and produce a reproducible artifact + report under `project_12/results/phase2_transformer_smoke/`.

This is an experiment baseline (not a validated claim). Claim status remains governed by Project 12 authority rules.

## Outputs

- `artifact.json` — metrics + config + commit hash
- `report.md` — short summary of training and evaluation

## Approach

- Generate dataset from teacher via `teacher_trace(...)`
- Train Transformer for 1–3 epochs on (observation, action) pairs
- Evaluate action accuracy on holdout set
- Record config, seed, dataset size, metrics in artifact

## Non-Goals

- Large-scale training (smoke run only)
- Checkpoint persistence (optional)
- New claims about Soroban solving
