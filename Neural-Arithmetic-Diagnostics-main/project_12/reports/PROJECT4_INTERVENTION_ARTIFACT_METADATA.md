# PROJECT4_INTERVENTION_ARTIFACT_METADATA — Raw Field Inspection

**Purpose:** Verbatim inspection of Project 4 historical intervention artifact.

**Files Inspected:**
- `project_4/interventions/adversarial_training/results/project_4_adversarial_training_artifact.json`
- `project_4/interventions/adversarial_training/results/project_4_adversarial_training_validation_runs.json`

---

## Artifact Structure

**Total top-level keys:** 11

**Keys present:**
- `base_model_family` (str)
- `baseline_reference` (dict, 2 keys)
- `framework_version` (str)
- `heldout_family` (list, 1 items)
- `heldout_results` (dict, 1 keys)
- `in_distribution` (dict, 4 keys)
- `intervention_type` (str)
- `notes` (list, 3 items)
- `seen_families` (list, 2 items)
- `seen_results` (dict, 2 keys)
- `timestamp_utc` (str)

---

## Raw Field Dumps (Verbatim from Artifact)

### 0a) base_model_family

```json
"phase30_mlp"
```

### 0b) framework_version

```json
"1.0"
```

### 0c) timestamp_utc

```json
"2026-03-31T19:37:50.224796Z"
```

### 1) intervention_type

```json
"adversarial_training"
```

### 2) seen_families

```json
[
  "alternating_carry",
  "full_propagation_chain"
]
```

### 3) heldout_family

```json
[
  "block_boundary_stress"
]
```

### 4) baseline_reference

```json
{
  "in_distribution": "compare against PROJECT_4_BASELINE_CLASSIFICATION_SUMMARY.md",
  "block_boundary_stress": "compare against stable baseline matrix"
}
```

### 5) seen_results

```json
{
  "alternating_carry": {
    "digit_acc": 1.0,
    "carry_acc": 1.0,
    "combined_acc": 1.0,
    "exact_match": 1.0
  },
  "full_propagation_chain": {
    "digit_acc": 0.6000000238418579,
    "carry_acc": 1.0,
    "combined_acc": 0.6000000238418579,
    "exact_match": 0.0
  }
}
```

### 6) heldout_results

```json
{
  "block_boundary_stress": {
    "digit_acc": 0.6000000238418579,
    "carry_acc": 1.0,
    "combined_acc": 0.6000000238418579,
    "exact_match": 0.0
  }
}
```

### 7) in_distribution

```json
{
  "digit_acc": 0.5875000135274604,
  "carry_acc": 0.9515625026542693,
  "combined_acc": 0.5875000135274604,
  "exact_match": 0.046875
}
```

---

## Metadata Gaps (P12 Standard)

**Identified 4 gap(s):**

1. `p12_metadata (git_hash, timestamp_utc, env, manifest_path, entrypoint)`
2. `config.seed (for reproducibility tracking)`
3. `config.base_checkpoint (path tracking)`
4. `config.training_steps or config.epochs (missing training duration)`

---

## Validation Runs Structure

**Total runs:** 4

**Sample run key:** `status`
  - Type: str

---

**Report Generated:** `project_12/scripts/inspect_project4_intervention_artifacts.py` (revised)
