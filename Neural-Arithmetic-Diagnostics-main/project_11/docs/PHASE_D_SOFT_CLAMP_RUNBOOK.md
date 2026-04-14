# PROJECT 11 — PHASE D RUNBOOK (Soft-Clamp / Homeostasis)

## Rules
- No installs / no venv / no deletions
- Do not edit locked holdout:
  `project_11/results/phase_c3_sat_margin/holdout_points.json`

## Commands
```powershell
cd "d:\Music\Project 03 Abacus\neural_arithmetic_diagnostics"
python -m py_compile project_11/experiments/phase_d_soft_clamp_evaluate.py
python project_11/experiments/phase_d_soft_clamp_evaluate.py
type project_11\results\phase_d_soft_clamp\report.md
```
