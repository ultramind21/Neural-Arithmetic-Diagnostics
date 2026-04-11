# PROJECT4_ARTIFACT_METADATA — Inspection Report

**Generated:** 2026-04-11T06:56:49.093456
**Status:** Sprint 4A read-only inspection

---

## Baseline Artifacts Summary

### MLP Baseline
**Status:** present
**Top-level keys (8):**
```
adapter_metadata, config, model_name, qualification_notes, raw_metrics, regime_guidance, scorecard, timestamp_utc
```

### LSTM Baseline
**Status:** present
**Top-level keys (8):**
```
adapter_metadata, config, model_name, qualification_notes, raw_metrics, regime_guidance, scorecard, timestamp_utc
```

### Transformer Baseline
**Status:** present
**Top-level keys (8):**
```
adapter_metadata, config, model_name, qualification_notes, raw_metrics, regime_guidance, scorecard, timestamp_utc
```

## Validation Runs Summary

### MLP Validation Runs
**Status:** present
**Structure:** 8 top-level keys

### LSTM Validation Runs
**Status:** present
**Structure:** 8 top-level keys

### Transformer Validation Runs
**Status:** present
**Structure:** 8 top-level keys

## Intervention Artifacts Summary

### Adversarial Training Main Artifact
**Status:** present
**Top-level keys (11):**
```
base_model_family, baseline_reference, framework_version, heldout_family, heldout_results, in_distribution, intervention_type, notes, seen_families, seen_results, timestamp_utc
```

### Intervention Validation Runs
**Status:** present

---

## Metadata Gaps Analysis (P12 Standard Fields)

### Baseline Artifacts

  - `seeds`: Validation seed list
  - `checkpoint_path`: Model checkpoint location
  - `git_hash`: Git commit identifier
  - `timestamp`: Execution timestamp
  - `env`: Environment metadata (Python version, library versions)
  - `task_spec`: Task definition (hyperparameters, ranges)
  - `family_breakdown`: Per-family accuracy breakdown

### Intervention Artifact

  - `base_checkpoint`: Name/ID of baseline model used
  - `training_seed`: Seed used for adversarial training
  - `checkpoint_path`: Path to trained intervention model
  - `git_hash`: Git commit identifier
  - `timestamp`: Training execution timestamp
  - `env`: Environment metadata during training
  - `task_spec`: Task parameters for intervention training
  - `family_breakdown`: Per-family accuracy breakdown (training + validation)

---

## Why P12 Standard Metadata Fields Matter

When reproducing Project 4 baselines & interventions in Project 12, we need:

1. **seeds / validation_runs:** Verify reproducibility across multiple random seeds
2. **checkpoint_path:** Locate the exact model weights to load (hardcoded paths in Project 4)
3. **git_hash:** Track which code version was used (ensures procedure-preserving validation)
4. **timestamp:** Correlate artifacts to Project 4 training logs
5. **env:** Verify library versions match (PyTorch, NumPy, etc.)
6. **task_spec:** Confirm hyperparameters (digit length, batch size, etc.) match pre-registration
7. **family_breakdown:** Check per-family accuracy differences for C02, C03, C05

---

## Artifact Path Verification

| Artifact | Path | Exists |
|----------|------|--------|
| MLP Baseline | `project_4\results\baseline_runs\phase30_mlp_baseline_artifact.json` | ✅ |
| LSTM Baseline | `project_4\results\baseline_runs\phase30_lstm_baseline_artifact.json` | ✅ |
| Transformer Baseline | `project_4\results\baseline_runs\phase30_transformer_baseline_artifact.json` | ✅ |
| Intervention | `project_4\interventions\adversarial_training\results\project_4_adversarial_training_artifact.json` | ✅ |

---

## Readiness for Sprint 4B

**Overall:** All critical paths confirmed (no missing TBD baseline/intervention artifacts).
