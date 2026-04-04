# PROJECT 5 SYNTHESIS V2
## Decomposition Robustness Exploration — Refined Scientific Position

**Date:** April 2026  
**Project:** 5  
**Status:** ACTIVE SYNTHESIS  
**Scope:** refined interim synthesis, not final closure

---

## 1. Purpose

This document records the refined synthesis point of Project 5 after the latest intervention and exclusion results.

Project 5 began from a focused question:

> Does decomposition improve structural robustness in neural arithmetic?

The project has now moved beyond that initial form.
It no longer asks only whether decomposition can work. It now asks a more precise question:

> Under what representational and structural conditions can decomposition be learned robustly?

---

## 2. Current Accepted Result Chain

### Result 1
**Structural decomposition with exact local oracle works perfectly.**

This established that decomposition is structurally feasible if carry is transferred correctly across chunk boundaries.

### Result 2
**A learned local processor fails, and the bottleneck is not uniform.**

The first learned local processor showed that carry prediction can be easy while digit prediction remains weak enough to collapse the composed system.

### Result 3
**The learned local bottleneck is strongly carry-conditioned.**

The local digit failure is concentrated especially in carry-producing cases.

### Result 4
**Simple loss reweighting does not rescue the bottleneck.**

This ruled out a simple class-imbalance explanation.

### Result 5
**Explicit carry-conditioned representation substantially improves local learnability and rescues one family.**

This was the first major positive result.
It showed that representational design matters strongly.

### Result 6
**Chunk size does not explain the residual family split.**

The remaining split persists across chunk-size variation.

### Result 7
**The rescued family is structurally the simplest family.**

The rescued family has:
- minimal local diversity
- zero transition burden
- effectively uniform local structure

### Result 8
**Simple local context expansion does not rescue the remaining failures.**

Adding a local neighborhood window does not solve the remaining difficult families and can even destroy earlier partial success.

### Result 9
**Explicit transition-aware local architecture achieves 92% local accuracy but still produces 0.0 composed accuracy.**

This is the most critical negative result yet.
Despite achieving:
- 92% local digit accuracy
- 99.99% carry accuracy
- near-zero carry-conditioned gap (0.035)
- explicit local transition structure representation

The composed system produces 0.0 exact-match on all three families, including full_propagation_chain which was previously rescued to 1.0.

---

## 3. What Project 5 Has Now Clearly Established

Project 5 now supports several strong statements.

### A. Decomposition can work in principle
This is no longer speculative.
The oracle-based result established structural feasibility cleanly.

### B. Learned decomposition failure is real and structured
The failure is not random and not uniform.
It is tied to identifiable arithmetic and family-level conditions.

### C. Representation matters more than naive weighting
The explicit carry-conditioned intervention produced a major gain where simple reweighting failed.

### D. The remaining failure is not explained by several simple alternatives
Project 5 has now ruled out or strongly weakened multiple simple accounts:
- decomposition itself is not the problem
- class imbalance alone is not the problem
- chunk size alone is not the problem
- simple local context shortage is not the problem
- insufficient local representation is not the problem
- missing transition structure awareness is not the problem

This is a very important point.
Project 5 is no longer just gathering results.
It is building an exclusion map.

---

## 4. The Current Best Explanation (Revised)

The strongest current scientific position has shifted:

Previous position: decomposition robustness depends on reliable carry-conditioned digit transformation.

**New position:** the bottleneck is not local representation quality but **composition error dynamics**.

Result 9 proved this.
At 92% local accuracy, the composed system still fails completely.
This means even given excellent local performance, error amplification through the feedback loop (previous step output → next step input) is catastrophic.

The issue is not:
- insufficient local representation
- carry-conditioned bottleneck alone
- or transition awareness

The issue is:
- **cumulative error feedback** during blockwise composition
- small local errors (8%) amplify into total failure over length-6 sequences
- the error propagation dynamics are fundamentally misaligned with sequential decomposition

---

## 5. What Has Been Ruled Out (Extended)

Project 5 has already ruled out five important simplified explanations:

### 1. "Decomposition itself is flawed"
Not supported.
Decomposition works perfectly under the exact local oracle.

