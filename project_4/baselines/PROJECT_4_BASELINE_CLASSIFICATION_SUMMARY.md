# PROJECT 4 BASELINE CLASSIFICATION SUMMARY
## Initial Stable Baseline Matrix

**Date:** March 31, 2026  
**Framework Version:** 1.0  
**Status:** ACTIVE BASELINE SUMMARY

---

## Purpose

This document records the first stable baseline comparison matrix obtained under Project 4.

At this stage, the goal is not to overstate final regime conclusions, but to document:

- which baselines have now been run under the Project 4 framework
- which results are stable under repeated runs
- what cross-model patterns are already visible
- what should and should not yet be concluded

---

## Validation Status

The following baseline families have now passed repeated-run stability validation under the current bounded Project 4 path:

- **MLP** → STABLE
- **LSTM** → STABLE
- **Transformer** → STABLE

This means the observed patterns below are no longer one-off runs or seed accidents.
They are stable empirical signals under the current evaluation path.

---

## Stable Baseline Matrix

| Dimension | MLP | LSTM | Transformer |
|----------|-----|------|-------------|
| Validation status | STABLE | STABLE | STABLE |
| In-distribution exact-match (mean) | 0.0859 | 0.0469 | 0.0339 |
| Alternating carry | 0.0000 | 0.0000 | 0.0000 |
| Full propagation chain | 0.0000 | 0.0000 | 0.0000 |
| Block-boundary stress | 1.0000 | 0.0000 | 1.0000 |
| Mean adversarial accuracy | 0.67 | 0.00 | 0.33 |

---

## Immediate Observations

### 1. All three baselines are weak in exact-match terms
Under the current bounded evaluation path, all three baselines show low exact-match values even in-distribution.

This means:
- none of the three should currently be treated as strong arithmetic performers under this Project 4 path
- the baseline matrix is informative precisely because it reveals structured weaknesses and differences, not because it confirms strong performance

### 2. Alternating carry and full propagation chain collapse across all three
All three baselines currently score **0.0** on:
- alternating carry
- full propagation chain

This suggests that these structured adversarial families are highly challenging under the current setup.

### 3. Block-boundary stress separates architectures sharply
This is the clearest stable cross-model signal currently observed:

- **MLP = 1.0**
- **LSTM = 0.0**
- **Transformer = 1.0**

This is a stable architecture-dependent difference under the current bounded Project 4 evaluation path.

### 4. LSTM is qualitatively distinct from MLP and Transformer on the current block-boundary test
The block-boundary stress test does not merely show a small numeric difference.
It shows a **binary split** in the current runs:
- MLP and Transformer succeed completely
- LSTM fails completely

This makes block-boundary stress the first especially important discriminative pattern in Project 4 baseline analysis.

---

## What Can Be Defensibly Said Now

The most defensible current baseline interpretation is:

> Project 4 has now produced its first stable baseline comparison matrix.
>
> Under the current bounded evaluation path, all three baseline models perform weakly in exact-match terms, all collapse on alternating-carry and full-propagation-chain tests, and a strong architecture-dependent split appears on block-boundary-stress, where MLP and Transformer succeed while LSTM fails.

This is already a meaningful Project 4 baseline result.

---

## What Should NOT Yet Be Overclaimed

At this stage, the following should still be avoided:

- claiming final regime assignments as if they were settled beyond review
- claiming a causal explanation for why LSTM fails on block-boundary stress
- claiming that the current baseline matrix settles the entire Project 4 research question
- claiming that placeholder dimensions (rounding sensitivity / carry corruption) are already fully informative

---

## Important Qualification

These baseline results are stable under repeated runs, but they are still produced under the current bounded Project 4 evaluation path.

Therefore:
- they are valid baseline signals
- but they remain part of a living framework
- and some dimensions are still less mature than others

In particular:
- rounding sensitivity is still placeholder-limited
- carry corruption is still placeholder-limited

So the strongest baseline conclusions should focus on:
- exact-match stability
- adversarial pattern contrast
- architecture-dependent differences already observed

---

## Current Working Regime Position

At this stage, all three baselines remain in a **non-Regime-3 zone**.

More specifically:
- none of the three currently provides evidence of strong algorithm-like generalization
- all three show major structured weaknesses
- the baseline matrix is more useful diagnostically than as a success story

Formal regime labels should remain:
- **tentative**
- **human-reviewed**
- and tied to later Project 4 synthesis, not this file alone

---

## Strategic Value for Project 4

This baseline matrix is important because it gives Project 4 a real starting point for intervention work.

It already tells us:
- what all three models fail on together
- where at least one architecture split appears
- and which adversarial families are most informative for the next step

That is exactly what a diagnostic framework is supposed to provide.

---

## Recommended Next Step

Proceed to the MVP intervention stage:

- **Adversarial Training**

The baseline matrix is now stable enough to justify intervention experiments.

In particular, future intervention analysis should test:
- whether alternating and full-chain collapse can be reduced
- whether block-boundary robustness transfers across architectures
- whether improvements generalize beyond the seen adversarial patterns

---

## Formal Status

**Baseline matrix status:** STABLE  
**Project 4 phase:** READY FOR MVP INTERVENTION  
**Strongest current baseline signal:** architecture-dependent split on block-boundary stress

---
