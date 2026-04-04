# PROJECT 5 SYNTHESIS V1
## Decomposition Robustness Exploration — Current Scientific Position

**Date:** April 2026  
**Project:** 5  
**Status:** ACTIVE SYNTHESIS  
**Scope:** interim synthesis, not final closure

---

## 1. Purpose

This document records the first strong synthesis point of Project 5.

Project 5 began from a focused structural question:

> Does decomposition improve structural robustness in neural arithmetic?

The experiments completed so far now support a much sharper and more informative position than the starting question alone.

This synthesis is therefore intended to:
- consolidate the accepted results
- clarify what has already been learned
- distinguish what is established from what remains open
- and define the most meaningful next step

---

## 2. Accepted Core Results So Far

The currently accepted Project 5 result chain is:

### Result 1
**Structural decomposition with exact local oracle works perfectly.**

This established that decomposition is structurally feasible if carry is handled correctly across chunk boundaries.

### Result 2
**A learned local processor fails, and the bottleneck is not uniform.**

The first learned local processor showed:
- carry prediction can be perfect
- digit prediction remains weak
- and the composed decomposition collapses

### Result 3
**The learned bottleneck is strongly carry-conditioned.**

The failure is concentrated especially in local digit prediction under `carry_out = 1` conditions.

### Result 4
**Simple loss reweighting does not rescue the bottleneck.**

Reweighting digit-loss on carry-producing cases worsened performance rather than fixing it, ruling out a simple class-imbalance explanation.

### Result 5
**Explicit carry-conditioned representation substantially improves local learnability.**

This changed the local problem dramatically:
- local digit accuracy improved strongly
- carry-conditioned local digit performance improved sharply
- and at least one family was rescued completely

### Result 6
**Chunk size does not explain the remaining family split.**

Changing decomposition granularity did not alter the core pattern:
- one family remained rescued
- the others remained failed

### Result 7
**The rescued family is structurally the simplest family.**

The rescued family (`full_propagation_chain`) has:
- zero transition burden
- minimal local diversity
- uniform local state structure

The unrecovered families involve:
- higher transition density
- more local pair diversity
- and more mixed structure

---

## 3. Main Scientific Position Now

The strongest current Project 5 position is:

> Decomposition is structurally feasible in principle, but learned decomposition succeeds only when the local processor both represents carry explicitly and operates on structurally simple local state distributions.

This is a much sharper conclusion than the starting question.

Project 5 no longer asks only:
- whether decomposition works

It now shows:
- decomposition can work
- simple learned local processing fails
- simple weighting fixes do not solve the problem
- explicit carry-aware representation helps substantially
- but the rescue remains limited to the structurally simplest family

This is already a significant research outcome.

---

## 4. What Has Been Ruled Out

Project 5 has already ruled out several simpler explanations:

### Not just "decomposition is bad"
False.
The exact local oracle result shows decomposition can preserve full correctness.

### Not just "carry is the problem"
False in the simple sense.
Carry can be predicted perfectly even when digit prediction fails.

### Not just "class imbalance"
False in the straightforward sense.
Carry-conditioned loss reweighting did not fix the bottleneck.

### Not just "chunk size"
False in the current tested range.
Changing chunk size did not alter the core family split.

These eliminations are important because they make the project scientifically cumulative rather than repetitive.

---

## 5. What the Project Now Suggests

The current evidence suggests that the true bottleneck lies in the interaction between:

- local carry-conditioned digit transformation
- local state diversity
- and the structural complexity of family-level transition patterns

In other words, the problem is no longer well described as:
- "models do not learn carry"
or
- "chunking breaks the solution"

The more precise position is:

> learned local decomposition may require a representation that can remain reliable under both carry-conditioned local arithmetic and structurally diverse local transition regimes.

This is a stronger and more useful research conclusion.

---

## 6. Why the Rescued Family Matters

The fact that `full_propagation_chain` was rescued is not trivial.

It shows that:
- the explicit carry-conditioned intervention is doing something real
- the learned local processor is not uniformly broken
- and at least one difficult family can be fully recovered

But the structural analysis also shows why this is not yet broad success:
- the rescued family is the least diverse and least transitional one

This means the intervention is real, but its robustness is still narrow.

That mirrors a familiar pattern from earlier work:
- real gain
- without broad transfer

Project 5 therefore extends that logic from model-level interventions into decomposition-level interventions.

---

## 7. Strongest Current Interpretation

The most defensible current interpretation is:

> Project 5 has shown that explicit carry-conditioned representation is a meaningful decomposition intervention, but that its benefits are currently limited to families with low local structural diversity and low transition burden.

This is neither a null result nor a full success story.

It is a structurally informative partial success.

---

## 8. What Project 5 Does NOT Yet Establish

Project 5 does not yet establish:

- a generally successful learned decomposition method
- a final decomposition architecture
- a full mechanistic account of why the remaining families fail
- a proof that explicit carry-conditioned representation is the final answer
- closure of the decomposition question as a whole

The project remains open.

---

## 9. Why This Is Already Valuable

Even without final closure, Project 5 is already scientifically valuable because it has transformed a vague architectural intuition into a set of increasingly precise empirical claims.

It established:
- what works in principle
- what fails in learned form
- what simple fixes do not help
- what representation change does help
- and what structural condition still separates success from failure

That is substantial progress.

---

## 10. Most Meaningful Next Step

The next meaningful question is now:

> What kind of local representation or local processor is strong enough to handle higher local structural diversity, not just carry-aware uniform families?

This suggests the next branch should focus on:
- stronger local representational structure
- richer local context encoding
- alternative local target formulations
- or transition-aware local architectures

That is now the correct frontier of Project 5.

---

## 11. Current Project 5 Status

**Project 5 status:** active  
**Current synthesis level:** strong interim synthesis  
**Closure status:** not yet closed  
**Scientific position:** decomposition can work, but learned robustness remains structurally selective

---
