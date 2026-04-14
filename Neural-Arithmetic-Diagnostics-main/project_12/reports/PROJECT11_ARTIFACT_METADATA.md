# PROJECT11_ARTIFACT_METADATA

**Purpose:** Audit trail of Project 11 artifact structure and metadata completeness.

**Date:** 2026-04-11  
**Inspection method:** Read-only Python script (inspect_project11_artifacts.py)  

---

## Summary (All Artifacts)

| Artifact | Exists | Size (bytes) | Error | Metadata gaps |
|---|---|---|---|---|
| Phase D (Soft Clamp Resolution Sweep) | ✅ | 8090 | None | git_hash, git_branch, timestamp, environment |
| Phase E2 (Sample Efficiency) | ✅ | 7270 | None | git_hash, git_branch, timestamp, environment |
| Phase E3 (Ratio + kNN) | ✅ | 8141 | None | git_hash, git_branch, timestamp, environment |

---

## Phase D (Soft Clamp Resolution Sweep)

**File:** `D:\Music\Project 03 Abacus\neural_arithmetic_diagnostics\project_11\results\phase_d_soft_clamp\RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`  
**Exists:** True  
**Size:** 8090 bytes  

**Top-level fields:**
  - k
  - points
  - true_dist
  - rules
  - nn
  - nn_grid_build

**Missing expected fields:** results, metadata, timestamp, git_hash

**Metadata gaps (missing in artifact.metadata):** git_hash, git_branch, timestamp, environment

---

## Phase E2 (Sample Efficiency)

**File:** `D:\Music\Project 03 Abacus\neural_arithmetic_diagnostics\project_11\results\phase_e2_sample_efficiency\artifact.json`  
**Exists:** True  
**Size:** 7270 bytes  

**Top-level fields:**
  - test
  - true_dist
  - v31
  - nn41
  - nn81
  - rows
  - elapsed_seconds

**Missing expected fields:** results, metadata, timestamp

**Metadata gaps (missing in artifact.metadata):** git_hash, git_branch, timestamp, environment

---

## Phase E3 (Ratio + kNN)

**File:** `D:\Music\Project 03 Abacus\neural_arithmetic_diagnostics\project_11\results\phase_e3_ratio_knn\artifact.json`  
**Exists:** True  
**Size:** 8141 bytes  

**Top-level fields:**
  - test
  - true_dist
  - baselines
  - rows
  - elapsed_seconds
  - pool_size
  - Ns
  - fracs
  - seeds

**Missing expected fields:** results, metadata, timestamp

**Metadata gaps (missing in artifact.metadata):** git_hash, git_branch, timestamp, environment

---

## CRITICAL METADATA GAPS (Sprint 2A)

Project 12 must ensure the following for re-validation artifacts:

| Field | Current (P11) | Required (P12) |
|---|---|---|
| git_hash | Missing/Present | ✅ Must capture |
| timestamp | Unclear | ✅ ISO 8601 format |
| environment | Not found | ✅ Python, Torch versions |
| seeds | Found in results | ✅ Explicit array at top level |
| holdout_path | Not in metadata | ✅ Must reference |
| pool_config | Not in metadata | ✅ pool_size + composition |
| baseline_implementations | Not explicit | ✅ Reference commit IDs |
