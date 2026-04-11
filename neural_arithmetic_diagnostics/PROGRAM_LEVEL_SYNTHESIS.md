# PROGRAM LEVEL SYNTHESIS
## Neural-Arithmetic-Diagnostics — Program Position (with Phase-1 Validation Overlay)

**Date:** April 2026  
**Status:** Current program synthesis (post-audit) + Project 12 Phase 1 validation overlay

---

## TL;DR
This repository is a research program on arithmetic reasoning in neural networks. A central lesson persists across the line:

> High arithmetic performance alone is not sufficient evidence of robust reasoning.

**Project 12** adds a validation layer that converts selected results into **reproducible evidence** (locked claims → manifests → artifacts → gates).  
Phase 1 of Project 12 validates **Project 11 + Project 4**; Projects 5–10 remain part of the post-audit research synthesis but are not yet consolidated under Project 12.

---

## 1. Purpose
This document states the current program-level position across the post-audit research line (Projects 4–11), while explicitly distinguishing:

- **Validated evidence (Project 12 Phase 1):** what is supported by reproducible gates today
- **Research synthesis (Projects 5–10):** the strongest current narrative position, pending full Project 12 consolidation

This is a program position document, not a per-project repetition.

---

## 2. What is validated vs. what is synthesis (important)
### 2.1 Validated evidence (Project 12 Phase 1)
Phase 1 produces a paper-ready evidence bundle for:
- **Project 11:** validated claims + one rejected-as-stated threshold claim + a validated mechanism-based revision
- **Project 4:** baseline diagnostics + adversarial-training narrow transfer, validated via policy checks and a 3-seed smoke check

**Primary evidence pointers:**
- Master snapshot: `project_12/docs/VALIDATED_RESULTS_MASTER_PHASE1.md`
- Claim registry: `project_12/docs/FORMAL_CLAIMS.md`
- Paper draft: `project_12/docs/PAPER_DRAFT_PHASE1.md`
- Evidence index: `project_12/docs/PAPER_READY_PHASE1_EVIDENCE_INDEX.md`

### 2.2 Program synthesis (post-audit line, not fully consolidated yet)
Projects 5–10 contribute strongly to the program arc (decomposition, interpretability, local-to-global bridge, architecture design, higher-dimensional sandboxes, theory-building under falsification pressure). Their conclusions are documented and internally consistent, but they are not yet fully revalidated under Project 12 Phase 1 gates.

---

## 3. The post-audit program arc (Projects 4–11)
### Project 4 — Diagnostic Arithmetic Reasoning (validated in Project 12 Phase 1)
Established a diagnostic framework to distinguish:
- distribution-bound fit
- bounded compositional competence
- stronger algorithm-like behavior

Also provides a validated intervention result: adversarial training can yield narrow transfer (see Section 6).

### Project 5 — Decomposition Robustness Exploration (synthesis)
Showed that decomposition can work structurally, but failures can be selective and not explained by simple one-factor stories.

### Project 6 — Mechanistic Interpretability Sandbox (synthesis)
Showed arithmetic-relevant internal structure is measurable: carry-sensitive signals, subspaces, unit-level probes, and causal/geometric evidence can be collected.

### Project 7 — Local-to-global bridge (synthesis)
Showed local-to-global failure is heterogeneous: some family-level failures are trigger-correctable, others are not.

### Project 8 — Composition stabilization architectures (synthesis)
Showed architecture can be designed on top of diagnosis: family-sensitive rescue mechanisms can be integrated rather than discovered by blind scaling.

### Project 9 — High-dimensional compositional sandboxes (synthesis)
Showed local-to-global propagation remains meaningful in richer arithmetic-like spaces, where topology- and family-sensitive behavior can emerge.

### Project 10 — Law testing + rescue regime theory (synthesis)
Showed that higher-order unifications must be adversarially tested; when necessity claims fail, the surviving higher-level result may be threshold-structured regime-space behavior rather than a flat universal law.

### Project 11 — Structure vs resolution vs sampling (validated in Project 12 Phase 1)
Adds an efficiency axis: structured sampling can approximate dense reference performance at reduced cost, with boundary behavior and mechanism details shaping outcomes.

---

## 4. What the program has established (current best-supported position)
The post-audit line supports the following high-level claims:

A) **High arithmetic performance is not sufficient.**  
Models can look strong under standard tests while failing under structured family diagnostics.

