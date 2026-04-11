# TRACEABILITY_PROJECT_11

**Purpose:** Audit trail mapping each Project 11 claim to primary source artifact, table/section, key observed numbers, and extraction notes.

**Scope:** All 8 Project 11 claims (P11-C01 through P11-C08). For each claim, this table provides verifiable traceability for Boss Audit and Sprint 1.6 validation.

---

## Traceability Table

| Claim ID | Primary source | Table/section | Key observed numbers | Source path | Extraction notes |
|---|---|---|---|---|---|
| P11-C01 | FIG_F1_NN_RESOLUTION.md (Phase D) | Overall performance table, soft vs hard clamp rows | V3.1=0.9353, V3=0.8435, gap=0.0918 | `project_11/packaging/out/FIG_F1_NN_RESOLUTION.md` | Deterministic holdout (seed 223311); single row extraction; no variance |
| P11-C02 | FIG_F1_NN_RESOLUTION.md (Phase D) | NN resolution sweep rows (NN11…NN81) | NN11=0.8770, NN21=0.9481, NN41=0.9674, NN81=0.9847 | `project_11/packaging/out/FIG_F1_NN_RESOLUTION.md` | Resolution grid scan; monotonic ordering observed; build times secondary |
| P11-C03 | FIG_F2_SAMPLE_EFFICIENCY.md (Phase E2) | N=1000 rows stratified by strategy | boundary=0.7011, uniform=0.9574, mixed=0.9780 (means over 3 seeds) | `project_11/packaging/out/FIG_F2_SAMPLE_EFFICIENCY.md` + `project_11/results/phase_e2_sample_efficiency/artifact.json` | Stochastic seeds [101, 202, 303]; strategy contrast clear; partial overlap with C04 evidence |
| P11-C04 | KEY_CLAIMS.md (core claim #4) + FIG_F2_SAMPLE_EFFICIENCY.md + FIG_F1_NN_RESOLUTION.md | Core claim narrative + E2 N=1000 mixed + NN81 resolution | mixed@N=1000=0.9780, NN81=0.9847, gap=0.0067, cost ratio=1000/6561≈0.1525 | `project_11/packaging/out/KEY_CLAIMS.md` (narrative), `project_11/packaging/out/FIG_F2_SAMPLE_EFFICIENCY.md` (table), `project_11/packaging/out/FIG_F1_NN_RESOLUTION.md` (baseline) | **Flagship efficiency claim**; composite evidence from 3 tables; ratio computed from explicit point counts |
| P11-C05 | FIG_F3_RATIO_KNN.md (Phase E3) | Best-config row (N=1500, frac=0.5) and k-neighbor sweep | Config(1500,0.5,1-NN)=0.9747, Config(1500,0.5,3-NN)=0.9627, gap=0.0120 | `project_11/packaging/out/FIG_F3_RATIO_KNN.md` + `project_11/results/phase_e3_ratio_knn/artifact.json` | Stochastic seeds [111, 222, 333, 444, 555]; ratio grid extraction; 1-NN > 3-NN ordering |
| P11-C06 | FIG_F2_SAMPLE_EFFICIENCY.md (Phase E2) | Mixed strategy rows across N∈{1000,1500,2000} | mixed@N=1000=0.9780, @N=1500=0.9714, @N=2000=0.9748 | `project_11/packaging/out/FIG_F2_SAMPLE_EFFICIENCY.md` | Stochastic seeds [101, 202, 303]; non-monotonic pattern observed; diminishing returns framing |
| P11-C07 | FIG_F1_NN_RESOLUTION.md (Phase D) | Boundary subset rows for V3, V3.1, NN81 | V3_boundary=0.6685, V3.1_boundary=0.8693, NN81_boundary=0.9291 | `project_11/packaging/out/FIG_F1_NN_RESOLUTION.md` | Deterministic holdout boundary subset (subset of 800 points); mechanism effect quantified |
| P11-C08 | FIG_F1_NN_RESOLUTION.md (build table) + Phase D/E3 protocols | Build time row (NN81) + protocol pool/holdout design | NN81_build_seconds=0.0527, pool_size=60000 (stated in protocol) | `project_11/packaging/out/FIG_F1_NN_RESOLUTION.md` (build), `project_11/docs/PHASE_E3_RATIO_KNN_PROTOCOL.md` (pool design), `project_11/results/phase_c3_sat_margin/holdout_points.json` (holdout lock) | Engineering claim; build cost + protocol structure; leakage prevention stated, independent verification planned |

---

## Claim Interdependencies

**Independent evidence (separate experiments):**
- P11-C01 (Phase D, deterministic)
- P11-C02 (Phase D, deterministic)
- P11-C07 (Phase D, deterministic, boundary subset)
- P11-C08 (Engineering check, deterministic)

**Shared Phase E2 evidence (same 3 seeds):**
- P11-C03 (boundary-only fails @ N=1000)
- P11-C04 (core efficiency @ N=1000 mixed)
- P11-C06 (non-monotonic pattern across N)
- **Note:** These three claims are sub-hypotheses within E2 sample efficiency experiment; independent validation requires new E2 seeds in Project 12.

**Shared Phase E3 evidence (same 5 seeds):**
- P11-C05 (ratio + kNN optimal config)
- **Note:** Single claim from E3; validation requires independent E3 seeds.

---

## Data Quality Inventory

| Component | Source | Completeness | Status |
|---|---|---|---|
| Phase D (deterministic) | FIG_F1_NN_RESOLUTION.md | ✅ Full tables present | Ready |
| Phase E2 (stochastic, 3 seeds) | FIG_F2_SAMPLE_EFFICIENCY.md + artifact.json | ⚠️ Mean reported; std/CI only in artifact JSON (not in table) | Requires JSON inspection (Sprint 2) |
| Phase E3 (stochastic, 5 seeds) | FIG_F3_RATIO_KNN.md + artifact.json | ⚠️ Mean reported; std/CI only in artifact JSON (not in table) | Requires JSON inspection (Sprint 2) |
| Holdout definition | `project_11/results/phase_c3_sat_margin/holdout_points.json` | ✅ Specified | Locked (seed 223311) |
| Pool definition | Phase E3 protocol statement | ⚠️ Size stated (60000); composition TBD | Requires protocol reference |
| Baseline implementations | KEY_CLAIMS.md summary | ✅ Stated | To be verified in Sprint 2 baselines |

---

## Extraction Audit Notes (Sprint 1.6)

- **Zero invention:** All numbers copied directly from Project 11 tables/artifacts.
- **Type reassessment:** Based on Boss audit (C02, C05, C06, C08 downgraded to medium/weak to reflect secondary vs flagship claims).
- **Status correction:** All changed from "strong support" (incorrect; no Project 12 validation yet) to "untested (Project 12)".
- **Validation target separation:** Observed (historical) and pre-registered (Project 12) thresholds now distinct; reduces confirmation bias risk.
- **Leakage protocol:** Stated in Project 11 protocol; independent verification planned for Project 12.

---

## Sprint 2 Validation Checklist

Before re-validation begins:

- [ ] Verify Phase D artifact JSON contains seed/parameter metadata
- [ ] Verify Phase E2 artifact JSON contains explicit seed list [101, 202, 303] + std/CI values
- [ ] Verify Phase E3 artifact JSON contains explicit seed list [111, 222, 333, 444, 555] + std/CI values
- [ ] Load pool definition from protocol; document composition (stratified/random/other)
- [ ] Inspect holdout_points.json; confirm size=800, locked to seed 223311
- [ ] Baseline implementations verified against specifications (dense NN, V3.1, uniform, boundary, mixed, 1-NN, 3-NN)
- [ ] New E2 seeds committed (must differ from [101, 202, 303]; recommend [404, 505, 606])
- [ ] New E3 seeds committed (must differ from [111, 222, 333, 444, 555]; recommend [666, 777, 888, 999, 1010])

---

## References

- **Project 11 Packaging:** `project_11/packaging/out/`
- **Project 11 Results:** `project_11/results/`
- **Project 12 Claims:** `project_12/docs/FORMAL_CLAIMS.md`
- **Project 12 Protocols:** `project_12/docs/EVALUATION_SPEC.md`
