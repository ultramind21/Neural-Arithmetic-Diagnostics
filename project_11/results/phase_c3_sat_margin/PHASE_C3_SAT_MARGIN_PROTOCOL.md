# PHASE C3: SATURATION-AWARE MARGINS PROTOCOL

## Experiment Summary
Test whether Rule V3 with saturation-aware margins (V3.1) recovers performance lost in T4-Large locked test through architectural fix targeting clamp-induced errors.

**Hypothesis**: Expanding decision thresholds when saturation risk ≥ 1 will reduce errors in regions where ground-truth clamping destroys information, improving V3.1 macro-F1 by ≥3% over V3-hard baseline.

**Null Hypothesis**: Margin expansion provides no meaningful gain (Δ macro-F1 < 0.03).

---

## Background & Justification

### From T4-Large Postmortem
- **Finding**: 100% of 80 V3 prediction errors were associated with sat_uni > 0 or sat_fam > 0
- **Root Cause**: Ground-truth labels use clamped mechanics:
  ```
  uni_score = clamp(base + P × sf)
  fam_score = clamp(base + 0.30 × sf + 0.80 × H)
  ```
- **Problem**: When raw score ≥ 1.0, clamp destroys entropy; V3 hard thresholds fail near boundaries

### Why Fixed Margins Fail
- **C1 Result**: V3 macro-F1 drops 13.6% under noise vs NN 9.5%
- **Inference**: Problem not sensitivity to noise but hard thresholds in compressed delta space
- **C2 Result**: MC voting (uncertainty) yields V3-MC ≈ V3-hard (Δ < 0.1%)
- **Inference**: Procedural fixes (voting, smoothing) insufficient; need architectural change

### Why V3.1 Should Work
- **Principle**: Detect saturation-risk hotspots and expand confidence margins locally
- **Minimal Change**: Only modify thresholds; preserve all other V3 logic
- **Justification**: 100% error-saturation correlation suggests sat_risk ≥ 1 is highly predictive

---

## Experimental Design

### Test Population
- **Seed**: 223311 (locked, distinct from T4-Large seed 114211)
- **Size**: N = 800 points
- **Composition**:
  - 400 uniform random in T4 ranges
  - 400 boundary-focused (high V3 boundary score)
  - Ensures good coverage of decision boundary where margins matter

### Ground Truth
System config: 4 families, T4 generation ranges [0.001, 0.020] × [0.260, 0.420]
```python
uni_score = clamp(base_global + P × shared_failure)
fam_score = clamp(base_global + 0.30 × shared_failure + 0.80 × H)
region = classify(fam_wins, uni_wins, gap, near_ties)
```
Saturation risk: count families where raw (pre-clamp) ≥ 1.0

### Predictors (3 models evaluated)

#### V3-hard (Baseline)
```python
gap_est = avg([0.80×H + (0.30-P)×sf for sf in shared_failures])
fam_wins = count(delta > 0.005)
uni_wins = count(delta < -0.005)

if fam_wins ≥ 3 and gap_est > 0.005:
    return "family-aware region"
elif uni_wins ≥ 2 or gap_est < -0.003:
    return "universal region"
else:
    return "transition region"
```

#### V3.1-sat-margin (Proposed)
**Key modification**: Expand thresholds conditional on saturation risk
```python
sat_risk = count(families with raw_uni ≥ 1.0 or raw_fam ≥ 1.0)

if sat_risk ≥ 1:
    # Expanded margins
    return v3_predict(margin=0.0065, gap_fam=0.0065, gap_uni=-0.0045)
else:
    # Normal margins
    return v3_predict(margin=0.005, gap_fam=0.005, gap_uni=-0.003)
```

**Rationale**: 
- 0.005 → 0.0065: +30% margin expansion for wins (δ > 0.005 → δ > 0.0065)
- gap_fam gap_fam -0.003 → -0.0045: 50% wider neutral zone for gap
- Effect: "more conservative (shift toward transition region) near clamp boundaries"

#### NN11 (Baseline)
11×11 grid over T4 ranges, predict via normalized nearest-neighbor:
```
d = sqrt(((H_a - H_b) / H_range)² + ((P_a - P_b) / P_range)²)
predict = label of closest grid point
```

### Evaluation Metrics

#### Primary Metrics
- **Accuracy per predictor**: `(true == pred) / total`
- **Macro-F1 per predictor**: avg F1 over 3 labels (per-label F1 averaged)

#### Subsets (breakdown)
1. **Uniform subset**: uniform-generated points
2. **Boundary subset**: boundary-focused points (should improve under V3.1)
3. **Sat_risk ≥ 1 subset**: points with saturation risk ≥ 1 (V3.1 target)
4. **Sat_risk = 0 subset**: points with no saturation (V3.1 should not harm)

