# ENTRYPOINT_FEASIBILITY_PROJECT_4 — Script Analysis and Reproducibility Strategy

**Purpose:** Analyze Project 4 baseline and intervention scripts to determine reproducibility strategy for Project 12.

**Date:** April 11, 2026, Sprint 4A  
**Status:** Read-only analysis from `project_4/` source code

---

## 1. Baseline Evaluation Scripts Analysis

### 1.1 MLP Baseline Evaluation

**File:** `project_4/baselines/project_4_phase30_mlp_baseline_eval.py`

**Structure Analysis:**
- ✅ Has `main()` function
- ✅ Has `if __name__ == "__main__"` guard
- ❓ Argparse support: NOT FOUND (hardcoded paths)

**Output Location:**
- Hardcoded: `RESULTS_DIR = PROJECT_4_ROOT / "results" / "baseline_runs"`
- Writes: `phase30_mlp_baseline_artifact.json` (hardcoded filename)
- **Issue:** Output path is NOT injectable via command-line arguments

**Input Specification:**
- Checkpoint: Imported via `build_phase30_adapter()` (path unclear, likely hardcoded in adapter)
- Seed handling: `random_digit_batch(num_samples, length, seed)` supports seed parameter
- Batch generation: appears deterministic given seed

**Reproducibility Assessment:**
- **Issue (CRITICAL):** Output directory hardcoded; cannot redirect to `project_12/results/`
- **Recommendation:** **COPY + PATCH strategy**
  - Copy script into `project_12/scripts/baselines/`
  - Patch `RESULTS_DIR` to accept environment variable or inline constant
  - Modify to follow Project 12 manifest structure

---

### 1.2 LSTM Baseline Evaluation

**File:** `project_4/baselines/project_4_phase30_lstm_baseline_eval.py`

**Structure:** Identical to MLP

**Output Location:** Hardcoded to `project_4/results/baseline_runs/`

**Reproducibility Assessment:** Same issue as MLP → **COPY + PATCH**

---

### 1.3 Transformer Baseline Evaluation

**File:** `project_4/baselines/project_4_phase30_transformer_baseline_eval.py`

**Structure:** Identical to MLP/LSTM

**Output Location:** Hardcoded to `project_4/results/baseline_runs/`

**Reproducibility Assessment:** Same issue → **COPY + PATCH**

---

### 1.4 Validation Scripts

**Files:**
- `project_4/baselines/project_4_phase30_mlp_baseline_validate.py`
- `project_4/baselines/project_4_phase30_lstm_baseline_validate.py`
- `project_4/baselines/project_4_phase30_transformer_baseline_validate.py`

**Purpose:** Post-training repeated-run stability checks

**Assessment:** Optional for Sprint 4B (focus on eval first, validation runs second)

---

## 2. Intervention Script Analysis

### 2.1 Adversarial Training

**File:** `project_4/interventions/adversarial_training/project_4_adversarial_training.py`

**Structure Analysis:**
- ✅ Has `main()` function
- ✅ Has `if __name__ == "__main__"` guard
- ❓ Argparse support: NOT FOUND (hardcoded paths)

**Output Location:**
- Hardcoded: `OUTPUT_DIR = PROJECT_4_ROOT / "interventions" / "adversarial_training" / "results"`
- Writes: 
  - `project_4_adversarial_training_artifact.json` (hardcoded)
  - `project_4_adversarial_training_report.md` (hardcoded)
- **Issue:** Output path NOT injectable

**Input Specification:**
- Base model: `"MLP"` (hardcoded in script)
- Seen families: `["alternating_carry", "full_propagation_chain"]` (hardcoded)
- Held-out family: `"block_boundary_stress"` (hardcoded)
- Training config: All parameters hardcoded

**Training Parameters (from artifact inspection):**
- `training_seed`: **MISSING from metadata** (gap flagged)
- `num_training_epochs`: TBD (inspect artifact)
- Learning rate: TBD

**Reproducibility Assessment:**
- **Critical issues:**
  - Output directory hardcoded → cannot write to `project_12/results/`
  - Training seed not recorded → cannot reproduce exactly
- **Recommendation:** **COPY + PATCH + MANIFEST**
  - Copy script into `project_12/scripts/interventions/`
  - Patch output directory
  - Inject seed from manifest
  - Inject training parameters from manifest if needed

---

### 2.2 Intervention Validation

**File:** `project_4/interventions/adversarial_training/project_4_adversarial_training_validate.py`

**Purpose:** Repeated-run stability check on intervention

**Assessment:** Optional for Sprint 4B (secondary to main intervention run)

---

## 3. Reproducibility Strategy Decision Matrix

| Component | Copy + Patch? | Subprocess? | Import + Wrapper? | Notes |
|-----------|---|---|---|---|
| MLP eval | **YES** | Possible | Not recommended | Output dir hardcoded; model import may have path issues |
| LSTM eval | **YES** | Possible | Not recommended | Same as MLP |
| Transformer eval | **YES** | Possible | Not recommended | Same as MLP |
| Adversarial training | **YES** | Possible | Not recommended | Output + seed hardcoded; training params fixed |
| Validation runs | Later | Later | Later | Secondary priority for Sprint 4B |

