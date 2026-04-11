# BASELINE_SPEC_PROJECT_4 — Task, Metrics, and Entrypoint Specification

**Purpose:** Document the official Project 4 task definition, metrics, and baseline configuration extracted from Project 4 source code.

**Date:** April 11, 2026, Sprint 4A  
**Status:** Read-only documentation from `project_4/` (no modifications)

---

## 1. Task Definition

### 1.1 Arithmetic Task
**Source:** `project_4/framework/PROJECT_4_DIAGNOSTIC_FRAMEWORK.md` + `project_4/baselines/project_4_phase30_mlp_baseline_eval.py`

**Core Task:** Single-digit addition with carry propagation.

**Operands:** 
- Two sequences of single digits (0–9 each)
- Length: variable (typically 8–16 positions for evaluation)
- Representation: position-wise (right-to-left convention: position 0 = ones place)

**Output:** 
- Position-wise digit predictions (0–9)
- Carry predictions per position (0 or 1)

**Exact-Match Definition (from Phase 30 alignment principle):**
- All predicted digits must match ground truth (position by position)
- All predicted carries must match ground truth (position by position)
- Both must be correct across the entire sequence

**In-Distribution Domain:**
- Random digit sequences, uniformly sampled from {0–9}
- No structural constraints beyond being independent random trials

---

## 2. Adversarial Pattern Families

**Source:** `project_4/diagnostics/benchmark_adversarial_patterns.py` (official definitions)

### 2.1 Pattern: Alternating Carry
**Definition (from code):**
```
a = [9, 0, 9, 0, 9, 0, ...]  (alternating 9 and 0)
b = [1, 0, 1, 0, 1, 0, ...]  (alternating 1 and 0)
```

**Expected result:**
- Each 9+1 at odd positions produces a carry chain
- Each 0+0 at even positions produces no carry
- Carry logic must alternate correctly

**Intended stress:** Periodic carry structure; tests alternating carry dependencies.

**Status in locked claims:** P4-C05 (universal collapse: all models 0.0)

---

### 2.2 Pattern: Full Propagation Chain
**Definition (from code):**
```
a = [9, 9, 9, 9, ...]  (all 9s)
b = [1, 1, 1, 1, ...]  (all 1s)
```

**Expected result:**
- 9+1 at position 0 produces digit=0 and carry=1
- Carry propagates through all subsequent positions
- Final result has leading 1 and zeros in middle, dependent on length

**Intended stress:** Full carry propagation across entire sequence; tests carry chain handling.

**Status in locked claims:** P4-C05 (universal collapse: all models 0.0)

---

### 2.3 Pattern: Block-Boundary Stress
**Definition (from framework):**
Operand pairs specifically designed to stress carry propagation at block boundaries (e.g., between conceptual 4-digit blocks).

**Example configuration (typical):**
- High-value digits at block boundaries (positions 3, 7, 11, ...)
- Patterns designed to produce carries that cross block edges

**Intended stress:** Boundary-specific carry handling; tests compositional robustness across artificial decomposition boundaries.

**Status in locked claims:** P4-C02 (architecture-dependent split; MLP=1.0, LSTM=0.0, Transformer=1.0)

---

## 3. Evaluation Metrics

**Source:** `project_4/baselines/project_4_phase30_mlp_baseline_eval.py` + `project_4/diagnostics/diagnostic_scorecard.py`

### 3.1 Primary Metric: Exact-Match Accuracy
**Definition:** Proportion of sequences where all digits AND all carries match ground truth.

**Computation:**
```
per_seq_match = (all_digits_correct) AND (all_carries_correct)
exact_match_accuracy = count(per_seq_match) / num_sequences
```

**Range:** [0.0, 1.0]  
**Benchmark:** Human baseline TBD (typically very high for in-distribution)

---

### 3.2 Accuracy Per Adversarial Family

Each family produces a single numeric accuracy value (exact-match across its test set).

**Notation:**
- `accuracy_in_dist`: in-distribution random evaluation
- `accuracy_alternating_carry`: alternating carry family
- `accuracy_full_propagation`: full propagation chain family
- `accuracy_block_boundary`: block-boundary stress family

---

### 3.3 Mean Adversarial Accuracy (Reported in Project 4 Results)

**Source:** `project_4/results/PROJECT_4_RESULTS_SUMMARY.md` (observed values)

**Definition:** Average of all adversarial family accuracies (excluding in-dist).

**Example (Project 4 observed MLP):**
- Alternating carry: 0.0
- Full propagation: 0.0
- Block-boundary: 1.0
- Mean adversarial = (0.0 + 0.0 + 1.0) / 3 = 0.333... ≈ 0.33

**Interpretation:** Summarizes overall robustness to structured adversarial patterns (does NOT replace per-family breakdown).

---

## 4. Baseline Models

**Source:** `project_4/baselines/` (phase30 implementations)

### 4.1 Architecture: MLP
**File:** `project_4/baselines/project_4_phase30_mlp_baseline_eval.py`

**Model class:** MLPSequenceArithmetic (from Phase 30)  
**Architecture:** Feed-forward MLP with hidden layers over flattened digit inputs  
**Checkpoint:** `project_4/checkpoints/phase30_mlp_model.pt`

**Hyperparameters (from Phase 30):**
- Hidden dim: TBD (inspect artifact)
- Num layers: TBD (inspect artifact)
- Activation: ReLU (standard Phase 30)

**Input representation:** Flattened one-hot or embedded digit sequences  
**Output:** Logits over digit classes (0–9) + carry logits (0–1) per position

---

### 4.2 Architecture: LSTM
**File:** `project_4/baselines/project_4_phase30_lstm_baseline_eval.py`

