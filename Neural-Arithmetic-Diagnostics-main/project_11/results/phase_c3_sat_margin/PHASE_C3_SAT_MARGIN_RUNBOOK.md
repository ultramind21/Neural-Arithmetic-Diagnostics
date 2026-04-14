# PHASE C3 SAT-MARGIN RUNBOOK

## Overview
This runbook provides step-by-step instructions to execute, monitor, and verify Phase C3 (saturation-aware margins test).

---

## STEP 1: Pre-flight Checks

### 1.1 Verify Phase C3 Directory Structure
```bash
type d:\Music\Project 03 Abacus\neural_arithmetic_diagnostics\project_11\results\phase_c3_sat_margin\
```
Expected: Directory exists (created by `phase_c3_generate_holdout.py`)

### 1.2 Verify Files Present
- `PHASE_C3_SAT_MARGIN_PROTOCOL.md` (this directory, explains design)
- `transfer_t4_system.json` (loaded by both scripts)
- `transfer_t4_large\preds_v3.json` (reference, not used by C3)

### 1.3 Python Syntax Validation (Required before execution)
```bash
cd d:\Music\Project 03 Abacus\neural_arithmetic_diagnostics
python -m py_compile project_11/experiments/phase_c3_generate_holdout.py
python -m py_compile project_11/experiments/phase_c3_evaluate.py
```
Expected: No errors (silent pass)

---

## STEP 2: Generate Holdout (Seed = 223311)

### 2.1 Execute Generator Script
```bash
python project_11/experiments/phase_c3_generate_holdout.py
```

### 2.2 Expected Output
```
=== PHASE C3 HOLDOUT GENERATED ===
samples generated: 400 uniform, 400 boundary-focused
total points: 800
seed: 223311
holdout_sha256: [hex string]
output: d:\Music\Project 03 Abacus\neural_arithmetic_diagnostics\project_11\results\phase_c3_sat_margin\holdout_points.json
```

### 2.3 Save SHA256 Hash
Record the `holdout_sha256` value here (immutable after generation):
```
Holdout SHA256: _________________________________
```
**CRITICAL**: Do NOT modify holdout_points.json after this point.

### 2.4 Verify Holdout Structure
```bash
cd d:\Music\Project 03 Abacus\neural_arithmetic_diagnostics
python -c "import json; d=json.load(open('project_11/results/phase_c3_sat_margin/holdout_points.json')); print(f\"Points: {len(d['points'])} | seed: {d.get('seed')} | sha256: {d.get('sha256')}\")"
```
Expected: Points: 800 | seed: 223311 | sha256: [matches recorded value]

---

## STEP 3: Evaluate on Holdout

### 3.1 Execute Evaluator Script
```bash
python project_11/experiments/phase_c3_evaluate.py
```

### 3.2 Expected Output
```
=== PHASE C3 EVALUATION COMPLETE ===
Report: d:\Music\Project 03 Abacus\neural_arithmetic_diagnostics\project_11\results\phase_c3_sat_margin\report.md
Artifact: d:\Music\Project 03 Abacus\neural_arithmetic_diagnostics\project_11\results\phase_c3_sat_margin\artifact.json
```

### 3.3 Verify Artifacts Created
```bash
type project_11\results\phase_c3_sat_margin\report.md
```
Expected: Report table with 4 rows (overall, subsets) showing V3, V3.1, NN11 metrics.

---

## STEP 4: Verify Success Criteria

### 4.1 Open Artifact
```bash
cd project_11/results/phase_c3_sat_margin
type artifact.json
```

### 4.2 Check Metrics (Python snippet to extract):
```python
import json
a = json.load(open('artifact.json'))
m = a['metrics']['overall']

v3_f1 = m['v3_macro_f1']
v31_f1 = m['v31_macro_f1']
gain = v31_f1 - v3_f1

print(f"V3 macro-F1:    {v3_f1:.4f}")
print(f"V3.1 macro-F1:  {v31_f1:.4f}")
print(f"Gain (V3.1-V3): {gain:+.4f}")
print(f"Criterion (>0.03): {'PASS ✓' if gain > 0.03 else 'FAIL ✗'}")

e = a['error_sat']
print(f"\nV3  sat-errors: {e['v3']['errors_with_sat']} / {e['v3']['errors']}")
print(f"V3.1 sat-errors: {e['v31']['errors_with_sat']} / {e['v31']['errors']}")
```

### 4.3 Success Criterion
✓ **PASS** if:
  - `v31_f1 - v3_f1 > 0.03` (3% gain in macro-F1)
  - `v31_sat_errors < v3_sat_errors` (reduced saturation-linked errors)

✗ **FAIL** if either condition unmet.

---

## STEP 5: Archive & Report

### 5.1 Record Results
- Phase: C3 Saturation-Aware Margins
- Holdout: 800 points (seed=223311)
- Holdout SHA256: `_________________________________`
- V3 macro-F1: _____________
- V3.1 macro-F1: _____________
- Gain: _____________
- Verdict: [ ] PASS [ ] FAIL

### 5.2 Cleanup Interpreter Cache (Optional)
```bash
cd project_11/experiments
del __pycache__\phase_c3_generate_holdout* /q
del __pycache__\phase_c3_evaluate* /q
```

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `FileNotFoundError: transfer_t4_system.json` | Ensure `project_11/results/transfer_t4_system.json` exists |
| `SyntaxError: invalid syntax` | Run `py_compile` (STEP 1.3) to locate exact line |
| `holdout.json missing` | Re-run generator (STEP 2) before evaluator |
| `macro-F1 ≈ 0.333` (random baseline) | Verify system.json labels match ground_truth return values |

---

## Timeline Estimate
- STEP 1: 1 minute (checks)
- STEP 2: 2 minutes (generation)
- STEP 3: 30–60 seconds (evaluation)
- STEP 4: 2 minutes (verification)
- **Total: ~5 minutes**

---

## References
- Protocol: `PHASE_C3_SAT_MARGIN_PROTOCOL.md`
- T4-Large baseline: `transfer_t4_large_evaluate.py`
- C1 noise sweep: `phase_c1_noise_sweep.py`
- C2 MC voting: `phase_c2_noise_aware_v3_mc.py`
