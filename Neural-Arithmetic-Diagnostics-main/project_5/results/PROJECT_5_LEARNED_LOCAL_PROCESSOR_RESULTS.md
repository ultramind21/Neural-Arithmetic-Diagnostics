# PROJECT 5 LEARNED LOCAL PROCESSOR RESULTS
## First Learned Interface Result

**Date:** April 2026  
**Project:** 5  
**Status:** COMPLETE  
**Verdict:** PASS

---

## Purpose

This document records the first learned-local-processor result in Project 5.

Its role is to answer the next question after the structural-oracle decomposition result:

> Can a learned local processor preserve the structural benefits of decomposition with explicit carry passing?

---

## Background

The previous Project 5 result established that decomposition is structurally sound when carry is handled correctly:

- exact local arithmetic + explicit carry interface
- preserved full correctness on the tested structured families

That result showed that decomposition itself is not the problem.

The next question was whether a learned local processor could support the same decomposition logic.

---

## Core Result

The first learned local processor result showed a sharp split:

- **local carry prediction** was learned easily
- **local digit prediction** was not learned well enough
- the fully composed system failed across all tested families

---

## Local Training Result

### Observed local metrics
- `local_digit_acc = 0.41`
- `local_carry_acc = 1.00`
- `local_exact_acc = 0.41`

### Interpretation
The local processor successfully learned the carry signal, but did not learn the digit output mapping with sufficient reliability.

This means the learned local module is not yet a faithful replacement for the exact local arithmetic oracle.

---

## Composed Blockwise Result

Under blockwise composition with explicit carry passing, the learned local processor produced:

- `alternating_carry = 0.0`
- `full_propagation_chain = 0.0`
- `block_boundary_stress = 0.0`

### Interpretation
The local processor's weaknesses were amplified through composition, resulting in full collapse across the tested structural families.

---

## Main Finding

The main finding of this experiment is:

> Structural decomposition can be sound in principle, yet still fail completely when implemented through a learned local processor that has not learned the local digit mapping well enough.

This is a strong and informative result.

---

## What This Establishes

This experiment establishes the following:

1. **decomposition feasibility and learned feasibility are different questions**
2. **carry-interface learnability alone is not enough**
3. **local digit prediction quality is a critical bottleneck**
4. **compositional collapse can arise even when the structural design is correct**

---

## Why This Result Matters

This result sharpens the Project 5 research question substantially.

Before this experiment, one could reasonably suspect that decomposition failure might come mainly from:
- chunk boundaries
- carry transfer
- or architectural interface problems

After this experiment, a new possibility becomes much more central:

- the decomposition design may be sound,
- but the learned local processor may be too weak to preserve the necessary local arithmetic transformation.

This is a deeper and more precise failure mode.

---

## What This Does NOT Yet Prove

This result does not prove that:

- learned local processors can never work
- decomposition is fundamentally flawed
- better local models or training schemes would not succeed
- the exact optimal local architecture is already known

It is a first learned-interface result, not a closure of Project 5.

---

## Correct Interpretation

The correct interpretation is:

- exact local decomposition works
- learned local decomposition currently fails
- therefore the problem has moved from:
  - "is decomposition structurally valid?"
  to
  - "what kind of local learned processor is strong enough to support decomposition?"

This is the central value of the experiment.

---

## Recommended Next Step

A natural next step is to investigate why local digit prediction remains weak.

Possible follow-up directions include:
- stronger local architectures
- richer local representations
- longer local training
- better local supervision
- explicit interface regularization

---

## Formal Status

**Result:** PASS  
**Type:** First learned local interface result  
**Main message:** structural soundness does not guarantee learned compositional success

---