B) **Failure is structured.**  
Failures are family-specific, architecture-sensitive, and composition-sensitive rather than uniform "works/fails" behavior.

C) **Local competence and global robustness differ.**  
Local or partial competence does not automatically scale to global compositional robustness.

D) **Internal structure is real and usable (synthesis).**  
Mechanistic signals can be probed and linked to outcomes, even when they do not yield a single unified explanation.

E) **Global failure is heterogeneous.**  
Different failure families can arise from different mechanisms.

F) **Design can respond to diagnosis (synthesis).**  
Architecture-level interventions can be targeted to distinct failure modes.

G) **Higher-level theory must survive adversarial pressure (synthesis).**  
Theory improves via falsification; a regime-space / threshold-structured account can be more defensible than a universal-law framing.

H) **Efficiency is a first-class axis (validated for Project 11 in Phase 1).**  
Near-dense performance can be approached with structured sampling at lower reference cost; dense NN remains a useful upper-performance reference.

---

## 5. Deepest program insight (calibrated)
A defensible program-level thread is:

> Robust arithmetic behavior is not explained by a single missing ingredient. It is mechanistically layered, failure-structured, and often sensitive to regime boundaries; some statements are brittle as absolute thresholds but stable as mechanism-based criteria.

This is illustrated concretely in Phase 1:
- **Project 11:** one absolute boundary-threshold claim is rejected-as-stated under holdout-seed variation, while a mechanism-based revision remains validated (C07 → C07R).
- **Project 4:** adversarial training can yield narrow transfer and negative transfer (policy-validated, with a 3-seed smoke check).

---

## 6. Phase 1 validated highlights (Project 12 overlay)
### Project 11 (validated)
- Soft clamp enables a competitive interpretable baseline overall (vs hard clamp baseline).
- Dense NN improves with resolution (upper-performance reference).
- Boundary-only sampling underperforms; mixed/global coverage is necessary.
- Mixed sampling at N=1000 achieves near-dense performance with fewer points.
- Absolute boundary threshold claim is brittle (rejected-as-stated); mechanism-based revision is robust (validated).

### Project 4 (validated)
- Baseline diagnostics show architecture-dependent behavior on block-boundary stress and universal collapse on certain adversarial families.
- Adversarial training validates narrow transfer: improvement on seen families coupled with degradation on held-out structure (policy-based validation + 3-seed smoke check).

Primary evidence pointers:
- `project_12/docs/VALIDATED_RESULTS_P11_PROJECT12.md`
- `project_12/docs/VALIDATED_RESULTS_P4_PROJECT12.md`

---

## 7. Strongest current assets (practical)
1) **Project 12 validation layer (Phase 1)** — claims → evidence workflow, paper-ready bundle  
2) **Project 11 packaged results** — reader-friendly evidence tables + efficiency axis  
3) **Project 4 diagnostic framework** — family-level diagnostics + validated narrow-transfer intervention  
4) **Projects 5–10 synthesis** — decomposition, mechanistic probes, bridge heterogeneity, targeted design, higher-dimensional exploration, falsification-driven theory-building

---

## 8. What the program does NOT yet claim
- A final universal arithmetic architecture
- A complete mechanistic theory of all failure families
- A single universal higher-order law that generalizes without qualification
- Fully consolidated Project 12 validation for Projects 5–10 (Phase 1 covers P11 + P4 only)

---

## 9. Best next macro-directions
A) **Publication synthesis:** expand paper-ready packaging from Phase 1 to additional projects (5–10) under the same validation discipline  
B) **Project 10 theory packaging:** produce a cleaner outward narrative with explicit falsification checkpoints  
C) **Extended validation:** apply Project 12 protocols to Projects 5–10 (claim locking → baselines → manifests → evidence snapshots)  
D) **Domain transfer:** test whether the diagnostic + validation logic extends beyond arithmetic

---

## 10. Final program position (concise)
Neural-Arithmetic-Diagnostics is a research program arguing that arithmetic reasoning in neural models cannot be justified by benchmark performance alone. It requires structured diagnostics, mechanistic analysis, family-sensitive interpretations, and—critically—validation discipline that converts experimental outcomes into reproducible evidence. Project 12 Phase 1 demonstrates this conversion for Projects 11 and 4, including a concrete example of rejecting a brittle absolute threshold while validating a mechanism-based revision.
