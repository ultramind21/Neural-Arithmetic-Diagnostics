# PROJECT 6 TRAJECTORY-PRESERVING INTERVENTION RESULTS
## Selective Hidden-State Smoothing Probe

**Date:** April 2026  
**Project:** 6  
**Status:** COMPLETE  
**Verdict:** PASS

---

## Purpose

This document records the selective trajectory smoothing result in Project 6.

Its purpose was to test whether reducing only the large hidden-state jumps would improve family-level behavior more safely than naive uniform damping.

---

## Main Result

The intervention did not rescue the failing family.

At the same time:
- one successful family remained successful
- another successful family was still damaged
- and the failing family did not recover despite selective smoothing being applied

This is a strong causal boundary result.

---

## What Was Tested

The intervention applied hidden-state smoothing only when the hidden-state difference between successive steps exceeded a threshold.

This was designed to test a more refined hypothesis than naive damping:

- perhaps the damaging factor is not trajectory evolution itself,
- but specifically large oscillatory jumps.

The result does not support that simplified hypothesis.

---

## What This Establishes

This result establishes the following:

1. reducing large hidden-state jumps is not sufficient to rescue the failing family
2. the remaining failure is not well explained by jump magnitude alone
3. selective smoothing can still damage useful family-level dynamics
4. therefore the causal structure of family-level success and failure is more constrained than a simple "smooth the trajectory" view

---

## Why This Matters

This is one of the strongest boundary results in Project 6.

Before this result, one could still suspect that the major remaining problem might be:
- trajectory instability in the sense of large oscillatory jumps

After this result, that explanation becomes substantially weaker.

The current evidence now supports a more careful position:

> sequence-level dynamics matter, but simple suppression of large oscillatory jumps is not the causal handle that restores family-level success.

---

## Correct Interpretation

The strongest safe interpretation is:

> selective hidden-state smoothing does not rescue the failing family and still harms one previously successful family, which shows that large-jump suppression alone is not the primary causal lever behind the remaining family-level failures.

This is a strong negative mechanistic result.

---

## What This Does NOT Yet Prove

This result does not prove:

- that trajectory structure is irrelevant
- that oscillation plays no role at all
- that no trajectory-based intervention could ever help
- or that the full family-level mechanism is now solved

It proves only that:
> this more selective smoothing intervention is not sufficient.

---

## Scientific Value

This result is valuable because it eliminates another plausible but overly simple explanation.

Project 6 now has evidence against both:
- naive global damping
- and selective large-jump smoothing

This significantly tightens the mechanistic search space.

---

## Updated Project 6 Position

After this result, the strongest trajectory-level position is:

- trajectory differences are real
- family-level success and failure are dynamically distinct
- but simple stabilization, even in a more selective form, does not recover the failing family

This makes the remaining problem more interesting, not less.

---

## Recommended Next Step

The next direction should not be:
- more of the same smoothing

Instead, stronger future directions would include:
- richer trajectory interventions
- state-subspace interventions
- or more specific local-to-global causal tracing

---

## Formal Status

**Result:** PASS  
**Type:** selective trajectory intervention result  
**Main message:** suppressing large hidden-state jumps is not sufficient to rescue the failing family and does not provide the missing causal handle

---
