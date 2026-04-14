# PROJECT 11 — PHASE E2
## Sample-Efficiency Curve + Ablations (Soft labels)

**Date:** April 2026  
**Status:** DRAFT → LOCKED after generation  
**Test:** phase_e2_sample_efficiency

---

## 0) Purpose

Quantify how reference set size and sampling strategy affects NN performance under soft-clamp labels.

We evaluate:
- Uniform-only
- Boundary-only (V3 boundary score)
- Mixed (50/50)

Across multiple reference sizes and seeds.

---

## 1) Fixed components

- Holdout (evaluation set): `project_11/results/phase_c3_sat_margin/holdout_points.json` (800 pts)
- System:
  - hard families + thresholds: `project_11/results/transfer_t4_system.json`
  - soft clamp k: `project_11/results/phase_d_soft_clamp/system_soft_clamp.json`
- Ground truth labels: softplus-based soft clamp (as in Phase E1)

- Baselines reported:
  - V3.1
  - NN41
  - NN81

---

## 2) Reference sizes (N)

N ∈ {250, 500, 1000, 1500, 2000}

---

## 3) Strategies

For each (N, seed):

A) uniform-only:
- N uniform points

B) boundary-only:
- N boundary-focused points selected from a fixed pool using V3 boundary score

C) mixed:
- N/2 uniform + N/2 boundary-focused

---

## 4) Seeds (LOCKED)

Seeds: {101, 202, 303}

---

## 5) Outputs

Folder:
- `project_11/results/phase_e2_sample_efficiency/`

Files:
- `artifact.json`
- `report.md`

This phase does not create 100s of JSON reference files; it generates reference sets in-memory deterministically per (N, seed, strategy) and reports aggregate results.

---
