# Neural-Arithmetic-Diagnostics
## From Arithmetic Performance to Robustness, Mechanism, Architecture, and Threshold-Structured Composition

**A research repository on arithmetic reasoning in neural networks, including the historical research line, a full trust-recovery audit, a post-audit diagnostic framework, decomposition research, mechanistic interpretability, local-to-global bridge analysis, architecture-level composition design, higher-dimensional compositional sandboxes, and a theory-building Project 10 that culminated in a threshold-structured regime-space account of rescue behavior.**

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
- **Project 5:** decomposition robustness exploration
- **Project 6:** mechanistic interpretability sandbox
- **Project 7:** local-to-global failure bridge analysis
- **Project 8:** family-sensitive composition architecture design
- **Project 9:** higher-dimensional compositional sandboxes
- **Project 10:** compositional failure laws and post-adversarial rescue regime theory

### Core message
> **High arithmetic accuracy alone is not sufficient evidence of robust reasoning.**

That remains the central lesson of the repository.

### Extended lesson after Project 10
> **Even higher-order theoretical unifications must survive adversarial pressure; when they do not, the stronger result may be a threshold-structured regime theory rather than a simple universal law.**

This is now one of the deepest lessons of the repository.

### Start here if you want the human reason this project matters
- [`WHY_THIS_PROJECT_MATTERS.md`](WHY_THIS_PROJECT_MATTERS.md)

### Start here if you want the fastest technical entry
- [`GETTING_STARTED_FAST.md`](GETTING_STARTED_FAST.md)

---

![Repository Overview](assets/repository_overview.png)

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
- a **decomposition research branch** (Project 5)
- a **mechanistic interpretability branch** (Project 6)
- a **local-to-global bridge branch** (Project 7)
- a **composition architecture design branch** (Project 8)
- a **higher-dimensional compositional sandbox branch** (Project 9)
- a **theory-building and post-adversarial regime-theory branch** (Project 10)

In other words, it preserves both:
- scientific results
- and the process by which those results were tested, corrected, deepened, redesigned, stress-tested, reformulated, and extended into higher-level theory

---

## Key result in one paragraph

Across the research line, strong arithmetic performance on standard/random tests repeatedly turned out to be insufficient for strong reasoning claims. Structured adversarial tests revealed hidden weaknesses, the audit locked important caveats, Project 4 introduced a framework for distinguishing narrow gains from broader structural robustness, Project 5 showed that decomposition can work in principle while learned decomposition fails selectively, Project 6 demonstrated that arithmetic-relevant internal structure is real and mechanistically meaningful, Project 7 showed that local-to-global compositional failure is not driven by one uniform mechanism, Project 8 demonstrated that family-sensitive rescue mechanisms can be integrated successfully within one architecture, Project 9 showed that higher-dimensional compositional worlds can themselves become topology-sensitive, family-sensitive, and rescue-sensitive, and Project 10 showed that attempts to compress rescue behavior into a simple higher-order law are too strong in their flat form. The stronger surviving result of Project 10 was a threshold-structured regime-space account in which family-aware advantage, mixed behavior, and universal dominance occupy different regions, and the rescue boundary itself shifts with heterogeneity. The repository therefore supports a stronger position than any single benchmark result: arithmetic behavior must be evaluated behaviorally, structurally, mechanistically, architecturally, compositionally, and — at the highest level — through adversarially tested regime theory rather than decorative law language.

---

## Repository at a glance

```text
neural_arithmetic_diagnostics/
├── src/               # Core executable project code
├── papers/            # Historical research line (Projects 1–3)
├── final_audit/       # Trust-recovery verification archive
├── project_4/         # Diagnostic Arithmetic Reasoning
├── project_5/         # Decomposition Robustness Exploration
├── project_6/         # Mechanistic Interpretability Sandbox
├── project_7/         # From Local Competence to Global Compositional Failure
├── project_8/         # Composition Stabilization Architectures
├── project_9/         # High-Dimensional Compositional Sandboxes
├── project_10/        # Compositional Failure Laws and Rescue Regime Theory
├── tests/             # Test files
├── checkpoints/       # Original checkpoints
└── README.md
```

