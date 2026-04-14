# PROJECT 4 ADVERSARIAL TRAINING RESULTS
## MVP Intervention Record

**Date:** March 31, 2026  
**Project:** 4  
**Intervention:** Adversarial Training  
**Status:** COMPLETE  
**Verdict:** PASS WITH QUALIFICATIONS

---

## Purpose

This document records the first MVP intervention result in Project 4.

The purpose of this intervention was to test whether adversarial training improves:

- genuine structural robustness,
- or only performance on specifically seen adversarial families.

This is a Project 4 framework result, not a final mechanistic proof.

---

## Intervention Setup

### Base model family
- Phase 30 MLP baseline

### Seen adversarial families used in augmentation
- `alternating_carry`
- `full_propagation_chain`

### Held-out adversarial family
- `block_boundary_stress`

### Evaluation goal
Distinguish between:
1. **narrow seen-family gain**
2. **broader robustness transfer**

---

## Repeated-Run Stability Status

Repeated runs were executed and the resulting pattern-level outcome was stable across the intervention runs reviewed in this step.

### Stable repeated pattern
- `alternating_carry` → stable success
- `full_propagation_chain` → stable failure
- `block_boundary_stress` → stable failure
- in-distribution exact-match remained low

This means the intervention result is not being treated as a one-off artifact.

---

## Core Observed Pattern

### Baseline reference pattern
Before intervention, the baseline pattern was approximately:

- `alternating_carry` → failure
- `full_propagation_chain` → failure
- `block_boundary_stress` → success

### Adversarial-training intervention pattern
After intervention, the observed stable intervention pattern was approximately:

- `alternating_carry` → success
- `full_propagation_chain` → failure
- `block_boundary_stress` → failure

---

## Main Finding

The most important current finding is:

> The adversarial-training intervention produced a stable improvement on one seen adversarial family (`alternating_carry`), but did not generalize that improvement to another difficult family (`full_propagation_chain`) and was associated with failure on the held-out family (`block_boundary_stress`).

This is the first stable intervention signal in Project 4.

---

## What This Supports

This result supports the following bounded interpretation:

- adversarial training can materially change model behavior on at least one seen structured family
- that gain does **not** automatically imply generalized structural robustness
- transfer across adversarial families is not guaranteed
- intervention gains may come with trade-offs or redistribution of failure

In other words:

> this result is consistent with **narrow family-specific fitting** rather than robust adversarial generalization.

---

## What This Does NOT Prove

This result does **not** by itself prove:

- the exact internal mechanism of failure
- that the intervention is "just memorization" in a strict mechanistic sense
- that adversarial training can never generalize
- that this single intervention settles Project 4

It is a strong bounded empirical signal, not a full theory.

---

## Qualification

### Validation qualification
The repeated-run behavior for the key intervention metrics was stable, but the general validation utility returned only a partial formal verdict because the intervention validation payload did not fully mirror a complete baseline-style scorecard payload.

This does **not** erase the stable repeated signal itself.  
It means only that:
- the intervention-specific validation packaging is not yet as mature as the baseline validation packaging.

### Interpretation qualification
This result should be interpreted as:

- stable
- informative
- and scientifically meaningful

but still:
- bounded
- early-stage
- and not yet a full mechanism claim

---

## Scientific Value of This Result

This is an important Project 4 MVP result because it demonstrates exactly the kind of distinction the framework was designed to detect:

- **improvement on seen adversarial structure**
versus
- **transfer of robustness to unseen structure**

The intervention currently supports the first more than the second.

That is already scientifically valuable.

---

## Current Best Interpretation

The most defensible current interpretation is:

> Under the current bounded Project 4 intervention setup, adversarial training improved performance on a seen adversarial family, but did not produce evidence of broad robustness transfer across adversarial structure families.

This makes the intervention result:
- meaningful
- stable
- and directly relevant to Project 4's main question

---

## Recommended Next Step

The next logical step is **not** to over-interpret this result, but to use it to guide the next Project 4 move.

Recommended immediate follow-up options include:
1. extending validation packaging for intervention runs
2. comparing this intervention effect against additional baselines or architectures
3. moving toward the next structural intervention stage once MVP evidence is documented

---

## Formal Status

**Intervention result:** PASS WITH QUALIFICATIONS  
**Project 4 role:** First stable MVP intervention signal  
**Main conclusion:** seen-family gain without robust held-out transfer

---
