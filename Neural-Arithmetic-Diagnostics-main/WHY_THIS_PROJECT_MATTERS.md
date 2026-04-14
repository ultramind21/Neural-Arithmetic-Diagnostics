# WHY THIS PROJECT MATTERS
## Neural-Arithmetic-Diagnostics

Most AI projects report accuracy.  
Far fewer show what that accuracy *means*, what it fails on, and what survives re-checking.

**This repository matters because it preserves the full arc**:
research → hidden weakness → audit → reconstruction → mechanism/architecture/theory → and finally **validated evidence** (Project 12 Phase 1).

---

## TL;DR
Arithmetic is a clean testbed for a serious question:

> When a model performs well, is it reasoning robustly—or is it succeeding inside a narrow pattern bubble?

This repository does not stop at "the score is high". It uses structured families, adversarial stress tests, audits, and validation gates to separate:
- **brittle thresholds** from **robust mechanisms**,
- **narrow gains** from **broad transfer**,
- and **narrative** from **evidence**.

If you want the evidence-first entry point, start here:
- `project_12/docs/VALIDATED_RESULTS_MASTER_PHASE1.md`
- `project_12/docs/PAPER_DRAFT_PHASE1.md`

---

## How to verify
Verify the entire validation infrastructure in one command:
```bash
python tools/verify_platform_p0.py
```

For detailed integrity checks, see `docs/REPRODUCIBILITY.md`.

---

## What this repository is (one sentence)
A research program on neural arithmetic reasoning that turns experiments into **validated evidence** via locked claims, manifests, artifacts, and validation gates (Project 12).

---

## Why this is scientifically important
Arithmetic is not "just a toy problem." It is one of the clearest places to test:

- **robustness** under structured families (not just random test sets),
- **transfer** across pattern families,
- **boundary behavior** near transitions (where many systems break),
- **mechanistic structure** inside the model (not just outputs),
- and whether higher-level "theory" survives falsification pressure.

This repository matters because it treats *failure* as scientific information, not as something to hide.

---

## Why this is methodologically important
The strongest contribution is not a single number. It is a way of working:

- verify before claiming,
- separate observation from claim from evidence,
- preserve caveats instead of burying them,
- use structured adversarial evaluation, not only standard test sets,
- treat theory as a hypothesis that must survive falsification,
- and upgrade claims when absolute thresholds fail but mechanisms survive.

### Project 12 (Phase 1) — the key methodological upgrade
Project 12 adds a validation layer that makes the repository **publication-safe**:
- claim locking (Observed vs Targets),
- baseline-first comparisons,
- manifest-driven execution,
- copy+patch reproduction enforced by diff gates,
- reproduction checks (deterministic) vs policy checks (stochastic training),
- and evidence-only snapshots with verified paths.

Phase 1 validates the P11 + P4 evidence bundle and provides a paper-ready draft + figures:
- `project_12/docs/PAPER_DRAFT_PHASE1.md`
- `project_12/paper_assets/`
- `project_12/docs/SUBMISSION_CHECKLIST_PHASE1.md`

---

## Why the audit matters
Many projects would stop before auditing. This repository did not.

The audit matters because it turned the repo into something stronger than a research narrative:
- it became a **verified archive** of what survived re-checking.

Start here:
- `final_audit/README.md`

---

## Why the post-audit projects matter (what each branch adds)
These projects are not "more experiments"; they are different ways of attacking the same robustness question.

### Project 4 — Diagnostic framework (post-audit foundation)
Distinguishes between:
- narrow gains vs broader robustness transfer,
- stability-aware interpretation,
- structured adversarial evaluation.

### Projects 5–8 — decomposition → bridge → architecture
A sequence that asks:
- why local competence may fail to scale globally,
- why families fail through heterogeneous mechanisms,
- and how architecture can be redesigned to rescue specific failure modes.

### Project 9 — higher-dimensional compositional worlds
Tests whether the story changes in richer structured spaces:
- topology matters,
- family identity matters,
- rescue policy matters.

### Project 10 — theory-building under adversarial pressure
Shows that higher-order unifications must survive falsification:
- when necessity-style "universal laws" fail,
- the surviving theory may be a threshold-structured regime space with transition bands and boundary geometry.

### Project 11 — boundary behavior + sampling/resolution tradeoffs
Adds a practical, packaged outcome:
- boundary behavior can dominate which predictor looks "best,"
- dense NN defines an upper bound,
- structured sampling closes much of the gap at far lower cost,
- and mechanism shifts (hard clamp → soft clamp) can remove boundary pathologies.

Packaged entry:
- `project_11/packaging/EXECUTIVE_ABSTRACT.md`

---

## What is validated right now? (Phase 1, evidence-first)
If you want "what is actually locked as evidence," use Project 12 snapshots:

- Master snapshot:
  - `project_12/docs/VALIDATED_RESULTS_MASTER_PHASE1.md`

Two key Phase 1 lessons:
1) **Brittle absolute thresholds vs robust mechanisms (P11):**
   - an absolute boundary threshold claim is rejected-as-stated,
   - a mechanism-based revision remains robust (C07 → C07R).
2) **Narrow transfer with negative transfer (P4):**
   - adversarial training can improve seen families while degrading held-out structure,
   - validated via policy checks and a small multi-seed smoke check.

---

## Who should care
If you care about:
- reasoning, generalization, robustness,
- interpretability and failure structure,
- evaluation discipline and reproducible science in AI,

this repository matters—not because it claims everything is solved,
but because it shows how to keep conclusions honest as the "easy interpretation" breaks.

---

## Final thought
The real value here is not a perfect model.

It is refusing to confuse high performance with deep understanding—and then building the tools and evidence layer needed to make that refusal operational.
