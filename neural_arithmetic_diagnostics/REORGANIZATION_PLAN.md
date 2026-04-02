================================================================================
PROJECT REORGANIZATION PLAN
Final Archive & Cleanup Structure
================================================================================

## PURPOSE
This document specifies the intended final organization structure for the soroban_project directory. It provides:
- Target files to retain (verified and clean final set)
- Recommended files to archive (historical, exploratory)
- Desired directory structure for organized project
- Implementation guidance

**Important note:** At present, some closure and summary documents still exist under `Papers/` or under legacy names. This plan describes the desired final organization, not necessarily the current exact file layout. Verification of file existence and location is needed before final implementation.

================================================================================
TARGET: TOP-LEVEL DOCUMENTATION (PROJECT ROOT)
================================================================================

The intended final set should consolidate the following core documentation at root level. Some of these files currently exist under `Papers/` or with alternative names and must be verified and relocated.

1. **PROJECT_CHARTER.md**
   - Initial project scope and goals
   - Keep in root as reference
   - Status: Verify final version exists

2. **MASTER_RESEARCH_SUMMARY.md**
   - Comprehensive summary of Projects 1, 2, 3
   - Intended as single source of reference for all findings
   - Status: Verify in root, or consolidate if currently elsewhere

3. **PROJECT_1_CLOSURE_DOCUMENT.md**
   - Official closure of Project 1
   - Findings and conclusions
   - Status: Verify existence and correct name (currently may be PROJECT_1_CLOSURE_DOCUMENT_FINAL.md in Papers/)

4. **PROJECT_2_CLOSURE_DOCUMENT.md**
   - Official closure of Project 2
   - Findings and conclusions
   - Status: Verify location in root or relocate from Papers/

5. **PROJECT_3_CLOSURE_DOCUMENT.md**
   - Official closure of Project 3
   - Alternating pattern test results and methodology
   - Status: Retain as core reference document once finalized

6. **FINAL_INTERPRETATION_MAP.md**
   - Map of how Projects 1, 2, 3 fit together
   - Narrative arc of research
   - Status: Verify existence and consolidate to root if needed

================================================================================
KEEP: SOURCE CODE (FINAL ARTIFACTS ONLY)
================================================================================

