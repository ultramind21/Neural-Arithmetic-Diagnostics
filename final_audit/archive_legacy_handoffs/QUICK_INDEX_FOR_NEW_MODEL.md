# QUICK INDEX FOR NEW MODEL SESSION
## Fast Reference to All Important Files & Status

---

## CURRENT STATE (March 30, 2026)

**Overall Status:** Phase 3 / Step 3B in progress  
**Last Action:** Created Phase 3B diagnostic (needs completion)  
**Decision Point:** DO NOT proceed to Phase 3C until 3B diagnostic completes

---

## PHASE STATUS

| Phase | Project | Target File | Status | Pass/Fail |
|-------|---------|-------------|--------|-----------|
| Phase 1 | Killer Test | Project_3/killer_test.py | Complete | ✓ PASS |
| Phase 2 | Project 1 | src/train/phase_26c_failure_audit.py | Complete | ✓ PASS WITH QUALIFICATIONS |
| **Phase 3** | **Project 2** | **src/train/phase_27c_architecture_audit.py** | **IN PROGRESS** | **3A ✓, 3B ⏳** |
| Phase 4+ | Projects 3,4 | src/train/phase_*.py | NOT STARTED | — |

---

## KEY RESULTS TO REMEMBER

### Phase 1 Finding (Killer Test)
```
Alternating Pattern Collapse (REAL):
- Digit Accuracy: 50.00%
- Carry Accuracy: 100.00%
- Exact Match: 50.00%
```

### Phase 2 Finding (Project 1 Baseline)
```
Overall success rate: 61.4% (1800 examples over 30 trials)
- Carry cases: 43.3% failure rate (904 examples)
- Non-carry: 33.9% failure rate (896 examples)
- Ratio: Carry 1.27× harder
```

### Phase 3 Critical Issue (Project 2 - TO VERIFY)
```
Question: Does random.shuffle(all_pairs) cause bias across architectures?
- all_pairs is shuffled in-place during MLP trials
- LSTM starts fresh but all_pairs may already be shuffled
- Are SAME test pairs used fairly across MLP/LSTM/Transformer?
```

---

## MOST IMPORTANT DECISION

**STOP HERE UNTIL PHASE 3B DIAGNOSTIC IS COMPLETE**

The Phase 3B shuffle-order issue must be resolved before ANY other work.

---

## ARTIFACTS TO SEND TO NEW MODEL

Send these files to the new model:

1. **HANDOFF_COMPLETE_CONTEXT_TO_NEW_MODEL.md** ← Main comprehensive handoff
2. **PHASE_1_KILLER_TEST_FOUNDATION_SUMMARY.md** ← Phase 1 documented
3. **PHASE_2_PROJECT_1_BASELINE_SUMMARY.md** ← Phase 2 documented
4. **verify_phase27c_step3a_source_setup.py** ← Already completed
5. **verify_phase27c_step3b_data_split.py** ← Already completed (shows the issue)
6. **phase_27c_architecture_audit.py** ← The target file itself

---

## NEXT IMMEDIATE TASKS (For New Model)

**Task 1 - URGENT:** Complete Phase 3B diagnostic
```python
# Create: verify_phase27c_step3b_diagnostic_shuffle.py
# Purpose: Track all_pairs state across architectures
# Output: Clear evidence that shuffle is fair OR identify bias
```

**Task 2:** If 3B passes → proceed to 3C  
**Task 3:** If 3C passes → proceed to 3D  
**Task 4:** If 3D passes → proceed to 3E and run full reproduction  

---

## METHODOLOGY RULES (CRITICAL)

1. ✓ VERIFY then Progress (don't assume)
2. ✓ DOCUMENT Qualifications (what was/wasn't checked)
3. ✓ NO Overstatement (state exactly what's known)
4. ✓ EXPLICIT Assumptions (list dependencies)
5. ✓ SEQUENTIAL within phase (parallel across phases OK)

---

## KEY CONTACTS

The original user expects:
- Clear status updates after each step
- Explicit pass/fail with qualifications
- No automatic progression
- Documentation before moving forward

---

## WHAT SUCCESS LOOKS LIKE

After Phase 3B diagnostic completes:

**If PASS:**
```
✓ All architectures use same test pairs per trial
✓ Shuffle order is deterministic and fair
✓ Proceed to Phase 3C
```

**If FAIL:**
```
✗ Shuffle order introduces bias
✗ Architectures not directly comparable
✗ Flag as comparability issue in final report
```

---

## END OF QUICK INDEX

