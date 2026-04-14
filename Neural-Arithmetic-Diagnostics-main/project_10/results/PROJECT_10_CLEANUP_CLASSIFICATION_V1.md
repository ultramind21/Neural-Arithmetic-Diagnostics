# PROJECT 10 CLEANUP CLASSIFICATION V1
## Canonical, Superseded, Unreviewed, Tools, and Delete Candidates

**Date:** April 2026  
**Project:** 10  
**Status:** ACTIVE CLEANUP CLASSIFICATION

---

## 1. Purpose

This document classifies the current Project 10 file surface into cleanup categories.

The purpose is to support a curated cleanup process that preserves scientific integrity while reducing clutter.

This classification is the reference point for any later move/archive/delete actions.

---

## 2. Category A — Keep (Canonical Core)

These files should remain in the main Project 10 surface because they define the official scientific or presentation state.

### Framework
- `framework/PROJECT_10_FRAMEWORK.md`
- `framework/PROJECT_10_LAW_CANDIDATES_V1.md`
- `framework/PROJECT_10_METHOD_REFINEMENT_PLAN.md`
- `framework/PROJECT_10_ADVERSARIAL_FALSIFICATION_PLAN.md`
- `framework/PROJECT_10_PHASE_2_PLAN.md`

### Core experiments and plans
- `experiments/PROJECT_10_FIRST_LAW_TEST_PLAN.md`
- `experiments/PROJECT_10_EVIDENCE_MATRIX_PLAN.md`
- `experiments/PROJECT_10_HIGHER_ORDER_LAW_TEST_PLAN.md`
- `experiments/PROJECT_10_LAW1_TEST_PLAN.md`
- `experiments/PROJECT_10_ADVERSARIAL_TEST_REGIMES_V1.md`
- `experiments/PROJECT_10_REGIME_A_SPEC_V1.md`
- `experiments/PROJECT_10_REGIME_A_V2_SPEC.md`
- `experiments/PROJECT_10_REGIME_B_SPEC_V1.md`
- `experiments/PROJECT_10_PHASE_2_TEST_MATRIX_PLAN.md`
- `experiments/PROJECT_10_THRESHOLD_REFINEMENT_PLAN_V1.md`
- `experiments/PROJECT_10_PHASE_DIAGRAM_REFINEMENT_PLAN_V1.md`

### Core scripts
- `experiments/project_10_law3_family_sensitive_rescue_test_v1.py`
- `experiments/project_10_law3_evidence_matrix_v1.py`
- `experiments/project_10_law1_evidence_matrix_v1.py`
- `experiments/project_10_higher_order_law_evidence_matrix_v1.py`
- `experiments/project_10_higher_order_law_break_test_v1.py`
- `experiments/project_10_regime_a_forced_universal_rescue_v1.py`
- `experiments/project_10_regime_a_forced_universal_rescue_v2.py`
- `experiments/project_10_regime_b_synthetic_homogeneous_families_v1.py`
- `experiments/project_10_regime_c_overpowered_universal_rescue_v1.py`
- `experiments/project_10_phase2_threshold_matrix_v1.py`
- `experiments/project_10_phase2_threshold_refinement_v1.py`
- `experiments/project_10_phase_diagram_refinement_v1.py`