---

## 4. Recommended Sprint 4B Strategy

### Phase 4B.1: Baseline Re-runs (Subprocess Execution)

**Approach:** Copy each baseline eval script into `project_12/scripts/baselines/` and patch output dir.

**Baseline scripts to include:**
1. `project_12/scripts/baselines/project4_mlp_baseline_repro.py` (copied + patched)
2. `project_12/scripts/baselines/project4_lstm_baseline_repro.py` (copied + patched)
3. `project_12/scripts/baselines/project4_transformer_baseline_repro.py` (copied + patched)

**Execution:**
```bash
python project_12/scripts/baselines/project4_mlp_baseline_repro.py --output_dir project_12/results/repro_p4/baselines
```

**Validation (P4-C02, C03, C05, C06):** Compare per-family accuracies to Project 4 historical values.

---

### Phase 4B.2: Intervention Re-run (Subprocess Execution)

**Approach:** Copy intervention script, patch output dir + seed injection.

**Intervention script:**
1. `project_12/scripts/interventions/project4_adversarial_training_repro.py` (copied + patched)

**Execution:**
```bash
python project_12/scripts/interventions/project4_adversarial_training_repro.py \
  --output_dir project_12/results/repro_p4/intervention \
  --training_seed 42 \
  --num_epochs 50
```

**Validation (P4-C04):** Compare seen-family gain vs. held-out-family gain; confirm narrow transfer pattern.

---

## 5. Checkpoint and Asset Verification

### 5.1 Required Assets (to verify exist)

**Baseline checkpoints:**
- `project_4/checkpoints/phase30_mlp_model.pt`
- `project_4/checkpoints/phase30_lstm_model.pt`
- `project_4/checkpoints/phase30_transformer_model.pt`

**Status:** TBD (inspect in Sprint 4B)

### 5.2 Phase 30 Imports

**Module:** `src/train/phase_30_multidigit_learning.py`

**Classes needed:**
- `MLPSequenceArithmetic`
- `LSTMSequenceArithmetic`
- `TransformerSequenceArithmetic`

**Status:** Assumed available (part of shared codebase)

---

## 6. Manifest Templates (For Sprint 4B Execution)

### 6.1 Baselines Manifest

**File:** `project_12/manifests/p4_baselines_repro.json`

```json
{
  "claim_ids": ["P4-C02", "P4-C03", "P4-C05", "P4-C06"],
  "baselines": {
    "mlp": {
      "script": "project_12/scripts/baselines/project4_mlp_baseline_repro.py",
      "checkpoint": "project_4/checkpoints/phase30_mlp_model.pt",
      "output_dir": "project_12/results/repro_p4/baselines/mlp"
    },
    "lstm": {
      "script": "project_12/scripts/baselines/project4_lstm_baseline_repro.py",
      "checkpoint": "project_4/checkpoints/phase30_lstm_model.pt",
      "output_dir": "project_12/results/repro_p4/baselines/lstm"
    },
    "transformer": {
      "script": "project_12/scripts/baselines/project4_transformer_baseline_repro.py",
      "checkpoint": "project_4/checkpoints/phase30_transformer_model.pt",
      "output_dir": "project_12/results/repro_p4/baselines/transformer"
    }
  },
  "validation": {
    "families": ["alternating_carry", "full_propagation_chain", "block_boundary_stress"],
    "num_test_samples": 1000
  }
}
```

### 6.2 Intervention Manifest

**File:** `project_12/manifests/p4_adversarial_training_repro.json`

```json
{
  "claim_ids": ["P4-C04"],
  "intervention": {
    "name": "adversarial_training",
    "script": "project_12/scripts/interventions/project4_adversarial_training_repro.py",
    "base_checkpoint": "project_4/checkpoints/phase30_mlp_model.pt",
    "training_seed": 42,
    "num_training_epochs": 50,
    "learning_rate": 0.001,
    "batch_size": 32,
    "seen_families": ["alternating_carry", "full_propagation_chain"],
    "heldout_family": "block_boundary_stress",
    "output_dir": "project_12/results/repro_p4/intervention"
  },
  "validation": {
    "compute_transfer_ratio": true
  }
}
```

---

## 7. Known Issues & Mitigations

| Issue | Severity | Mitigation | Sprint |
|-------|----------|-----------|--------|
| Output dirs hardcoded | HIGH | Copy + patch in 4B | 4B.1 |
| Training seed not recorded | HIGH | Extract from artifact or fix in copy | 4B.2 |
| Checkpoint paths unclear | MEDIUM | Verify existence in 4B verification phase | 4B.1 |
| No argparse in scripts | MEDIUM | Acceptable; use manifest-driven execution | 4A-4B |

---

## 8. Readiness Checklist for Sprint 4B

- ✅ All baseline eval scripts identified
- ✅ Intervention script identified
- ✅ Output hardcoding issue documented
- ✅ Strategy (copy + patch) agreed
- ✅ Manifest templates prepared
- ⏳ Checkpoint verification (Sprint 4B)
- ⏳ Actual copying + patching (Sprint 4B)
- ⏳ Execution + validation (Sprint 4B)

---
