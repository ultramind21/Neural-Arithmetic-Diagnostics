# PROJECT 11 — PHASE E1 RUNBOOK (Adaptive NN)

## Rules
- No installs / no venv / no deletions
- Do not edit reference_points.json after SHA256 is printed

## Commands
```powershell
cd "d:\Music\Project 03 Abacus\neural_arithmetic_diagnostics"
python -m py_compile project_11/experiments/phase_e1_generate_reference_points.py
python -m py_compile project_11/experiments/phase_e1_evaluate.py
python project_11/experiments/phase_e1_generate_reference_points.py
python project_11/experiments/phase_e1_evaluate.py
type project_11\results\phase_e1_adaptive_nn\report.md
```
