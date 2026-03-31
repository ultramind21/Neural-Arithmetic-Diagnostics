# PROJECT STRUCTURE — Navigation Guide
## Project 03 Abacus — Organized Directory Map

**Last Updated:** March 31, 2026

---

## Root Directory Overview

```
soroban_project/
├── src/                              # Core project code
├── final_audit/                      # Trust-recovery audit (Phases 1-6)
├── papers/                           # Research papers & closures
├── project_4/                        # Diagnostic framework project
├── tests/                            # Test files
├── checkpoints/                      # Model checkpoints
└── PROJECT_STRUCTURE.md              # This file
```

---

## 1. src/ — Core Project Code
**Purpose:** Model implementations and training scripts

### Key Files:
- `src/train/phase_26c_failure_audit.py` — Project 1 baseline
- `src/train/phase_27c_architecture_audit.py` — Project 2 architecture comparison
- `src/train/project_3_residual_logic_layer.py` — Project 3 baseline
- `src/train/project_3_killer_test_adversarial_carry_chain.py` — Project 3 killer test
- `src/train/phase_30_multidigit_learning.py` — Extended multidigit learning

---

## 2. final_audit/ — Trust-Recovery Audit Archive
**Purpose:** Complete audit documentation (Phases 1-6)

### Structure:

```
final_audit/
├── code_audit/                       # Verification scripts & raw outputs
│   ├── verify_*.py                   # Step-by-step verification scripts
│   ├── step*e_*_raw_output.txt       # Raw execution outputs
│   └── [diagnostic results files]
│
├── documentation/                    # Audit documentation
│   ├── phase_summaries/              # 4 Phase closure summaries
│   │   ├── PHASE_3_CLOSURE_SUMMARY.md
│   │   ├── PHASE_4_CLOSURE_SUMMARY.md
│   │   ├── PHASE_5_CLOSURE_SUMMARY.md
│   │   └── PHASE_6_CLOSURE_SUMMARY.md
│   │
│   └── executive_summaries/          # High-level audit reports
│       ├── EXECUTIVE_SUMMARY_FINAL.md
│       ├── MASTER_AUDIT_SUMMARY_PHASES_1_TO_6.md
│       └── QUICK_REFERENCE_FINAL.md
│
├── limitations/                      # Post-audit caveats
│   └── POST_AUDIT_LIMITATIONS_NOTE.md
│
└── integrity_checks/                 # Meta-verification scripts
    └── verify_audit_integrity_master_check.py
```

### How to Use:
1. **For audit overview:** Read `EXECUTIVE_SUMMARY_FINAL.md`
2. **For quick reference:** Read `QUICK_REFERENCE_FINAL.md`
3. **For master findings:** Read `MASTER_AUDIT_SUMMARY_PHASES_1_TO_6.md`
4. **For phase specifics:** Read `documentation/phase_summaries/PHASE_*.md`
5. **For known limitations:** Read `limitations/POST_AUDIT_LIMITATIONS_NOTE.md`

### Audit Status:
- ✅ **PASS** — Audit integrity verified
- All locked caveats documented
- Three permanent qualifications in place

---

## 3. papers/ — Research Papers & Closures
**Purpose:** Final research narratives and project closures

### Structure:

```
papers/
├── project_closures/                 # Project 1-3 closure documents
│   ├── killer_test_results.txt
│   ├── KILLER_TEST_VERDICT_FINAL.md
│   ├── PROJECT_1_CLOSURE_DOCUMENT_FINAL.md
│   ├── PROJECT_2_CLOSURE_DOCUMENT.md
│   ├── PROJECT_3_CLOSURE_MASTER_INDEX.md
│   ├── PROJECT_3_QUICK_REFERENCE_CARD.md
│   └── THE_FINAL_JUDGMENT.md
│
├── audit_reports/                    # Audit-related narratives
│   └── [audit interpretation documents]
│
└── final_narratives/                 # High-level research summaries
    └── [mission statements & overviews]
```

### How to Use:
1. **For Project 1-3 results:** Start with `project_closures/`
2. **For methodology explanations:** Read `THE_FINAL_JUDGMENT.md`
3. **For quick reference cards:** Read `PROJECT_*_QUICK_REFERENCE_CARD.md`

### Paper Status:
- ✅ All files audit-aligned
- ✅ All qualifications locked and visible
- ✅ Ready for research publication

---