**Model class:** LSTMSequenceArithmetic (from Phase 30)  
**Architecture:** LSTM over digit embeddings; output head for digit + carry  
**Checkpoint:** `project_4/checkpoints/phase30_lstm_model.pt`

**Key parameters:**
- LSTM hidden dim: TBD (inspect artifact)
- Num layers: TBD (inspect artifact)
- Embedding dim: TBD

---

### 4.3 Architecture: Transformer
**File:** `project_4/baselines/project_4_phase30_transformer_baseline_eval.py`

**Model class:** TransformerSequenceArithmetic (from Phase 30)  
**Architecture:** Self-attention Transformer  
**Checkpoint:** `project_4/checkpoints/phase30_transformer_model.pt`

**Key parameters:**
- Hidden dim / d_model: TBD (inspect artifact)
- Num heads: TBD
- Num layers: TBD
- Positional encoding: absolute or relative (TBD)

---

## 5. Stability Protocol

**Source:** `project_4/framework/RESULT_VALIDATION_PROTOCOL.md` + `project_4/validation/validate_run_stability.py`

### 5.1 Definition of STABLE

A baseline is marked **STABLE** if repeated independent runs (same architecture, different random seeds) produce:
- **Consistent accuracy values** (within measurement tolerance)
- **Consistent per-family rankings** (e.g., always lowest on alternating carry)
- **No sign reversals** between runs

**Tolerance:** Typically ≤ 1e-4 relative difference or explicit threshold TBD.

### 5.2 Repeat-Run Configuration

**Number of runs:** TBD (inspect `*_validation_runs.json`)  
**Seeds used:** TBD (inspect artifact metadata)  
**Run independence:** Each run uses fresh random initialization and fresh random batches

### 5.3 Stability Classification Location

**Declared in:** `project_4/results/PROJECT_4_BASELINE_CLASSIFICATION_SUMMARY.md` (column "Status")

**Example (Project 4 reported):**
```
MLP:        STABLE (across all families)
LSTM:       STABLE (across all families)
Transformer: STABLE (across all families)
```

---

## 6. Intervention: Adversarial Training

**Source:** `project_4/interventions/adversarial_training/project_4_adversarial_training.py`

### 6.1 Training Procedure

**Base model:** MLP baseline (Phase 30 checkpoint)

**Adversarial augmentation families (seen during training):**
- Alternating carry
- Full propagation chain

**Training strategy:**
- Mix adversarial examples into training batch
- Standard supervised learning with cross-entropy loss
- Number of epochs: TBD (inspect artifact)
- Learning rate & schedule: TBD (inspect artifact)

### 6.2 Evaluation

**Post-training evaluation on:**
1. In-distribution random (baseline)
2. Alternating carry (seen during training)
3. Full propagation chain (seen during training)
4. Block-boundary stress (**held-out**; not seen during training)

### 6.3 Interpretation (Narrow Transfer Test)

**Narrow transfer (from P4-C04):**
- Improvement on seen families: should be positive
- Improvement on held-out (block-boundary): should be near zero or negative
- Gap: (seen_gain − held_out_gain) ≥ 0.10 (pre-registered threshold)

**Result (Project 4 observed):** Strong gain on seen, failure on held-out (narrow transfer confirmed).

---

## 7. Manifest Integration

### 7.1 For Baseline Re-validation (P4-C02, C03, C05, C06)

**Manifest:** `project_12/manifests/p4_baselines_repro.json`

**Required parameters:**
- `architecture`: "mlp" | "lstm" | "transformer"
- `checkpoint_path`: path to phase30 checkpoint
- `output_dir`: where to write results in `project_12/results/repro_p4/`
- `num_test_seeds`: ≥1 (can be single deterministic run)
- `adversarial_families`: ["alternating_carry", "full_propagation_chain", "block_boundary_stress"]

---

### 7.2 For Intervention Re-validation (P4-C04)

**Manifest:** `project_12/manifests/p4_adversarial_training_repro.json`

**Required parameters:**
- `base_checkpoint`: MLP phase30 checkpoint
- `seen_families`: ["alternating_carry", "full_propagation_chain"]
- `heldout_family`: "block_boundary_stress"
- `output_dir`: where to write results
- `training_seed`: reproducible random seed
- `num_training_epochs`: TBD (from artifact)

---

## 8. Artifact Paths (Project 4 Historical)

### 8.1 Baseline Artifacts (to inspect)
- `project_4/results/baseline_runs/phase30_mlp_baseline_artifact.json`
- `project_4/results/baseline_runs/phase30_lstm_baseline_artifact.json`
- `project_4/results/baseline_runs/phase30_transformer_baseline_artifact.json`

**Contents (expected):**
- Per-family accuracies
- Metrics breakdown
- Checkpoint and seed info
- Git hash / run timestamp

### 8.2 Intervention Artifacts (to inspect)
- `project_4/interventions/adversarial_training/results/project_4_adversarial_training_artifact.json`
- `project_4/interventions/adversarial_training/results/project_4_adversarial_training_validation_runs.json`

---

## 9. Status Summary

| Component | Status | Ready for Sprint 4B? |
|-----------|--------|-----|
| Task definition | ✅ Documented | YES |
| Adversarial families | ✅ Defined in benchmark_adversarial_patterns.py | YES |
| Metrics | ✅ Exact-match (detailed above) | YES |
| Baselines (architectures) | ⏳ Checkpoints TBD (inspect artifacts) | Pending 4A |
| Stability protocol | ✅ Defined | YES |
| Intervention (adv training) | ✅ Defined | YES |

---
