# PROJECT 5 INTERIM SYNTHESIS
## Decomposition Robustness Exploration — Current Position

**Date:** April 2026  
**Project:** 5  
**Status:** INTERIM SYNTHESIS ACTIVE

---

## Purpose

This document records the current synthesis point in Project 5.

Project 5 began with a focused question:

> Does decomposition improve structural robustness in neural arithmetic?

The project has now produced a sequence of linked results that are strong enough to justify an interim synthesis before further expansion.

---

## Result 1 — Structural Decomposition Feasibility

The first clean decomposition experiment established that:

- blockwise decomposition is structurally sound
- explicit carry transfer across block boundaries preserves correctness
- carry reset at chunk boundaries causes immediate failure on hard structured families

### Interpretation
This showed that decomposition itself is not the problem.
If carry transfer is correct, decomposition can preserve robustness.

---

## Result 2 — Learned Local Processor Bottleneck

The second result showed that:

- a learned local processor can learn carry perfectly
- but fails substantially on local digit prediction
- and the composed learned system collapses across all tested structural families

### Interpretation
This established that:
- structural feasibility
- and learned feasibility

are different questions.

A decomposition design may be correct in principle while still failing completely when implemented through a weak learned local processor.

---

## Result 3 — Reweighting Does Not Rescue the Bottleneck

The third result tested a focused hypothesis:

- perhaps the failure came from underweighting carry-producing local digit cases

This was tested by reweighting digit-loss on `carry_out = 1` cases.

### Observed outcome
- overall digit accuracy became worse
- carry-conditioned hard cases did not improve meaningfully
- composed system performance remained collapsed

### Interpretation
This strongly suggests that the bottleneck is not well explained by simple class imbalance or straightforward carry-conditioned loss underweighting.

---

## Current Best Interpretation

The most defensible current interpretation is:

> decomposition can be structurally correct, but successful learned decomposition requires a local processor that can reliably separate carry emission from carry-conditioned digit transformation.
>
> The current learned local processor fails at that second requirement, and simple loss reweighting does not fix it.

This is now the strongest Project 5 position.

---

## What Project 5 Has Already Established

Project 5 has already established three important things:

1. **decomposition can work in principle**
2. **the learned bottleneck is local and carry-conditioned**
3. **simple loss reweighting is not enough to solve it**

These are already meaningful research findings.

---

## What Project 5 Has NOT Yet Established

Project 5 has not yet established:

- whether a larger local model would solve the bottleneck
- whether a different local representation would solve it
- whether a more structured interface design would solve it
- whether decomposition can become genuinely learned and robust under a stronger local processor

Those remain open.

---

## Recommended Next Research Branch

The next question should no longer be:
- "does decomposition work in principle?"

That question is answered.

The next question should be:
- "what kind of local learned processor is strong enough to support decomposition?"

This suggests the next branch should test one of:

1. **larger local model capacity**
2. **explicit carry-conditioned representation**
3. **alternative output formulation**
4. **more structured local supervision**

---

## Interim Position

Project 5 is already scientifically productive even before final closure.

It has transformed the original question into a sharper one:

- not whether decomposition is possible,
- but what prevents a learned local model from realizing it.

That is substantial progress.

---