#### Secondary Metrics
- **Saturation-linked errors**: 
  - V3 errors where sat_risk ≥ 1 (should decrease under V3.1)
  - V3.1 errors where sat_risk ≥ 1 (target: fewer than V3)

---

## Success Criteria

### Criterion 1: Macro-F1 Gain
```
Δ_macro_f1 = V3.1_macro_f1 - V3_macro_f1
PASS if Δ_macro_f1 > 0.03 (3% absolute improvement)
```

### Criterion 2: Saturation-Error Reduction
```
V3.1_sat_linked_errors < V3_sat_linked_errors
AND
V3.1_sat_linked_errors_rate < 50% of V3 rate
```

### Overall Verdict
- **PASS** (both criteria met): V3.1 is effective saturation-aware fix, viable for adoption
- **FAIL** (either criterion unmet): Saturation margins insufficient; pivot to alternative architectures (e.g., soft margins, retrained NN)

---

## Data Integrity & Immutability

1. **Locked Holdout**:
   - Generated once by `phase_c3_generate_holdout.py` (seed 223311)
   - SHA256 hash printed; holdout_points.json not modified thereafter
   - Prevents data leakage to evaluation

2. **Prior Phases Immutable**:
   - T4-Large (500 pts), C1 (5 noise levels × 20 reps), C2 (100 configs all locked)
   - C3 runs independently on fresh holdout → no overfitting to prior phases

3. **Artifacts Non-destructive**:
   - `artifact.json`: raw metrics (immutable after generation)
   - `report.md`: human-readable summary (can be re-rendered from artifact without rerun)

---

## Timeline & Resource Estimate

| Phase | Task | Est. Time | Notes |
|-------|------|-----------|-------|
| Prep | Syntax check (2 scripts) | 30 sec | py_compile |
| Gen | Holdout generation (800 pts, seed 223311) | 2 min | Boundary score computation |
| Eval | Evaluate on holdout (3 predictors × 800 pts) | 1 min | ~20K predictions |
| Report | Artifact + markdown summary | 10 sec | Auto-generated |
| **Total** | | ~4 min | Pure Python, no deps |

---

## References & Cross-Links

- **T4-Large (Locked)**: macro-F1 V3=0.8575, NN=0.9050
  - Postmortem: 80/80 errors have sat_risk > 0
  - Boundary subset: V3=74.8%, NN=93.2%

- **Phase C1 (Noise)**: V3 robust hypothesis DISPROVEN
  - V3 macro-F1 drop: 13.6% | NN drop: 9.5%
  - Conclusion: not noise sensitivity (procedural) but threshold architecture (structural)

- **Phase C2 (MC Voting)**: Uncertainty mitigation INEFFECTIVE
  - V3-MC ≈ V3-hard (Δ < 0.1%)
  - Conclusion: procedural fixes insufficient

---

## Potential Outcomes

| Outcome | Implication | Next Phase |
|---------|-------------|-----------|
| **PASS** (Δ > 0.03 + sat reduction) | Saturation margins effective | Optional C4 (interpolated grid) or adopt V3.1 |
| **Marginal** (Δ ≈ 0.01-0.03) | Partial benefit | Consider soft margins or retrain baseline |
| **FAIL** (Δ < 0 or sat errors increase) | Architecture fundamentally limited | Accept NN11 or explore alternative models |

---

## Code Artifacts

**Generator** (`phase_c3_generate_holdout.py`):
- Sample 400 uniform (H, P) from T4 ranges
- Compute V3 boundary score (min distance to thresholds) for all candidates
- Sample 400 from boundary pool (sorted by score, highest first)
- Output: holdout_points.json with SHA256 locked

**Evaluator** (`phase_c3_evaluate.py`):
- Load system config (4 families, shared_success values)
- Load holdout (800 points, seed 223311)
- For each point: compute ground_truth, v3_predict, v3_1_sat_margin, nn_label
- Aggregate: overall metrics, subset metrics, saturation-linked error counts
- Output: artifact.json (metrics) and report.md (summary)

---

## Notes for Analyst/Reviewer

1. **V3.1 is minimal**: Only 3 threshold parameters changed (margin, gap_fam, gap_uni) based on sat_risk ≥ 1
2. **No ground-truth modification**: V3.1 predicts using same gaps/deltas; only decision boundaries adjusted
3. **Seed locked**: Holdout irreproducible after hashing; prevents post-hoc data manipulation
4. **Subset analysis critical**: Boundary subset performance is key indicator of fix effectiveness
5. **Saturation-error correlation**: If V3.1 reduces sat-linked errors significantly, hypothesis validated

