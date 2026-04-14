# PROJECT 6 TRAJECTORY INTERVENTION PLAN
## Hidden-State Damping Probe

**Date:** April 2026  
**Project:** 6  
**Status:** ACTIVE EXPERIMENT PLAN

---

## 1. Purpose

This document defines the next Project 6 experiment.

The purpose is to move from:
- trajectory observation

to:
- trajectory intervention

The core question is:

> If oscillatory trajectory behavior is reduced, does family-level performance improve?

---

## 2. Why This Experiment Now

Project 6 already established that:

- failing and successful families differ at the trajectory level
- alternating carry is associated with strong oscillatory instability
- successful families show stabilization or controlled transitions

This makes trajectory intervention the most natural next step.

---

## 3. Core Hypothesis

### Working hypothesis
Trajectory instability is not only correlated with family-level failure, but is at least partly causally relevant to it.

### Prediction
If hidden-state oscillation is damped or stabilized, some failing family behavior may improve.

---

## 4. First Intervention Type

### Hidden-State Damping
At each sequence step, hidden state will be modified by a damping rule such as:

- partially mixing current and previous hidden state

This is a bounded and interpretable first intervention.

---

## 5. Evaluation Targets

The intervention should be tested at minimum on:

- alternating_carry
- full_propagation_chain
- block_boundary_stress

The most important target is:
- `alternating_carry`

because it showed the clearest oscillatory instability.

---

## 6. What Would Count as a Positive Result

A positive result would be any of the following:

- reduced oscillation in the failing family
- improved family-level exact-match in the failing family
- partial recovery without destroying the already-successful family
- stronger trajectory stability aligned with stronger performance

---

## 7. What Would Count as a Negative But Useful Result

A negative result would still be scientifically valuable if:

- damping reduces oscillation but does not improve performance
- damping harms successful families without rescuing failing ones
- the intervention reveals that oscillation is a symptom rather than a sufficient causal lever

This would still sharpen the mechanistic picture.

---

## 8. Immediate Next Step

The next implementation step is:

- `project_6/experiments/project_6_trajectory_intervention_v1.py`

---
