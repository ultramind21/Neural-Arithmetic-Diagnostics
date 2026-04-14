# PROJECT 6 SUCCESS VS FAILURE RESULTS
## Internal Activation Contrast under Local Arithmetic

**Date:** April 2026  
**Project:** 6  
**Status:** COMPLETE  
**Verdict:** PASS

---

## Purpose

This document records the second accepted interpretability result in Project 6.

Its purpose was to test whether successful and failing local arithmetic cases are distinguishable in hidden activation space.

This moves the project from:
- carry-selectivity alone
to
- a direct internal-behavioral contrast

---

## Main Result

The experiment showed that successful and failing local cases are strongly separable in hidden activation space.

This means the model's internal states do not merely encode carry-related information in the abstract. They also differ systematically according to whether the arithmetic computation succeeds or fails.

This is a stronger mechanistic signal than carry selectivity alone.

---

## Why This Result Matters

This result is important because it links:
- **internal representation**
to
- **behavioral correctness**

That is one of the core goals of mechanistic interpretability.

Projects 4 and 5 established structured behavioral patterns and bottlenecks.
Project 6 now shows that these behavioral differences are accompanied by clear internal activation contrasts.

This is a meaningful advance.

---

## Observed Pattern

The experiment found:

- very strong local overall performance
- a small number of failure cases
- and strong activation differences between successful and failing cases

A small subset of hidden units showed especially strong separation between the two groups.

This suggests that:
- the model's hidden space is not behaviorally neutral
- and that some units may play a disproportionate role in distinguishing reliable from unreliable local arithmetic states

---

## What This Establishes

This result establishes the following:

1. successful and failing local arithmetic cases are not internally mixed together
2. hidden activation structure contains clear success-vs-failure information
3. some units appear much more diagnostic than others
4. Project 6 can now identify not only arithmetic-related state variables, but also behavior-linked internal contrasts

---

## Why This Is Stronger Than the First Probe

The first Project 6 result showed that:
- carry-conditioned models encode carry more strongly than simpler local baselines

That was useful, but it was still a variable-level probe.

This second result is stronger because it directly asks:
- what differs internally when the model succeeds vs fails?

That makes it closer to mechanistic diagnosis rather than simple representational presence.

---

## Correct Interpretation

The strongest safe interpretation is:

> under the current carry-conditioned local model, successful and failing arithmetic cases occupy measurably different regions of hidden activation space, and a small subset of units appears especially important in that separation.

This is a strong and valid mechanistic signal.

---

## What This Does NOT Yet Prove

This result does not yet prove:

- that the identified units are causally necessary
- that the top units alone form a complete arithmetic circuit
- that the full internal mechanism is now solved
- that the same structure automatically explains the larger Project 5 family-level failures

Those remain open questions.

---

## Scientific Value

This result gives Project 6 a stronger internal footing.

Project 6 can now say that:
- internal carry-related structure exists
- and internal success/failure contrasts also exist

Together, these results show that mechanistic interpretation in this sandbox is not merely speculative. It is empirically tractable.

---

## Recommended Next Step

A natural next step is to deepen this contrast through one of:

- stronger decodability testing
- ablation of top diagnostic units
- comparison between rescued and unrecovered family-local cases
- causal perturbation of the most selective units

This would move the project from contrastive observation toward stronger causal interpretability.

---

## Formal Status

**Result:** PASS  
**Type:** internal success-vs-failure contrast result  
**Main message:** successful and failing local arithmetic cases are strongly distinguishable in hidden activation space

---
