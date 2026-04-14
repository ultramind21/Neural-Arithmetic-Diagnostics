# PROJECT 10 REGIME C SPECIFICATION V1
**Name**: Overpowered Universal Rescue  
**Date**: April 8, 2026  
**Purpose**: Determine if mechanism power can substitute for family-specificity

---

## Strategic Context

### Why Regime C Now?
**Regime B Result**: Falsified the claim that "rescue requires family-aligned mechanisms"
- When families became deeply homogeneous (±0.003), universal became nearly equivalent to family-aware
- This raised a critical question: Is family-alignment **structurally necessary** or just **competitively advantageous**?

**Regime C Tests**: Can universal rescue overcome its structural disadvantage through **pure mechanism power**?

### Modified Hypothesis
**If universal can win decisively with 40% power boost**: 
- Family-alignment is not necessary, just happens to be competitive
- Higher-order candidate needs major revision (mechanism power >> family specificity)

**If family-aware still dominates despite power boost**:
- Family-alignment provides structural advantage beyond simple power scaling
- Higher-order candidate survives with family-heterogeneity restriction

---

## Experimental Design

### Structure (Replicates Regime A V2)
- 4 families with residual_family_factor ≈ ±0.015
- base_global_score ≈ 0.465–0.480
- shared_failure_factor ≈ 0.40–0.41

**Rationale**: Keep family heterogeneity constant (high), change only mechanism power

### Rescue Mechanism Specification

#### Universal Rescue (AMPLIFIED)
```
base_gain = 0.42 * shared_failure_factor  ← Increased from 0.30 (+40%)
final_score = avg_base_global_score + base_gain
            = 0.465 + base_gain
```

**Justification for 40% boost**:
- In Regime A V2, gap was 0.0118 with universal at 0.30× factor
- 40% boost could shift competitive balance (~0.35–0.45 range)
- Intermediate enough to be realistic, strong enough to challenge family-aware

#### Family-Aware Rescue (UNCHANGED)
```
base_gain = 0.30 * (avg_base_global_score - family_base_global_score)
family_adjustment = 0.80 * abs(residual_family_factor)
final_score = base_gain + family_adjustment
```

**Rationale**: Controls for mechanism comparison
- If universal (amplified) still loses → family structure matters
- If universal (amplified) wins → mechanism power, not structure, is decisive

---

## Verdict Logic

### Success Threshold (Same as Regime A V2)
- **WEAKENS**: universal_wins ≥ 2 OR avg_universal ≥ avg_family_aware - 0.005
- **SUPPORTS**: family_aware_wins ≥ 3 AND gap > 0.008
- **BOUNDARY**: All other outcomes

### Expected Outcomes & Interpretations

| Outcome | Meaning | Next Step |
|---------|---------|-----------|
| universal_wins ≥ 2 | Power overcomes family-specificity | Candidate narrowed drastically |
| universal_wins = 1 | Competitive but family-aware still ahead | Candidate survives with restriction |
| universal_wins = 0, near_ties ≥ 2 | Family-aware advantage shrinks but persists | Candidate holds, considers Regime D |
| family_aware_wins ≥ 3 | Family structure proves fundamental | Candidate survives strongest test |

---

## Specific Test Case Predictions (Based on Regime A V2)

**Regime A V2 Baseline (0.30× factor)**:
| Family | Universal | Family-Aware | Winner |
|--------|-----------|--------------|--------|
| A | 0.5865 | 0.5983 | family-aware |
| B | 0.5865 | 0.5983 | family-aware |
| C | 0.5865 | 0.5983 | family-aware |
| D | 0.5865 | 0.5983 | near-tie |

**Regime C V1 Prediction (0.42× factor, +40% boost)**:
With 40% boost, universal scores increase by ~0.036 per case:
| Family | Universal (predicted) | Family-Aware | Winner (predicted) |
|--------|----------------------|--------------|-------------------|
| A | 0.622 | 0.598 | universal |
| B | 0.622 | 0.598 | universal |
| C | 0.622 | 0.598 | universal |
| D | 0.622 | 0.592 | universal |

**Prediction**: universal_wins = 4 or 3, WEAKENS candidate (mechanism power > family specificity)

---

## Key Variables Under Control

| Variable | Regime A V2 | Regime C V1 | Purpose |
|----------|------------|-----------|---------|
| Family heterogeneity | HIGH (±0.015) | HIGH (±0.015) | Constant |
| Shared failure factor | 0.40–0.41 | 0.40–0.41 | Constant |
| Base global scores | 0.46–0.48 | 0.46–0.48 | Constant |
| Universal base_gain factor | **0.30** | **0.42** | VARIABLE |
| Family-aware mechanism | Symmetric | Symmetric | Constant |