**src/models/**
```
residual_logic_adder.py          ✅ Final model architecture
```

**src/train/** (FINAL REFERENCE EXPERIMENTS)
```
phase_26c_failure_audit.py       ✅ Project 1 benchmark
phase_27c_architecture_audit.py   ✅ Project 2 benchmark
phase_30_multidigit_learning.py   ✅ Project 3 baseline
phase_30b_stress_test.py          ✅ Project 3 extended training
project_3_residual_logic_layer.py ✅ Project 3 architecture
project_3_killer_test_adversarial_carry_chain.py ✅ Adversarial test
```

These 6 files represent the clean research artifacts. They are executable,
documented, and serve as evidence for the research findings.

================================================================================
WHAT TO ARCHIVE
================================================================================

The following should be moved to archive/ as superseded or intermediate work:

**Exploratory Phases (archive/exploratory_phases/):**
- phase_10 through phase_25: hypothesis testing and initial explorations
- Reason: superseded by final benchmarks; kept for transparency on research evolution

**Failed Variants (archive/failed_variants/):**
- project_3_v4c_*: digit leakage in loss function
- project_3_v4d_*: pure regression without additional structure
- project_3_v3*: capacity investigation variants
- Reason: methodology issues or incomplete approaches; should not be used for results

**Diagnostic Scripts (archive/diagnostic_scripts/):**
- Intermediate diagnostic tests and early iteration scripts
- Reason: superseded by killer_test or no longer needed for final analysis

**Large Result Files (archive/big_data/):**
- *.pkl result files from experiments
- Old or obsolete checkpoint files
- Reason: archived for reproducibility and record-keeping, removed from working directories

================================================================================
FINAL DIRECTORY STRUCTURE
================================================================================

```
soroban_project/
│
├─ [ROOT DOCUMENTATION] ──────────────────────
│  ├── PROJECT_CHARTER.md
│  ├── MASTER_RESEARCH_SUMMARY.md
│  ├── PROJECT_1_CLOSURE_DOCUMENT.md
│  ├── PROJECT_2_CLOSURE_DOCUMENT.md
│  ├── PROJECT_3_CLOSURE_DOCUMENT.md ✅
│  ├── FINAL_INTERPRETATION_MAP.md
│  ├── README.md (optional: overview + links)
│  └── REORGANIZATION_PLAN.md (this file)
│
├─ [SOURCE CODE] ─────────────────────────────
│  └── src/
│      ├── models/
│      │   └── residual_logic_adder.py
│      │
│      └── train/
│          ├── phase_26c_failure_audit.py
│          ├── phase_27c_architecture_audit.py
│          ├── phase_30_multidigit_learning.py
│          ├── phase_30b_stress_test.py
│          ├── project_3_residual_logic_layer.py
│          └── project_3_killer_test_adversarial_carry_chain.py
│
├─ [CHECKPOINTS] ─────────────────────────────
│  └── checkpoints/
│      └── (keep only final models if space-constrained)
│
├─ [PAPERS & ANALYSIS] ───────────────────────
│  └── Papers/
│      ├── PROJECT_3_QUICK_REFERENCE_CARD.md
│      ├── PROJECT_3_CLOSURE_MASTER_INDEX.md
│      ├── THE_FINAL_JUDGMENT.md
│      ├── KILLER_TEST_VERDICT_FINAL.md
│      ├── MECHANISM_VERIFIED.md
│      ├── TRUTH_SUMMARY_1MIN.md
│      ├── THE_COMPLETE_TRUTH.md
│      └── killer_test_results.txt
│
└─ [ARCHIVE] ─────────────────────────────────
   └── archive/
       ├── exploratory_phases/
       │   ├── phase_10_*/
       │   ├── phase_13_*/
       │   └── ... (all exploratory phases)
       │
       ├── failed_variants/
       │   ├── project_3_v4c_*/
       │   ├── project_3_v4d_*/
       │   └── ... (all dead ends)
       │
       ├── diagnostic_scripts/
       │   ├── project_3_v2_extended_100.py
       │   ├── project_3_diagnostic_kill_tests.py
       │   └── ... (intermediate diagnostics)
       │
       ├── big_data/
       │   ├── final_results_*.pkl
       │   └── checkpoints/phase_*
       │
       └── README.md (explains what's archived and why)
```

================================================================================
MIGRATION STEPS
================================================================================

### Step 1: Verify Clean Set Exists
```
Verify these files exist and are complete:
- PROJECT_3_CLOSURE_DOCUMENT.md ✅ (just created)
- MASTER_RESEARCH_SUMMARY.md (check Project 3 section updated)
- PROJECT_1_CLOSURE_DOCUMENT.md
- PROJECT_2_CLOSURE_DOCUMENT.md
- FINAL_INTERPRETATION_MAP.md
- PROJECT_CHARTER.md
```

### Step 2: Create Archive Structure
```
mkdir -p archive/exploratory_phases
mkdir -p archive/failed_variants
mkdir -p archive/diagnostic_scripts
mkdir -p archive/big_data
touch archive/README.md
```

Create archive/README.md explaining the contents and rationale for archival.

### Step 3: Move Exploratory Phases
```
Move phase_10_* through phase_25_* to archive/exploratory_phases/
Reason: These are hypothesis testing, superseded by final benchmarks
```

### Step 4: Move Failed Variants
```
Move project_3_v4c_* through project_3_v3* to archive/failed_variants/
Reason: These have methodology issues and should never run again
```

### Step 5: Move Diagnostic Scripts
```
Move project_3_v2_extended_100.py to archive/diagnostic_scripts/
Move project_3_diagnostic_kill_tests.py to archive/diagnostic_scripts/
Move project_3_intervention_test.py to archive/diagnostic_scripts/
Reason: Superseded by killer_test or no longer needed
```

### Step 6: Move Big Data
```
Move *.pkl files to archive/big_data/
Move obsolete checkpoints to archive/big_data/
Reason: Keep for reproducibility but out of working directory
```

### Step 7: Clean & Verify
```
Final src/train/ should contain ONLY:
  - phase_26c_failure_audit.py
  - phase_27c_architecture_audit.py
  - phase_30_multidigit_learning.py
  - phase_30b_stress_test.py
  - project_3_residual_logic_layer.py
  - project_3_killer_test_adversarial_carry_chain.py

Final src/models/ should contain ONLY:
  - residual_logic_adder.py
```

================================================================================
MINIMUM CLEAN SET (IF SPACE IS CRITICAL)
================================================================================

If you need absolute minimum for publication:

**Keep:**
```
PROJECT_CHARTER.md
MASTER_RESEARCH_SUMMARY.md
PROJECT_1_CLOSURE_DOCUMENT.md
PROJECT_2_CLOSURE_DOCUMENT.md
PROJECT_3_CLOSURE_DOCUMENT.md
FINAL_INTERPRETATION_MAP.md

src/models/residual_logic_adder.py
src/train/project_3_killer_test_adversarial_carry_chain.py

Papers/PROJECT_3_QUICK_REFERENCE_CARD.md
Papers/KILLER_TEST_VERDICT_FINAL.md
```

**Can delete with minimal loss:**
```
All phase_10 through phase_25 experiments (available in archive if needed)
All V4C and V4D variants (failed approaches)
All intermediate diagnostic scripts
checkpoints/ folder (can regenerate from code)
Papers/ other files (redundant with closure documents)
```

Result: ~50 MB clean set vs 1+ GB full archive

================================================================================
RULES FOR FUTURE MODIFICATIONS
================================================================================

**RULE 1: Separate exploratory and final code**
- All new experiments should be isolated from src/train/ (e.g., in experiments/ folder)
- Only final, tested, approved code in src/train/
- Exploratory or intermediate work should be archived immediately after project closure

**RULE 2: Single closure document per project**
- PROJECT_1_CLOSURE_DOCUMENT.md (retain as the official closure for Project 1)
- PROJECT_2_CLOSURE_DOCUMENT.md (retain as the official closure for Project 2)
- PROJECT_3_CLOSURE_DOCUMENT.md (retain as the official closure for Project 3)
- Do not allow variant names or duplicates to accumulate

**RULE 3: Papers/ folder for supporting analysis only**
- Papers/ contains analysis, quick references, and detailed breakdowns
- MASTER_RESEARCH_SUMMARY.md remains the single source of truth
- Never create contradictory summaries or alternate versions of findings

**RULE 4: Regular archival of completed experiments**
- Monthly or after project closure, move completed experiments to archive/
- Do not let intermediate work accumulate in src/
- archive/README.md should explain why each phase or variant was archived

**RULE 5: Killer test code as reference pattern**
- project_3_killer_test_adversarial_carry_chain.py is the pattern for adversarial testing
- Future diagnostic work should follow this pattern, not create new variants
- Preserve this file as methodological reference

================================================================================
TARGET VERIFICATION CHECKLIST
================================================================================

Before considering the reorganization complete:

✅ PROJECT_3_CLOSURE_DOCUMENT.md finalized and placed in root
✅ MASTER_RESEARCH_SUMMARY.md verified to be in root with Project 3 section
✅ Papers/KILLER_TEST_VERDICT_FINAL.md complete and properly linked
✅ Papers/PROJECT_3_QUICK_REFERENCE_CARD.md complete
✅ src/train/ verified to contain exactly 6 final reference scripts
✅ src/models/ verified to contain only residual_logic_adder.py
✅ All PROJECT_*_CLOSURE_DOCUMENT.md files verified (names and locations)
✅ archive/ directory created and fully organized
✅ archive/README.md created explaining archived contents
✅ No conflicting document names (consolidated to single versions)
✅ All retained code files commented and documented
✅ Killer test code preserved and referenced as key artifact

================================================================================
STATUS & COMPLETION
================================================================================

**Document Version:** 1.0
**Date:** March 29, 2026
**Status:** Target plan for implementation
**Effort:** 2-3 hours for complete reorganization
**Outcome:** Clean, organized, and internally consistent archived project structure

================================================================================