## 4. project_4/ — Diagnostic Framework Project
**Purpose:** Post-audit diagnostic framework for arithmetic reasoning

### Structure:

```
project_4/
├── framework/                        # Core framework definitions
│   ├── PROJECT_4_DIAGNOSTIC_FRAMEWORK.md  # Main specification
│   └── FRAMEWORK_CHANGELOG.md              # Version history
│
├── diagnostics/                      # Diagnostic measurement tools
│   ├── diagnostic_scorecard.py              # Core 5-dimension metrics
│   ├── benchmark_adversarial_patterns.py    # Pattern generation
│   └── regime_classification.py             # Regime detector
│
├── baselines/                        # Baseline model evaluation
│   ├── project_4_baseline_comparison.py
│   └── PROJECT_4_BASELINE_RESULTS.md
│
├── interventions/                    # Experimental interventions
│   ├── adversarial_training/
│   │   ├── project_4_adversarial_training.py
│   │   └── PROJECT_4_ADVERSARIAL_TRAINING_RESULTS.md
│   │
│   └── blockwise_decomposition/
│       ├── project_4_blockwise_decomposition.py
│       └── PROJECT_4_BLOCKWISE_RESULTS.md
│
└── results/                          # Final synthesis
    └── PROJECT_4_RESULTS_SUMMARY.md
```

### How to Use:
1. **Understand the mission:** Read `framework/PROJECT_4_DIAGNOSTIC_FRAMEWORK.md`
2. **Track changes:** Check `framework/FRAMEWORK_CHANGELOG.md`
3. **Run diagnostics:** Use scripts in `diagnostics/`
4. **View experiment results:** Check `baselines/` and `interventions/`

### Project 4 Status:
- ⏳ **IN PROGRESS** — Framework locked, implementation ongoing
- Baseline re-evaluation: PENDING
- MVP intervention: PENDING
- Extended scope: OPTIONAL

---

## 5. Key Files Across the Project

### Critical Audit Files:
| File | Location | Purpose |
|------|----------|---------|
| `MASTER_AUDIT_SUMMARY_PHASES_1_TO_6.md` | `final_audit/documentation/executive_summaries/` | Complete audit verdict |
| `EXECUTIVE_SUMMARY_FINAL.md` | `final_audit/documentation/executive_summaries/` | High-level audit overview |
| `verify_audit_integrity_master_check.py` | `final_audit/integrity_checks/` | Meta-consistency check |

### Critical Project 4 Files:
| File | Location | Purpose |
|------|----------|---------|
| `PROJECT_4_DIAGNOSTIC_FRAMEWORK.md` | `project_4/framework/` | Framework specification |
| `diagnostic_scorecard.py` | `project_4/diagnostics/` | Measurement tools |
| `FRAMEWORK_CHANGELOG.md` | `project_4/framework/` | Version tracking |

### Critical Paper Files:
| File | Location | Purpose |
|------|----------|---------|
| `THE_FINAL_JUDGMENT.md` | `papers/project_closures/` | Final research narrative |
| `PROJECT_3_CLOSURE_MASTER_INDEX.md` | `papers/project_closures/` | Project 3 reference index |

---

## Navigation Quick Links

### If You Want To...

**...understand the audit:**
→ Read: `final_audit/documentation/executive_summaries/EXECUTIVE_SUMMARY_FINAL.md`

**...understand Project 4:**
→ Read: `project_4/framework/PROJECT_4_DIAGNOSTIC_FRAMEWORK.md`

**...understand what happened to Projects 1-3:**
→ Read: `papers/project_closures/THE_FINAL_JUDGMENT.md`

**...verify audit integrity:**
→ Run: `python final_audit/integrity_checks/verify_audit_integrity_master_check.py`

**...check all locked caveats:**
→ Read: `final_audit/documentation/executive_summaries/QUICK_REFERENCE_FINAL.md`

**...see known limitations:**
→ Read: `final_audit/limitations/POST_AUDIT_LIMITATIONS_NOTE.md`

---

## Organization Principles

This structure follows these principles:

1. **Separation of concerns:** Audit archive separate from ongoing Project 4
2. **Logical grouping:** Related files stay together
3. **Clear metadata:** Each folder has a clear purpose
4. **Scalability:** Easy to add new interventions or baselines
5. **Navigation:** README files and clear naming conventions

---

## Last Updated
- **Date:** March 31, 2026
- **Status:** Complete reorganization
- **Next:** Project 4 implementation begins