---

## Outputs & Artifact Locations

### Primary Outputs:
```
project_10/results/project_10_regime_c_overpowered_universal_rescue_v1_artifact.json
project_10/results/project_10_regime_c_overpowered_universal_rescue_v1_report.md
```

### JSON Artifact Structure:
- `timestamp_utc`: Execution time
- `experiment`: "project_10_regime_c_overpowered_universal_rescue_v1"
- `cases[]`: Per-family data (local_competence, base_global, shared_failure, residual_family)
- `rows[]`: Per-family results (universal_score, family_aware_score, winner)
- `summary`: Aggregated metrics (universal_wins, family_aware_wins, near_ties, verdict)
- `notes`: Context and interpretation

### Markdown Report:
- Purpose & strategy
- Per-family results table
- Comparison to Regime A V2 baseline
- Verdict and interpretation
- Next steps

---

## Interpretation Framework

### If WEAKENS (universal dominates):
```
Interpretation: Family-alignment is not structurally necessary
Implication: The higher-order candidate is based on a false premise
             (it's mechanism power, not family-specificity, that matters)
Revision: Candidate must be reformulated as mechanism-strength law, not family-alignment law
Next: Regime D to find exact power threshold or abandon family-alignment focus
```

### If SUPPORTS (family-aware still dominates):
```
Interpretation: Family-specificity provides advantage beyond power scaling
Implication: The higher-order candidate is on the right track (family matters fundamentally)
Revision: Candidate remains valid with family-heterogeneity restriction
Next: Regime D to refine boundary (how much heterogeneity is "enough"?)
```

### If BOUNDARY (mixed results):
```
Interpretation: Power and family-specificity are competitive factors
Implication: The advantage is fragile, depends on their interaction
Revision: Candidate survives but becomes more conditional
Next: Regime D with intermediate power levels or stay current
```

---

## Methodological Notes

### Design Integrity:
- ✅ Maintains symmetric rescue definitions (same as A V2)
- ✅ Isolates only one variable (universal base_gain factor)
- ✅ Uses same family structure as A V2 (direct comparison possible)
- ✅ Predicts outcome before execution (falsification discipline)

### Falsification Discipline:
- If prediction proves wrong, accept the result gracefully
- Do not rationalize away findings that contradict the candidate
- Use all verdicts (WEAKENS, BOUNDARY, SUPPORTS) legitimately

### Boundary Importance:
This test is crucial because it asks: "Is family-alignment a **necessary structural principle** (what we thought Law 3 claimed) or just a **happy coincidence** of the scale at which we've tested?"

If mechanism power can overcome family-specificity → Law 3 needs revision (it's about power, not family)  
If family-specificity persists despite power → Law 3 is on the right track (but scoped by heterogeneity)

---

## Regime C in the Falsification Sequence

```
Regime A V1 (aligned + asymmetry)
    ↓ REJECTED due to design asymmetry
Regime A V2 (aligned + symmetric)
    ↓ RESULT: SUPPORTS WITH BOUNDARY PRESSURE
Regime B V1 (homogeneous structure)
    ↓ RESULT: WEAKENS (family-awareness not necessary)
Regime C V1 (overpowered universal) ← WE ARE HERE
    ↓ Will determine: Is family-alignment fundamentally necessary or just comparatively advantageous?
Regime D (TBD based on C results)
    ↓ Will refine: Exact boundary conditions
Final consolidation → Revised candidate with scope conditions
```

---

## Confidence & Contingency

### Prediction Confidence: MEDIUM-HIGH
- Based on clear mechanism scaling (40% boost should shift balance)
- But family-specificity might provide non-linear advantages
- Prepared for surprise results (e.g., family-aware still wins despite power boost)

### Contingency Plans:
- If C V1 shows mixed results: Implement C V2 with alternative power boost levels (30% or 50%)
- If results are unclear: Commission additional analysis of power vs. specificity trade-off
- If family-aware persists: Proceed directly to Regime D

---

## Timeline & Integration

**Execution**: Immediate (next available session)  
**Expected Duration**: <5 minutes (execution) + analysis time  
**Integration**: Results feed into final adversarial summary and candidate revision  
**Publication**: Include in Project 10 final theory consolidation

---

**Prepared by**: Project 10 Adversarial Falsification Phase  
**Status**: Specification complete, ready for implementation  
**Next**: Create `project_10_regime_c_overpowered_universal_rescue_v1.py` and execute
