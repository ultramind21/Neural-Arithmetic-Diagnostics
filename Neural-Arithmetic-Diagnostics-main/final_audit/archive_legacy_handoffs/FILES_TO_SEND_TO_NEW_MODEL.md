# FILES TO SEND TO NEW MODEL
## Complete File List with Locations & Descriptions

---

## READ THESE FIRST (In Order)

### 1. MESSAGE_TO_NEW_MODEL.md
**Location:** `/final_audit/MESSAGE_TO_NEW_MODEL.md`  
**Read First:** YES - This explains your immediate task  
**Purpose:** Direct instructions for Phase 3B diagnostic

---

### 2. QUICK_INDEX_FOR_NEW_MODEL.md
**Location:** `/final_audit/QUICK_INDEX_FOR_NEW_MODEL.md`  
**Read First:** YES - Quick reference to status and what's important  
**Purpose:** Fast lookup table for current project status

---

### 3. HANDOFF_COMPLETE_CONTEXT_TO_NEW_MODEL.md
**Location:** `/final_audit/HANDOFF_COMPLETE_CONTEXT_TO_NEW_MODEL.md`  
**Read First:** YES - Comprehensive background and methodology  
**Purpose:** Full context, how we got here, what was done before

---

## THEN READ THESE (For Deep Understanding)

### 4. PHASE_1_KILLER_TEST_FOUNDATION_SUMMARY.md
**Location:** `/final_audit/PHASE_1_KILLER_TEST_FOUNDATION_SUMMARY.md`  
**Read First:** Optional (but highly recommended)  
**Purpose:** Phase 1 is complete, understand the foundation  
**Key Takeaway:** Killer test is reproducible and real

---

### 5. PHASE_2_PROJECT_1_BASELINE_SUMMARY.md
**Location:** `/final_audit/PHASE_2_PROJECT_1_BASELINE_SUMMARY.md`  
**Read First:** YES - This is your baseline reference  
**Purpose:** Phase 2 baseline (61.4% success rate) is provisionally trustworthy  
**Key Takeaway:** Project 1 baseline is PASS WITH QUALIFICATIONS

---

## THEN USE THESE (For Execution)

### 6. phase_27c_architecture_audit.py
**Location:** `/src/train/phase_27c_architecture_audit.py`  
**Read First:** YES - The target file you're analyzing  
**Purpose:** The official script you need to verify  
**What to Look For:** The shuffle logic in main loop (lines 200+)

---

### 7. verify_phase27c_step3a_source_setup.py
**Location:** `/final_audit/code_audit/verify_phase27c_step3a_source_setup.py`  
**Run This:** No (already completed)  
**Purpose:** Understand Phase 3A pattern for building 3B diagnostic  
**Reference:** Use this as a template for your diagnostic script

---

### 8. verify_phase27c_step3b_data_split.py
**Location:** `/final_audit/code_audit/verify_phase27c_step3b_data_split.py`  
**Run This:** No (already completed, shows the problem)  
**Purpose:** This identified the shuffle-order issue  
**Reference:** Shows what questions need answering

---

### 9. verify_phase26c_step2e_reproduction.py
**Location:** `/final_audit/code_audit/verify_phase26c_step2e_reproduction.py`  
**Run This:** No (Phase 2 reference only)  
**Purpose:** Understand how reproduction verification works  
**Reference:** Pattern to follow for Phase 3E later

---

## OUTPUT FILES (Reference Only)

### 10. step2e_phase26c_raw_output.txt
**Location:** `/final_audit/code_audit/step2e_phase26c_raw_output.txt`  
**Contains:** Raw output from Phase 2E (61.4% result)  
**Purpose:** Reference data showing baseline result

---

## YOUR JOB: CREATE THESE

### 11. verify_phase27c_step3b_diagnostic_shuffle.py
**Location:** `final_audit/code_audit/verify_phase27c_step3b_diagnostic_shuffle.py`  
**Status:** TO BE CREATED BY YOU  
**Purpose:** Answer the shuffle-order fairness question  
**Output:** Clear pass/fail/ambiguous on architecture comparability

---

## DIRECTORY STRUCTURE

```
soroban_project/
├── src/
│   └── train/
│       ├── phase_26c_failure_audit.py        [Phase 2 target]
│       └── phase_27c_architecture_audit.py   [Phase 3 target - FOCUS HERE]
│
├── final_audit/
│   ├── HANDOFF_COMPLETE_CONTEXT_TO_NEW_MODEL.md
│   ├── QUICK_INDEX_FOR_NEW_MODEL.md
│   ├── MESSAGE_TO_NEW_MODEL.md
│   ├── PHASE_1_KILLER_TEST_FOUNDATION_SUMMARY.md
│   ├── PHASE_2_PROJECT_1_BASELINE_SUMMARY.md
│   └── code_audit/
│       ├── verify_phase27c_step3a_source_setup.py
│       ├── verify_phase27c_step3b_data_split.py
│       ├── verify_phase27c_step3b_diagnostic_shuffle.py    [YOU CREATE THIS]
│       ├── verify_phase26c_step2e_reproduction.py
│       ├── step2e_phase26c_raw_output.txt
│       └── [... other Phase 1 & 2 scripts ...]
```

---

## HOW TO USE THIS FILE LIST

### If you're the NEW MODEL:

1. Read files 1-3 first (messages and context)
2. Skim files 4-5 (background phases)
3. Study file 6 carefully (your target)
4. Use files 7-8 as references (understand the problem)
5. Create and run file 11 (your task)
6. Skip file 12 (already done)

### If you need to send these to the user:

Package these files:
- Files 1-5: Markdown context docs
- File 6: The target script (phase_27c_architecture_audit.py)
- Files 7-8: Reference scripts
- File 10: Reference output

---

## TOTAL FILE COUNT

**To Send to New Model:** 9 files  
**To Create:** 1 file (diagnostic)  
**Already Done:** 6 files (from Phases 1-2)

---

# SEND THIS CHECKLIST TOO

When handoff completes, new model should have:

- [ ] MESSAGE_TO_NEW_MODEL.md
- [ ] QUICK_INDEX_FOR_NEW_MODEL.md
- [ ] HANDOFF_COMPLETE_CONTEXT_TO_NEW_MODEL.md
- [ ] PHASE_1_KILLER_TEST_FOUNDATION_SUMMARY.md
- [ ] PHASE_2_PROJECT_1_BASELINE_SUMMARY.md
- [ ] phase_27c_architecture_audit.py (from src/train/)
- [ ] verify_phase27c_step3a_source_setup.py
- [ ] verify_phase27c_step3b_data_split.py
- [ ] verify_phase26c_step2e_reproduction.py (reference)
- [ ] step2e_phase26c_raw_output.txt (reference)

---

# END OF FILE LIST

