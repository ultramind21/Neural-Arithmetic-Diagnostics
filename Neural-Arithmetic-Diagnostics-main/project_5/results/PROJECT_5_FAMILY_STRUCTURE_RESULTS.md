# PROJECT 5 FAMILY STRUCTURE RESULTS
## Structural Comparison Across Core Families

**Date:** April 2026  
**Project:** 5  
**Status:** COMPLETE  
**Verdict:** PASS

---

## Purpose

This document records the first structural comparison of the core Project 5 families after the explicit carry-conditioned representation result.

Its purpose is to answer a sharper question:

> If chunk size does not explain the residual family split, what structural property does?

---

## Main Structural Finding

The strongest result of this analysis is that the rescued family,
`full_propagation_chain`, is structurally much simpler than the two unrecovered families.

### Rescued family: `full_propagation_chain`
This family is characterized by:
- zero transitions in `a`
- zero transitions in `b`
- zero transitions in carry sequence
- only one local pair type
- only one local `(a, b, carry)` triple type
- effectively uniform structure across the sequence

### Unrecovered families
The two unrecovered families are more structurally demanding:

#### `alternating_carry`
- high transition count
- periodic alternation
- multiple local pair/triple types

#### `block_boundary_stress`
- mixed block structure
- multiple local pair/triple types
- sharper structural heterogeneity across regions

---

## What This Establishes

This analysis establishes the following:

1. the rescued family is not just another carry-heavy case
2. it is also the structurally simplest family in the Project 5 core set
3. the unrecovered families involve substantially more local variation
4. the remaining failure pattern is therefore strongly consistent with structural complexity, not just carry existence alone

---

## Why This Result Matters

This result significantly sharpens Project 5.

Earlier, the project established that:
- decomposition can work structurally
- a learned local processor fails
- simple reweighting does not fix the failure
- explicit carry-conditioned representation helps substantially but only partially

The family-structure result now adds:

> the partial rescue appears to occur specifically on the family with the lowest transition burden and the lowest local-state diversity.

This is a major explanatory refinement.

---

## Correct Interpretation

The most defensible interpretation is:

> the current explicit carry-conditioned local representation is sufficient for a structurally uniform family, but not yet sufficient for families with higher transition density or more diverse local state combinations.

This does not prove a final mechanism, but it is a strong and informative structural account of the current family split.

---

## What This Does NOT Yet Prove

This result does not prove:

- that transition count alone is the unique causal variable
- that local diversity alone fully explains the failures
- that no alternative representation could overcome these families
- that Project 5 is complete

However, it does rule out simpler explanations such as:
- chunk size alone
- or carry existence alone

---

## New Strong Project 5 Position

After this result, the strongest current Project 5 position is:

1. decomposition can work in principle
2. learned local decomposition fails in a structured way
3. explicit carry-conditioned representation improves local learning substantially
4. the rescue currently appears limited to the structurally simplest family
5. the remaining failures are associated with higher structural variation

This is now the best-supported internal logic of the project.

---

## Recommended Next Step

The next step should now focus on:

> whether a stronger local representation can handle families with higher transition density and local-state diversity

This can be explored through:
- larger local capacity
- richer local state representation
- alternative local target formulation
- or explicit transition-aware structure

---

## Formal Status

**Result:** PASS  
**Type:** family structure analysis  
**Main message:** the current rescue is associated with the structurally simplest family, while higher-variation families remain unsolved

---