---

## The main layers of the repository

### 1) Projects 1–3 — Historical research line
Located in:
- [`papers/`](papers/)

This is where you find:
- original project closures
- historical findings
- killer-test narratives
- final research-facing interpretations

**Start here:**  
- [`papers/README.md`](papers/README.md)

---

### 2) Audit — Verification archive
Located in:
- [`final_audit/`](final_audit/)

This is where the project's trust was rebuilt after a critical model/source mismatch problem.

It contains:
- executive summaries
- phase closure summaries
- verification scripts
- bounded reproduction outputs
- locked caveats

**Start here:**  
- [`final_audit/README.md`](final_audit/README.md)

---

### 3) Project 4 — Diagnostic Arithmetic Reasoning
Located in:
- [`project_4/`](project_4/)

This project established the post-audit diagnostic framework:
- regimes
- scorecard
- stable baseline matrix
- intervention-based narrow-vs-transfer distinction

**Start here:**  
- [`project_4/README.md`](project_4/README.md)

---

### 4) Project 5 — Decomposition Robustness Exploration
Located in:
- [`project_5/`](project_5/)

This branch asks:
- can decomposition improve structural robustness?
- where does learned local decomposition fail?
- what explanations can be ruled out?

**Current status:** COMPLETE with bounded decomposition conclusions established

---

### 5) Project 6 — Mechanistic Interpretability Sandbox
Located in:
- [`project_6/`](project_6/)

This branch investigates:
- where carry lives internally
- how success and failure differ internally
- which units and subspaces matter causally
- and how arithmetic structure appears in hidden geometry

**Current status:** COMPLETE with strong mechanistic success

---

### 6) Project 7 — From Local Competence to Global Compositional Failure
Located in:
- [`project_7/`](project_7/)

This branch asks:
- why local arithmetic competence can coexist with global family-level failure
- and whether different failure families are driven by different local-to-global mechanisms

**Current status:** COMPLETE with bounded local-to-global bridge conclusions established

---

### 7) Project 8 — Composition Stabilization Architectures
Located in:
- [`project_8/`](project_8/)

This branch asks:
- how to turn local arithmetic competence into globally robust compositional behavior
- whether interface and controller mechanisms can rescue different family-level failures
- and whether family-sensitive rescue can be integrated inside one architecture

**Current status:** COMPLETE with strong architecture-level rescue results established

---

### 8) Project 9 — High-Dimensional Compositional Sandboxes
Located in:
- [`project_9/`](project_9/)

This branch asks:
- how local competence behaves in higher-dimensional compositional state spaces
- whether topology-sensitive and family-sensitive local-to-global propagation emerges
- and whether adaptive family-aware rescue can succeed inside a 3D arithmetic-like world

**Current status:** COMPLETE as the first higher-dimensional sandbox phase

---

### 9) Project 10 — Compositional Failure Laws and Rescue Regime Theory
Located in:
- [`project_10/`](project_10/)

This branch began as a theory-building effort to extract compositional failure laws from Projects 4–9.

It established:
- strong support for Law 1
- strong but bounded support for Law 3
- adversarial weakening of stronger higher-order necessity claims
- and a stronger replacement in the form of a threshold-structured regime-space theory

Its strongest higher-level contribution is that rescue behavior is best understood through:
- regime regions
- transition bands
- threshold structure
- and heterogeneity-dependent boundary geometry

**Current status:** COMPLETE at stable packaged checkpoint

---

## Current repository status

### Projects 1–3
- complete
- historically preserved
- audit-qualified where needed

### Audit
- complete
- integrity-checked
- final trust position documented

### Project 4
- complete
- methodological framework established

### Project 5
- complete
- bounded decomposition conclusions established

### Project 6
- complete
- strong mechanistic interpretability success established