### Canonical results
- `results/PROJECT_10_LAW1_STRONG_SUPPORT.md`
- `results/PROJECT_10_LAW3_STRONG_SUPPORT.md`
- `results/PROJECT_10_HIGHER_ORDER_STATUS_NOTE.md`
- `results/PROJECT_10_HIGHER_ORDER_BREAK_TEST_V1_RESULTS.md`
- `results/PROJECT_10_HIGHER_ORDER_CANDIDATE_STATUS_UPDATE_V2.md`
- `results/PROJECT_10_HIGHER_ORDER_CANDIDATE_REVISION_V1.md`
- `results/PROJECT_10_POST_ADVERSARIAL_SYNTHESIS_V1.md`
- `results/PROJECT_10_THEORY_STATUS_TABLE_V1.md`
- `results/PROJECT_10_PHASE_1_CLOSURE.md`
- `results/PROJECT_10_PHASE_2_THRESHOLD_MATRIX_RESULTS.md`
- `results/PROJECT_10_REGIME_SPACE_REFORMULATION_V1.md`
- `results/PROJECT_10_REGIME_SPACE_MAP_V1.md`
- `results/PROJECT_10_THRESHOLD_REFINEMENT_RESULTS_V1.md`
- `results/PROJECT_10_THRESHOLD_THEORY_NOTE_V1.md`
- `results/PROJECT_10_PHASE_DIAGRAM_V1.md`
- `results/PROJECT_10_PHASE_DIAGRAM_REFINEMENT_RESULTS_V1.md`
- `results/PROJECT_10_BOUNDARY_GEOMETRY_NOTE_V1.md`
- `results/PROJECT_10_PHASE_2_SYNTHESIS_V2.md`
- `results/PROJECT_10_CYCLE_STATUS_SUMMARY_V1.md`
- `results/PROJECT_10_PACKAGING_PLAN_V1.md`
- `results/PROJECT_10_PRESENTATION_SUMMARY_V2.md`
- `results/PROJECT_10_PHASE_DIAGRAM_ARTIFACT_SPEC_V1.md`
- `results/PROJECT_10_PHASE_DIAGRAM_ARTIFACT_TEXT_V1.md`
- `results/PROJECT_10_PHASE_DIAGRAM_ARTIFACT_LAYOUT_V1.md`
- `results/PROJECT_10_PHASE_DIAGRAM_ARTIFACT_RENDER_PLAN_V1.md`
- `results/PROJECT_10_PHASE_DIAGRAM_ARTIFACT_RENDERED_V1.md`
- `results/PROJECT_10_CLEANUP_PLAN_V1.md`

### Artifacts and reports
- all `*_artifact.json`
- all paired `*_report.md`
for the canonical experiment scripts above

---

## 3. Category B — Move to Superseded

These files are useful historically but should not remain in the main canonical view.

- `results/PROJECT_10_SYNTHESIS_V1.md`
- `results/PROJECT_10_PHASE_2_SYNTHESIS_V1.md`
- `results/PROJECT_10_PRESENTATION_SUMMARY_V1.md`

These should move to a `results/superseded/` location.

---

## 4. Category C — Move to Unreviewed Agent Outputs

These files were created during uncontrolled agent expansion and should not remain in the main canonical surface unless explicitly re-reviewed later.

- `results/PROJECT_10_ADVERSARIAL_FALSIFICATION_COMPLETE.md`
- `results/PROJECT_10_ADVERSARIAL_FALSIFICATION_PHASE_STATUS.md`
- `results/PROJECT_10_HIGHER_ORDER_CANDIDATE_STATUS_UPDATE_REGIME_B.md`
- `results/PROJECT_10_REGIME_B_V1_RESULTS.md`
- `results/PROJECT_10_REGIME_C_V1_RESULTS.md`

These should move to a location such as:
- `results/unreviewed_agent_outputs/`

---

## 5. Category D — Move to Tools or Archive

These files do not belong in the core Project 10 scientific surface.

- `generate_diagram.py`
- `merge_files.py`
- `project_tree.py`

These should move to a tools/archive location if still useful.

---

## 6. Category E — Delete Candidate

This file appears likely to be disposable or at least not part of the clean scientific surface:

- `neural_arithmetic_diagnosticss.md`

This should be reviewed one final time, and if confirmed as a local merged dump or redundant artifact, it can be deleted.

---

## 7. Immediate Next Step

The next step is:

- `project_10/results/PROJECT_10_CLEANUP_ACTION_PLAN_V1.md`

This should convert the classification into a concrete keep/move/archive/delete action sequence.

---
