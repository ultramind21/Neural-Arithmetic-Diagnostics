# PROJECT 5 LOCAL EXPLICIT CARRY RESULTS
## Carry-Conditioned Representation Intervention

**Date:** April 2026  
**Project:** 5  
**Status:** COMPLETE  
**Verdict:** PASS

---

## Purpose

This document records the first successful representation-level intervention in Project 5.

Its purpose was to test whether the local decomposition bottleneck could be reduced by making carry representation more explicit inside the local processor.

---

## Background

Earlier Project 5 results established three things:

1. decomposition is structurally sound when exact local arithmetic is used
2. the first learned local processor fails mainly on digit prediction, not carry prediction
3. simple loss reweighting does not rescue the bottleneck

These results suggested that the problem may lie not in carry existence itself, but in how carry is represented and integrated into local digit transformation.

---

## Intervention

The intervention introduced a more explicit carry-conditioned local representation.

Instead of treating the local input only as a flat undifferentiated mapping, the model separated:
- a digit-pair pathway
- a carry pathway
- and then recombined them before digit/carry prediction

This was intended to test whether the local bottleneck reflected representation failure rather than merely optimization weakness.

---

## Main Result

The intervention produced a major improvement in local learnability.

### Local performance shift
- `digit_acc`: approximately **0.41 → 0.95**
- `carry-conditioned gap`: sharply reduced
- `carry_out = 1` digit behavior improved dramatically

### Composed structural effect
- `full_propagation_chain`: **rescued to 1.0**
- `alternating_carry`: remained **0.0**
- `block_boundary_stress`: remained **0.0**

---

## What This Establishes

This result establishes several important points:

### 1. Representation matters directly
The decomposition bottleneck was not just a generic local-capacity failure.
A change in carry-conditioned representation dramatically improved local digit learning.

### 2. Carry-conditioned local difficulty is not fixed
The earlier local bottleneck was not inevitable. It could be reduced substantially by changing representational structure.

### 3. Structural gain can be family-specific
Even after major local improvement, not all structured families were recovered.
This means improved local decomposition does not automatically imply broad structural robustness.

### 4. Full propagation can be rescued without full general rescue
The fact that `full_propagation_chain` was restored while `alternating_carry` and `block_boundary_stress` remained at zero is highly informative.
It shows that decomposition-sensitive success can emerge selectively.

---

## Why This Result Is Important

This is the strongest Project 5 result so far because it changes the status of the decomposition question.

Earlier results showed:
- decomposition works in principle
- but learned local decomposition fails

This result sharpens the conclusion:

> learned local decomposition can improve dramatically when carry representation is made explicit, but the resulting robustness remains selective rather than broad.

That is a major refinement of the project's central hypothesis.

---

## Correct Interpretation

The most defensible interpretation is:

> explicit carry-conditioned representation is a meaningful intervention on the learned local bottleneck, and it can substantially improve both local digit learning and at least one major structured family. However, this does not yet produce broad decomposition robustness across all tested families.

This is a strong positive result, but not a full closure claim.

---

## What This Does NOT Yet Prove

This result does not prove:

- that explicit carry-conditioned representation is sufficient in general
- that decomposition is now solved
- that alternating and block-boundary failures are secondary or irrelevant
- that the optimal local architecture has already been found
- that Project 5 has reached final closure

---

## New Project 5 Position After This Result

Project 5 now has a much sharper structure:

1. decomposition is structurally possible
2. naive learned local processing fails
3. simple loss reweighting does not solve the failure
4. explicit carry-conditioned representation substantially improves the situation
5. but broad structural robustness remains incomplete

This is now the strongest current internal logic of the project.

---

## Recommended Next Step

The natural next step is now narrower and more informative than before:

> Why do `alternating_carry` and `block_boundary_stress` remain unsolved even after explicit carry-conditioned representation succeeds on `full_propagation_chain`?

This is now the most important follow-up question.

---

## Formal Status

**Result:** PASS  
**Type:** representation-level intervention result  
**Main message:** explicit carry-conditioned representation materially improves learned local decomposition, but robustness remains selectively incomplete

---