### Project 7
- complete
- bounded local-to-global bridge conclusions established

### Project 8
- complete
- strong architecture-level rescue results established

### Project 9
- complete
- first higher-dimensional compositional sandbox phase established

### Project 10
- complete
- law-testing, adversarial revision, and threshold-regime theory cycle established

---

## Fastest reading path

If you want to understand the repository quickly, read:

1. [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md)
2. [`GETTING_STARTED_FAST.md`](GETTING_STARTED_FAST.md)
3. [`WHY_THIS_PROJECT_MATTERS.md`](WHY_THIS_PROJECT_MATTERS.md)
4. [`STRATEGIC_RESEARCH_MAP.md`](STRATEGIC_RESEARCH_MAP.md)

---

## Best entry points by reader type

### If you want the historical research story
- [`papers/README.md`](papers/README.md)

### If you want the final verification-aligned position
- [`final_audit/README.md`](final_audit/README.md)
- [`final_audit/documentation/executive_summaries/EXECUTIVE_SUMMARY_FINAL.md`](final_audit/documentation/executive_summaries/EXECUTIVE_SUMMARY_FINAL.md)

### If you want the post-audit framework contribution
- [`project_4/README.md`](project_4/README.md)

### If you want the strongest current mechanistic branch
- [`project_6/results/PROJECT_6_SYNTHESIS_FINAL.md`](project_6/results/PROJECT_6_SYNTHESIS_FINAL.md)

### If you want the strongest current local-to-global bridge branch
- [`project_7/results/PROJECT_7_SYNTHESIS_V1.md`](project_7/results/PROJECT_7_SYNTHESIS_V1.md)

### If you want the strongest current architecture-design branch
- [`project_8/results/PROJECT_8_SYNTHESIS_FINAL.md`](project_8/results/PROJECT_8_SYNTHESIS_FINAL.md)

### If you want the strongest current higher-dimensional branch
- [`project_9/results/PROJECT_9_SYNTHESIS_V2.md`](project_9/results/PROJECT_9_SYNTHESIS_V2.md)

### If you want the Project 10 theory-building result
- [`project_10/results/PROJECT_10_PRESENTATION_SUMMARY_V2.md`](project_10/results/PROJECT_10_PRESENTATION_SUMMARY_V2.md)
- [`project_10/results/PROJECT_10_CYCLE_STATUS_SUMMARY_V1.md`](project_10/results/PROJECT_10_CYCLE_STATUS_SUMMARY_V1.md)
- [`project_10/results/PROJECT_10_PHASE_DIAGRAM_ARTIFACT_RENDERED_V1.md`](project_10/results/PROJECT_10_PHASE_DIAGRAM_ARTIFACT_RENDERED_V1.md)

---

## Current strongest scientific position

The repository now supports the following bounded but powerful position:

> Neural arithmetic models can appear strong on standard evaluations while remaining narrow, family-sensitive, mechanistically non-uniform, and compositionally fragile. Robust understanding requires not only benchmark performance, but also structured diagnostics, explicit validation, decomposition analysis, mechanistic probing, local-to-global failure analysis, architecture-level design sensitive to heterogeneous failure modes, exploration of higher-dimensional compositional state spaces, and — at the highest level — adversarially tested threshold-structured regime theory rather than simplistic higher-order law language.

---

## Final note

This repository should be read as a full scientific arc:

- original research
- hidden weakness
- trust crisis
- rigorous audit
- diagnostic reconstruction
- decomposition research
- mechanistic interpretability
- local-to-global bridge analysis
- composition architecture design
- higher-dimensional compositional sandbox exploration
- and finally theory-building under adversarial pressure

That full arc — not any single isolated metric — is the real contribution of the repository.

---

*Status: Research line active | Audit complete | Projects 4–10 complete with bounded/project-specific qualifications where appropriate*  
*Project identity: Neural-Arithmetic-Diagnostics*

**License:** Custom non-commercial license. Any commercial use requires prior written permission from Mohamed Mhamdi.
