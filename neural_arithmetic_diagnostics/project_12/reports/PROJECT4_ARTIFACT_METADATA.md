# PROJECT4_ARTIFACT_METADATA — Inspection Report

**Generated:** 2026-04-11T06:48:56.668635
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

## Metadata Gaps Analysis

- Intervention: missing 'base_checkpoint'
- Intervention: missing 'training_seed'

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