### 2. "The failure is mostly a class-imbalance issue"
Not supported.
Simple loss reweighting does not solve the bottleneck and can worsen performance.

### 3. "The failure is mainly a chunk-size artifact"
Not supported.
The family split is stable across the tested chunk sizes.

### 4. "The local model just needs a bit more neighboring context"
Not supported in the simple tested form.
A wider local context window does not rescue the failing families and may erase previous gains.

### 5. "The local model just needs better representation"
Most critical. Not supported.
Even at 92% local accuracy with transition-aware structure, the composed system produces 0.0 accuracy.

This proves the problem is **not insufficient local representation** but **error accumulation dynamics**.

This is now one of the strongest outputs of Project 5:
a structured elimination of weak explanations, converging toward the real frontier.

---

## 6. What the Positive Result Actually Means

The explicit carry-conditioned intervention is important because it showed that:
- local learnability can improve dramatically
- carry-conditioned digit bottlenecks can be reduced
- and one full family can be rescued completely

But the significance of that result must be read carefully.

It does not mean:
- decomposition is solved
- or that representation alone is sufficient in the current form

What it means is:

> representational intervention can unlock real progress, but that progress remains selectively bounded by family structure.

This is a stronger and more realistic conclusion than either:
- "nothing works"
or
- "we found the answer"

---

## 7. The New Project 5 Question (Refined)

The project has now advanced to a sharper question:

> How can learned decomposition overcome error accumulation in the feedback loop, where previous position errors become input noise for future positions?

This is now the real frontier.

Not:
- whether decomposition is possible
- whether the local model can learn
- or whether we can improve local accuracy

But:
- **how to structure composition so that error feedback does not amplify catastrophically**
- what changes to loss, architecture, or target formulation could stabilize the sequential error dynamics
- whether decomposition as currently formulated can handle the error feedback problem at all

---

## 8. Why This Is Already Valuable

Even without final closure, Project 5 is already scientifically valuable because it has converted a broad architectural intuition into a structured empirical map.

It has identified:
- one clean positive feasibility result
- one major representational improvement result
- several ruled-out simple explanations
- and one refined frontier question

That is substantial progress.

---

## 9. What Project 5 Does NOT Yet Establish

Project 5 still does not establish:

- a final successful learned decomposition method
- a definitive local architecture
- a complete mechanistic account of the remaining failures
- a final project closure verdict
- a proof that explicit carry-conditioned representation is the last major ingredient

Those remain open.

---

## 10. Current Best Interim Position

The most defensible current interim position is:

> Project 5 has shown that decomposition is structurally feasible, that learned local decomposition fails in a strongly structured way, that explicit carry-conditioned representation can materially improve the situation, and that several simpler explanations for the remaining failure can already be ruled out.

This is now the strongest Project 5 statement.

---

## 11. Recommended Next Step

The next meaningful step should now target error accumulation and error feedback dynamics, not local representation.

Examples include:
- **error feedback stabilization** through auxiliary losses
- **intermediate supervision** on intermediate carry predictions
- **different target formulation** to reduce error amplification
- **chunked loss weighting** to stabilize over length
- **reconsideration of decomposition approach** if feedback dynamics are fundamentally incompatible

At this point Project 5 should continue only through interventions that directly address:
- error accumulation mechanisms
- feedback stability
- or fundamental restructuring of the composition strategy

Not:
- further local representation improvements
- (we already proved 92% local accuracy is insufficient)

---

## 12. Current Status (Updated)

**Project 5 status:** active  
**Synthesis level:** refined interim synthesis  
**Closure status:** not yet closed  
**Major breakthrough:** hypothesis shifted from representation to error dynamics  
**Main contribution so far:** decomposition robustness has been converted from a vague idea into a structured exclusion-and-dynamic-map

---

## 13. Critical Recent Insight

The discovery that 92% local accuracy produces 0.0 composed accuracy is profound because it proves:

> The bottleneck is **not** how well the local model learns, but **how errors from one step affect future steps**.

This is a fundamental shift in Project 5's understanding.

---
