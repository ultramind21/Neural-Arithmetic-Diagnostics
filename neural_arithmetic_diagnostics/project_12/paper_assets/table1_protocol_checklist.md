# Table 1: Project 12 Validation Protocol Checklist

| Step | Component | Purpose | Status |
|------|-----------|---------|--------|
| 1 | Claim Locking | Define observed + targets + status taxonomy upfront | ✅ FORMAL_CLAIMS.md |
| 2 | Baseline Definition | Establish pre-intervention performance perimeter | ✅ P11/P4 baselines |
| 3 | Metrics Specification | Per-family, per-seed, reproducible measurement | ✅ exact_match, macroF1 |
| 4 | Manifest Configuration | JSON-driven setup (schema + paths + hyperparams) | ✅ project_12/manifests/ |
| 5 | Output Safety | Results isolated to project_12/results/ | ✅ directory structure |
| 6 | Entrypoint Fidelity | Copy+patch discipline (diff gate ≥0.85) | ✅ diff_gate reports |
| 7 | Reproduction Check | Re-execute baseline procedures, verify match | ✅ REPRO_CHECK_*.md |
| 8 | Policy Validation | Non-comparison, use pre-registered thresholds | ✅ policy check scripts |
| 9 | Evidence Aggregation | Link all claims to reports + artifacts | ✅ EVIDENCE_INDEX.md |
| 10 | Sensitivity Analysis | Sweep seeds/configs to test robustness | ✅ C07 sweep + P4F sweep |
| 11 | Failures → Revisions | Rejected claims refined mechanistically | ✅ C07 → C07R |
| 12 | Closure Gate | Final decision rule per project | ✅ PROJECT_*_CLOSURE.md |

**Key insight:** Rigid protocol catches both false positives (C07 absolute threshold) and confirms robust patterns (C07R mechanisms, P4-C04 narrow transfer across seeds).
