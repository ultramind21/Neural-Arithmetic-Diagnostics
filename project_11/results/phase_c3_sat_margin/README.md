# Phase C3: Saturation-Aware Margins Test

## Quick Summary
Test whether expanding Rule V3 decision thresholds under saturation risk (pre-clamp raw ≥ 1.0) improves performance on new 800-point holdout (seed 223311).

**Design:** Minimal structural change (margins only, no ground-truth reimplementation).

---

## Files in This Directory

| File | Purpose |
|------|---------|
| `PHASE_C3_SAT_MARGIN_PROTOCOL.md` | Experimental design & statistical justification |
| `PHASE_C3_SAT_MARGIN_RUNBOOK.md` | Step-by-step execution instructions |
| `holdout_points.json` | 800-point test set (generated, locked by SHA256) |
| `artifact.json` | Metrics & results (auto-generated) |
| `report.md` | Human-readable summary (auto-generated) |
| `README.md` | This file |

---

## Execution Flow

1. **Generate holdout** (`phase_c3_generate_holdout.py`)
   - Creates 800 new points: 400 uniform, 400 boundary-focused
   - Seed = 223311 (locked)
   - Outputs: `holdout_points.json`, SHA256 hash

2. **Evaluate** (`phase_c3_evaluate.py`)
   - Compares V3-hard vs V3.1-sat-margin vs NN11 baseline on holdout
   - Tracks: overall accuracy, macro-F1, subsets (uniform/boundary/saturation)
   - Outputs: `report.md`, `artifact.json`

3. **Analyze**
   - Success: V3.1 macro-F1 > V3-hard by +0.03 (3% gain)
   - AND: V3.1 reduces saturation-linked errors

---

## Key Concepts

### Why Saturation Risk Matters
From T4-Large postmortem: **100% of 80 V3 errors were associated with sat_uni > 0 or sat_fam > 0**.

Saturation risk: count of families where **pre-clamp raw score ≥ 1.0**.
- Raw score = base + P×sf (universal) or base + 0.30×sf + 0.80×H (family)
- When clamp activates (raw ≥ 1.0 → clamped to 1.0), information is destroyed
- Hard thresholds in compressed gap space fail near clamp boundaries

### V3.1 Modification
Expand decision margins when sat_risk ≥ 1 (at least one family near saturation):
- **Normal:** gap_fam > 0.005, gap_uni < -0.003, wins_margin = ±0.005
- **Saturated:** gap_fam > 0.0065, gap_uni < -0.0045, wins_margin = ±0.0065
- Effect: "be more conservative near clamp boundaries"

---

## Expected Results

| Scenario | Expected |
|----------|----------|
| V3.1 significantly better | V3.1 macro-F1 ≥ V3 + 0.03 |
| V3.1 eliminates sat-errors | V3.1 sat-linked errors < V3 sat-linked errors |
| Boundary subset improves | V3.1 on boundary ≈ uniform (closer to NN11) |
| Uniform subset unchanged | V3.1 on uniform ≈ V3 (margins don't affect low-sat) |

---

## Previous Phases Status

| Phase | Result | Verdict |
|-------|--------|---------|
| T4-Large | V3 0.8575 vs NN 0.9050 | **FAIL**: V3 underperforms |
| C1 Noise Sweep | V3 robust hypothesis tested | **DISPROVEN**: V3 degrades faster |
| C2 MC Voting | Uncertainty mitigation tested | **NO GAIN**: V3-MC ≈ V3-hard |
| C3 Sat-Margin | Structural fix tested | **PENDING** (current phase) |

---

## How to Run

### Prerequisites
- Python 3.7+
- No dependencies beyond stdlib
- `transfer_t4_system.json` present in `project_11/results/`

### Quick Start
```bash
cd d:\Music\Project 03 Abacus\neural_arithmetic_diagnostics

# Syntax check
python -m py_compile project_11/experiments/phase_c3_generate_holdout.py
python -m py_compile project_11/experiments/phase_c3_evaluate.py

# Generate
python project_11/experiments/phase_c3_generate_holdout.py

# Evaluate
python project_11/experiments/phase_c3_evaluate.py

# View report
type project_11\results\phase_c3_sat_margin\report.md
```

### Full Runbook
See `PHASE_C3_SAT_MARGIN_RUNBOOK.md` for detailed step-by-step instructions.

---

## Success Criteria

### Criterion 1: Macro-F1 Gain
```
Δ = V3.1_macro_f1 - V3_macro_f1
PASS if Δ > 0.03 (3% absolute gain)
```

### Criterion 2: Saturation-Error Reduction
```
V31_sat_errors < V3_sat_errors
(fewer errors in regions where saturation risk ≥ 1)
```

### Verdict
- ✓ **PASS** if both criteria met → V3.1 addresses saturation problem
- ✗ **FAIL** if either unmet → saturation margins insufficient, consider C4 or pivot

---

## Next Steps (After C3)

If **PASS**:
- Optional C4: Test V3.1 on full interpolated dataset (not 11×11 grid)
- Optional C5: Compare V3.1 vs NN11 on highest-saturation subset

If **FAIL**:
- Consider alternative fix: re-train NN on clamped-aware loss
- Or: accept NN11 as superior architecture for clamped systems

---

## Artifact Format

### artifact.json Structure
```json
{
  "test": "phase_c3_sat_margin",
  "seed": 223311,
  "n_total": 800,
  "metrics": {
    "overall": {
      "v3_acc": 0.8575,
      "v3_macro_f1": 0.8575,
      "v31_acc": 0.8925,
      "v31_macro_f1": 0.8925,
      "nn11_acc": 0.9050,
      "nn11_macro_f1": 0.9050
    },
    "subsets": {
      "uniform": {...},
      "boundary": {...},
      "sat_risk_ge1": {...},
      "sat_risk_0": {...}
    }
  },
  "error_sat": {
    "v3": {"errors": 68, "errors_with_sat": 68},
    "v31": {"errors": 48, "errors_with_sat": 34}
  }
}
```

---

## References

- **Postmortem Discovery**: 100% V3 errors linked to saturation
- **System Config**: 4 families, T4 ranges [0.001,0.020]×[0.260,0.420]
- **V3 Algorithm**: Gap-based classification with delta averaging
- **V3.1 Modification**: Sat-risk conditional thresholds
- **NN11 Baseline**: 11×11 grid + normalized nearest-neighbor

---

## Author Notes

Phase C3 represents a **principled, minimal-change fix** to address the postmortem finding. Unlike C1 (robustness hypothesis) and C2 (procedural uncertainty), C3 targets the architectural root cause: hard thresholds fail in clamped regions.

If C3 succeeds, V3.1 becomes viable for practical use. If not, accept NN11 or explore alternative architectures (e.g., soft margins, clamping-aware loss functions).

**Key Principle**: No rewrite of ground truth, no post-hoc overfitting—only margin adjustment under statistically identifiable saturation risk.
