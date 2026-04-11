# CLAIM_LOCK_STATUS — Project 12

## Project 11 — Validation Summary

### Metrics
- **Total claims drafted:** 8
- **Claims with numeric acceptance criteria (full):** 8 ✅
- **Claims with TBD acceptance criteria:** 0
- **Claims marked strong:** 3
- **Claims marked medium:** 3
- **Claims marked weak:** 2

### Claim breakdown

| Claim ID | Status | Type | Has metrics | Has baselines | Notes |
|---|---|---|---|---|---|
| P11-C01 | untested (Project 12) | strong | ✅ | ✅ | Soft clamp mechanism; deterministic |
| P11-C02 | untested (Project 12) | medium | ✅ | ✅ | Dense NN resolution scaling; deterministic |
| P11-C03 | untested (Project 12) | strong | ✅ | ✅ | Boundary-only fails; 3 seeds |
| P11-C04 | untested (Project 12) | strong | ✅ | ✅ | **Core efficiency claim**; 3 seeds; comparison to NN81 |
| P11-C05 | untested (Project 12) | medium | ✅ | ✅ | Ratio sweep + kNN; 5 seeds |
| P11-C06 | untested (Project 12) | weak | ✅ | ✅ | Diminishing returns past N=1000; 3 seeds |
| P11-C07 | untested (Project 12) | strong | ✅ | ✅ | Boundary performance under soft clamp; deterministic |
| P11-C08 | untested (Project 12) | weak | ✅ | ✅ | Build efficiency + leakage prevention; deterministic |

### Run specifications summary

| Phase | Holdout size | Deterministic? | Seeds | Seed list |
|---|---|---|---|---|
| Phase D (resolution) | 800 | ✅ Yes | 1 | seed=223311 (locked holdout) |
| Phase E2 (sample efficiency) | 800 | ❌ Stochastic | 3 | [101, 202, 303] |
| Phase E3 (ratio + kNN) | 800 | ❌ Stochastic | 5 | [111, 222, 333, 444, 555] |

### Data integrity Status

✅ **Leakage prevention stated in protocol:**
- Holdout locked in Phase D (seed 223311)
- Sampling pool (pool_size=60000) separate from holdout (stated by PHASE_E3 protocol)
- No test-set reuse across phases (stated by protocol design)
- All selection/tuning based on pool, not holdout (stated by protocol)
- **Note:** Project 12 will independently verify via explicit holdout ∩ reference = ∅ assertion.

✅ **Reproducibility:**
- Seed lists explicit
- Deterministic phases identified
- Artifact locations documented

### Outstanding items (for Sprint 2)

**Critical (must address):**
- Compute mean ± std / CI explicitly for E2/E3 claims (currently Project 11 artifacts lack std reporting in tables)
- Verify Project 11 artifact JSONs contain seed/parameter metadata
- Generate new re-validation runs on independent holdout/pool seeds (Project 12 validation prerequisite)

**Structural (pre-Sprint 3):**
- Verify baselines (dense NN, uniform, boundary, mixed, 1-NN, 3-NN) match specifications
- Create manifest for reproducible grid runs
- Establish traceability map from claims → validation runs

### Ready for Sprint 2?

✅ **YES — with conditions.** FORMAL_CLAIMS.md claims are **locked** with all 8 Project 11 claims numerically specified and status corrected to `untested (Project 12)`.

**Sprint 2 objectives (next):**
1. **Baseline verification** — confirm dense NN, uniform, boundary, mixed, 1-NN, 3-NN implementations match specifications exactly
2. **Manifest creation** — define reproducible grid runs with pre-registered acceptance thresholds (no data-driven modification)
3. **Artifact metadata inspection** — load Project 11 artifact JSONs to verify seed integrity, run parameters, git hash integrity
4. **Traceability finalization** — complete TRACEABILITY_PROJECT_11.md mapping claims → evidence sources
5. **New seed sampling** — commit independent re-validation seeds for E2/E3 stochastic phases (must differ from Project 11: [101,202,303] and [111,222,333,444,555])

**Critical gate:** Do NOT execute Project 12 grid runs until all baselines verified and manifest locked.

---

## Project 4–10 (Future)

Planned in subsequent sprints. Project 11 extraction/locking serves as template.

