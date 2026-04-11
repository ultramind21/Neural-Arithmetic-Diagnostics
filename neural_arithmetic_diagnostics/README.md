# Neural-Arithmetic-Diagnostics
## From Arithmetic Performance to Robustness, Mechanism, Architecture, and Threshold-Structured Composition

A research repository on arithmetic reasoning in neural networks. It preserves:
- the historical research line (Projects 1–3),
- a full trust-recovery audit,
- a post-audit diagnostic framework (Project 4),
- decomposition and interpretability research (Projects 5–6),
- local-to-global and architecture-level composition work (Projects 7–9),
- theory-building under adversarial pressure (Project 10),
- and a major mechanism + sampling extension (Project 11).

**NEW (Project 12, Phase 1):** this repository now includes a reproducibility-first validation layer that converts key results into a system of evidence (locked claims → manifests → artifacts → gates), with paper-ready outputs.

---

## Why this repository matters

Neural models can achieve high arithmetic accuracy and still fail in structured, surprising, and scientifically important ways.

This repository matters because it does not stop at:
- high benchmark scores
- or shallow interpretations of success

Instead, it documents a full research arc that moved through:

- **Projects 1–3:** original arithmetic-learning research
- **A full trust-recovery audit:** to determine what was actually supported
- **Project 4:** a diagnostic framework for distinguishing narrow gains from broader structural robustness
- **Projects 5–9:** decomposition, mechanistic interpretability, local-to-global bridging, and family-sensitive composition design
- **Project 10:** compositional failure laws and a threshold-structured regime-space theory
- **Project 11:** predictive regime theory stress tests + transfer + boundary failure analysis + hard-clamp vs soft-clamp mechanism shift + structure-guided sampling
- **Project 12 (Phase 1):** validation & consolidation protocol (repro checks, policy checks, diff gates, link integrity gates) + paper-ready bundle

### Core message
> **High arithmetic accuracy alone is not sufficient evidence of robust reasoning.**

### Extended lesson after Project 10
> Even higher-order theoretical unifications must survive adversarial pressure; when they do not, the stronger result may be a threshold-structured regime theory rather than a simple universal law.

### Extended lesson after Project 11 (mechanism + sampling)
> Hard clamp discontinuities can concentrate errors near boundaries; replacing them with smooth saturation (soft clamp) restores global consistency and enables interpretable structure to guide sample-efficient evaluation (coverage + boundary-focused sampling).

---

## Start here (fast paths)

### Human motivation
- `WHY_THIS_PROJECT_MATTERS.md`

### Fast technical entry
- `GETTING_STARTED_FAST.md`

### Project 11 packaged results (evidence + figures)
- `project_11/packaging/EXECUTIVE_ABSTRACT.md`
- `project_11/packaging/PACKAGING_INDEX.md`

### NEW: Project 12 validation closure + paper bundle (Phase 1)
- **Master validated snapshot:** `project_12/docs/VALIDATED_RESULTS_MASTER_PHASE1.md`
- **Paper draft (Markdown):** `project_12/docs/PAPER_DRAFT_PHASE1.md`
- **Paper assets (figures/tables):** `project_12/paper_assets/`
- **Submission checklist:** `project_12/docs/SUBMISSION_CHECKLIST_PHASE1.md`
- **PDF build instructions:** `project_12/paper_build/README.md`

---

!

---

## What makes this repository different

This is not just:
- a code dump
- a benchmark repository
- or a sequence of disconnected experiments

It contains:
- a **historical research line** (Projects 1–3)
- a **verification archive** (the audit)
- a **post-audit diagnostic framework** (Project 4)
- a **multi-branch research program** (Projects 5–10)
- a **mechanism + sampling extension** (Project 11)
- and a **reproducibility-first validation layer** (Project 12)

In other words, it preserves both:
- scientific results
- and the process by which those results were tested, corrected, stress-tested, and consolidated into evidence.

---

## Key result in one paragraph (updated through Project 12 Phase 1)

Across the research line, strong arithmetic performance on standard/random tests repeatedly turned out to be insufficient for strong reasoning claims. Structured adversarial tests revealed hidden weaknesses; the audit locked important caveats; Project 4 introduced a framework for distinguishing narrow gains from broader structural robustness; and Projects 5–10 developed decomposition, interpretability, composition, and regime-theory perspectives under adversarial pressure. Project 11 then identified a critical mechanism: **hard clamp discontinuities concentrate errors near boundaries**, while **soft saturation (soft clamp) restores smoother regime structure**, and structure-guided sampling can approach dense nearest-neighbor performance with far fewer reference points. Project 12 (Phase 1) converts these outcomes into a **validated evidence bundle**: locked claims, manifest-driven execution, copy+patch reproduction enforced by diff gates, reproduction checks for deterministic procedures, and policy checks for stochastic interventions—yielding publication-safe validated/rejected/revised claims with explicit provenance.

---

## Repository at a glance

```text
neural_arithmetic_diagnostics/
├── src/                    # Core executable project code
├── Papers/                 # Historical research line (Projects 1–3)
├── final_audit/            # Trust-recovery verification archive
├── project_4/              # Diagnostic Arithmetic Reasoning
├── project_5/              # Decomposition Robustness Exploration
├── project_6/              # Mechanistic Interpretability Sandbox
├── project_7/              # Local-to-global failure bridge analysis
├── project_8/              # Composition stabilization architectures
├── project_9/              # High-dimensional compositional sandboxes
├── project_10/             # Rescue regime theory / threshold-structured regime space
├── project_11/             # Mechanism + transfer + boundary + sampling + packaging
│   └── packaging/          # Packaged outputs (evidence + figures + claims)
├── project_12/             # Validation & consolidation protocol + paper bundle
├── tests/                  # Test files
├── checkpoints/            # Original checkpoints
└── README.md
```

---

## The main layers of the repository

### 1) Projects 1–3 — Historical research line
- `Papers/`
Start: `Papers/README.md`

### 2) Audit — Verification archive
- `final_audit/`
Start: `final_audit/README.md`

### 3) Projects 4–11 — Core research program
Start: `PROJECT_STRUCTURE.md` and each project's README.

### 4) Project 12 — Validation & paper-ready outputs (Phase 1)
- `project_12/`
Start:
- `project_12/docs/VALIDATED_RESULTS_MASTER_PHASE1.md`
- `project_12/docs/PAPER_DRAFT_PHASE1.md`

---

## Current repository status (updated)

- Projects 1–3: complete, historically preserved, audit-qualified where needed
- Audit: complete, integrity-checked, final trust position documented
- Projects 4–11: complete with bounded qualifications where appropriate
- Project 12 Phase 1: complete (validated evidence bundle + paper-ready outputs)

---

## Final note

This repository should be read as a full scientific arc:
historical results → hidden weakness → trust crisis → audit → diagnostic reconstruction → mechanistic and compositional research → regime theory → mechanism/sampling extension → evidence consolidation.

*Status: Research line archived-as-artifacts | Audit complete | Projects 4–11 complete | Project 12 Phase 1 validated & paper-ready*  
*Project identity: Neural-Arithmetic-Diagnostics*

**License:** Custom non-commercial license. Any commercial use requires prior written permission from Mohamed Mhamdi.
