# PROJECT 6 CARRY SELECTIVITY RESULTS
## First Interpretability Probe

**Date:** April 2026  
**Project:** 6  
**Status:** COMPLETE  
**Verdict:** PASS WITH QUALIFICATIONS

---

## Purpose

This document records the first accepted interpretability result in Project 6.

Its purpose was to test whether carry-related information is measurably represented in the hidden activations of local arithmetic models.

---

## Experiment Summary

The first probe compared two local model families:

1. a simpler local model
2. a carry-conditioned local model

For each model, hidden activations were analyzed under two local output conditions:

- `carry_out = 0`
- `carry_out = 1`

The experiment then measured a first separability statistic for hidden units.

---

## Main Result

The carry-conditioned model showed stronger carry separability than the simpler model under the current probe.

This means that:

- carry-related information is not only behaviorally relevant
- it is also more clearly represented in the hidden activations of the carry-conditioned model

This is the first positive internal-representation signal in Project 6.

---

## What This Establishes

This result establishes the following:

1. hidden activations contain measurable carry-related structure
2. carry-conditioned architecture strengthens that internal distinction
3. some hidden units appear substantially more carry-selective than others
4. Project 6 can already detect meaningful representational differences, not just behavioral ones

---

## Why This Matters

This is important because it moves the research line one step beyond behavioral diagnosis.

Projects 4 and 5 mainly established:
- where models succeed
- where they fail
- and how failure changes under interventions

Project 6 now begins to ask:
- where relevant arithmetic state may be represented internally
- and whether architectural differences affect that representation

This result suggests the answer is yes.

---

## Qualification

This result remains bounded in several ways:

- it is a first probe, not a full mechanistic proof
- it uses a simple separability statistic
- it does not yet establish a complete circuit-level explanation
- it does not yet prove that the top units are sufficient or necessary for behavior
- it is best understood as an exploratory but valid mechanistic signal

---

## Correct Interpretation

The strongest correct interpretation is:

> carry-conditioned local architecture appears to produce stronger carry-selective internal structure than a simpler local baseline under the current hidden-activation probe.

This is a meaningful result, but not yet a complete mechanistic account.

---

## Recommended Next Step

A natural next step would be to deepen this line in one of the following ways:

- probe additional layers or internal stages
- test linear carry decodability more directly
- compare successful vs failing arithmetic cases
- contrast carry-selective units with digit-error conditions
- move from separability statistics to stronger representation analyses

---

## Formal Status

**Result:** PASS WITH QUALIFICATIONS  
**Type:** first interpretability probe  
**Main message:** carry-selective internal structure is measurably stronger in the carry-conditioned model than in the simpler local baseline

---
