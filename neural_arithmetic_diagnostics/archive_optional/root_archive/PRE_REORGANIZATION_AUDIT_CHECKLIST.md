================================================================================
PRE-REORGANIZATION AUDIT CHECKLIST
Repository State Verification Before Cleanup
================================================================================

Run this checklist BEFORE moving/deleting any files.
Purpose: Ensure you understand the current state before reorganization, and that no important files will be lost.

Important note:
This checklist reflects the intended final organization and naming conventions. Before using it, update any filename or path assumptions so that they match the actual current repository state.

================================================================================
CHECKLIST ITEMS
================================================================================

## ✓ ITEM 1: Verify Official Closure Documents and Their Current Locations

**Action:** Check which closure and summary documents currently exist, under what names, and in which directories. Confirm which versions are intended to remain as the final official set once reorganization is complete.

Verify the status of:
- [ ] PROJECT_CHARTER.md (or equivalent)
- [ ] Project 1 closure document (confirm exact final filename and location)
- [ ] Project 2 closure document (confirm exact final filename and location)
- [ ] PROJECT_3_CLOSURE_DOCUMENT.md
- [ ] MASTER_RESEARCH_SUMMARY.md (or current equivalent)
- [ ] FINAL_INTERPRETATION_MAP.md (if part of final approved set)

**Duplicate Check:**
- [ ] No superseded duplicate such as PROJECT_2_CLOSURE_FINAL.md remains in the active final set (if present, mark for archive or deletion after verification)
- [ ] No conflicting *_FINAL.md vs *_DOCUMENT.md naming creates ambiguity
- [ ] Verify any duplicate MASTER_RESEARCH_SUMMARY.md in Papers/ vs root (mark extras for consolidation)

Command to check for duplicates:
```powershell
Get-ChildItem -Path "d:\Music\Project 03 Abacus\soroban_project" -File -Name | 
  Where-Object { $_ -match "CLOSURE" -or $_ -match "MASTER_RESEARCH" }
```

Expected output:
```
PROJECT_1_CLOSURE_DOCUMENT.md
PROJECT_2_CLOSURE_DOCUMENT.md
PROJECT_3_CLOSURE_DOCUMENT.md
MASTER_RESEARCH_SUMMARY.md
```

NO other variants.

---

## ✓ ITEM 2: Verify The Final Reference Code Files Exist

**Action:** Verify these exist in their locations:

**src/models/:**
- [ ] residual_logic_adder.py (final architecture)

**src/train/ (Phase Reference Benchmarks):**
- [ ] phase_26c_failure_audit.py
- [ ] phase_27c_architecture_audit.py
- [ ] phase_30_multidigit_learning.py
- [ ] phase_30b_stress_test.py

**src/train/ (Project 3 Finals):**
- [ ] project_3_residual_logic_layer.py
- [ ] project_3_killer_test_adversarial_carry_chain.py ⚡ CRITICAL

Command:
```powershell
@(
  "src/models/residual_logic_adder.py",
  "src/train/phase_26c_failure_audit.py",
  "src/train/phase_27c_architecture_audit.py",
  "src/train/phase_30_multidigit_learning.py",
  "src/train/phase_30b_stress_test.py",
  "src/train/project_3_residual_logic_layer.py",
  "src/train/project_3_killer_test_adversarial_carry_chain.py"
) | ForEach-Object {
  $path = "d:\Music\Project 03 Abacus\soroban_project\$_"
  if (Test-Path $path) { Write-Host "✓ $_" } else { Write-Host "✗ MISSING: $_" }
}
```

Expected: All 7 files show ✓

---

## ✓ ITEM 3: Count Exploratory Phases That Need Archiving

**Action:** List all phase_* files in src/train/ that are NOT in the final 7

Command:
```powershell
Get-ChildItem -Path "d:\Music\Project 03 Abacus\soroban_project\src\train" -Filter "phase_*.py" | 
  Select-Object Name | 
  Sort-Object Name
```

**Expected result:** Should see phases 10-25 and any others besides:
- phase_26c_failure_audit.py ✓ (KEEP)
- phase_27c_architecture_audit.py ✓ (KEEP)
- phase_30_multidigit_learning.py ✓ (KEEP)
- phase_30b_stress_test.py ✓ (KEEP)

All others → ARCHIVE

**Record count:**
- [ ] Count = ___ phases to archive (document this)
  Expected: exploratory phases from earlier development stages

---

## ✓ ITEM 4: Identify Failed Variants (V4C, V4D, V3 series)

**Action:** List all project_3_v*.py files that FAILED or are SUPERSEDED

Command:
```powershell
Get-ChildItem -Path "d:\Music\Project 03 Abacus\soroban_project\src\train" -Filter "project_3_v*.py" | 
  Select-Object Name | 
  Sort-Object Name
```

**Mark each:**
- [ ] project_3_v4c_* → ARCHIVE (digit leakage)
- [ ] project_3_v4d_* → ARCHIVE (same as extended V2, redundant)
- [ ] project_3_v3* → ARCHIVE (capacity experiments, superseded)
- [ ] project_3_v2_extended_100.py → ARCHIVE (diagnostic, not final)
- [ ] project_3_teacher_forcing_test.py → ARCHIVE (failed)
- [ ] project_3_huber_loss_test.py → ARCHIVE (failed)

**Record count:**
- [ ] Count = ___ failed variants to archive
  Expected: archived variants with methodology issues or limited value

---

## ✓ ITEM 5: Verify Killer Test Code Is Pristine

**Action:** Check killer test file is clean and runnable

File: `src/train/project_3_killer_test_adversarial_carry_chain.py`

- [ ] File exists ✓
- [ ] File has docstring explaining purpose
- [ ] File has comments explaining each test
- [ ] File imports are satisfied (no missing dependencies)
- [ ] File runs without errors (test on one pattern)
- [ ] Output format matches Papers/killer_test_results.txt

Quick test:
```powershell
cd "d:\Music\Project 03 Abacus\soroban_project"
python -c "import src.train.project_3_killer_test_adversarial_carry_chain; print('✓ Imports work')"
```

---

## ✓ ITEM 6: Verify MASTER_RESEARCH_SUMMARY.md Is Consistent

**Action:** Check there's only ONE authoritative version

Command:
```powershell
Get-ChildItem -Path "d:\Music\Project 03 Abacus\soroban_project" -Recurse -Filter "MASTER_RESEARCH_SUMMARY.md"
```

**Expected:** Exactly one final authoritative version should remain in the project after cleanup. If multiple versions exist, mark the extras for archive or consolidation after confirming the intended primary source.

---

## ✓ ITEM 7: Check Papers/ Folder Is Supporting Only (Not Primary)

**Action:** Verify Papers/ files reference root documents

Files in Papers/ should include:
- [ ] PROJECT_3_QUICK_REFERENCE_CARD.md ✓
- [ ] PROJECT_3_CLOSURE_MASTER_INDEX.md ✓
- [ ] KILLER_TEST_VERDICT_FINAL.md ✓
- [ ] THE_FINAL_JUDGMENT.md ✓
- [ ] MECHANISM_VERIFIED.md ✓
- [ ] TRUTH_SUMMARY_1MIN.md ✓
- [ ] killer_test_results.txt ✓
- [ ] THE_COMPLETE_TRUTH.md ✓

**Rule check:**
- [ ] Supporting files in Papers/ should not replace the final official closure and summary documents once those are confirmed
- [ ] Papers/ should contain explanatory analysis and quick references, not alternative versions of official findings

---

## ✓ ITEM 8: Verify Archive/ Folder Exists & Is Empty

**Action:** Prepare archive structure

Command:
```powershell
Test-Path "d:\Music\Project 03 Abacus\soroban_project\archive"
```

If NOT exists:
- [ ] Create it now with proper structure:
```powershell
New-Item -ItemType Directory -Force -Path "d:\Music\Project 03 Abacus\soroban_project\archive"
New-Item -ItemType Directory -Force -Path "d:\Music\Project 03 Abacus\soroban_project\archive\exploratory_phases"
New-Item -ItemType Directory -Force -Path "d:\Music\Project 03 Abacus\soroban_project\archive\failed_variants"
New-Item -ItemType Directory -Force -Path "d:\Music\Project 03 Abacus\soroban_project\archive\diagnostic_scripts"
New-Item -ItemType Directory -Force -Path "d:\Music\Project 03 Abacus\soroban_project\archive\big_data"
```

If exists:
- [ ] Verify it's for actual moving (not randomly stuff)
- [ ] If old/garbage in there, clean it first

---

## ✓ ITEM 9: Document File Move Plan

**Action:** Create a manifest of exactly what gets moved where

Create file: `REORGANIZATION_MANIFEST.txt`

Format:
```
EXPLORATORY PHASES → archive/exploratory_phases/
- phase_10_*
- phase_13_*
- ... (list each)
(Total: ___ files)

FAILED VARIANTS → archive/failed_variants/
- project_3_v4c_*
- project_3_v4d_*
- ... (list each)
(Total: ___ files)

DIAGNOSTIC SCRIPTS → archive/diagnostic_scripts/
- project_3_v2_extended_100.py
- ... (list each)
(Total: ___ files)

BIG DATA → archive/big_data/
- *.pkl files
- old checkpoints
(Total: ___ files)
```

- [ ] Manifest created ✓
- [ ] Each file marked for specific destination
- [ ] Total file count recorded

---

## ✓ ITEM 10: Final Sanity Check - Can You Reproduce The Key Result?

**Action:** Quick test that killer test still works

Command:
```powershell
cd "d:\Music\Project 03 Abacus\soroban_project"
python src/train/project_3_killer_test_adversarial_carry_chain.py 2>&1 | grep -E "(Alternating|50\.00|VERDICT)"
```

Expected output includes:
```
Alternating 9,0,9,0... : 50.00%
Failure detected
```

- [ ] Killer test runs ✓
- [ ] Produces 50% on alternating ✓
- [ ] Reproduces the expected adversarial failure pattern ✓

If FAILS:
- [ ] DO NOT proceed with reorganization
- [ ] Investigate why killer test broken
- [ ] Fix before archiving

---

================================================================================
SCORING & DECISION POINT
================================================================================

**Count checkmarks:**
- Total possible: 50+ individual checkmarks
- Proceed if: 95%+ complete
- Fix issues before proceeding: < 95%

**If any ITEM shows FAILED:**
1. Note which item(s) failed
2. Fix that specific issue
3. Re-check that item
4. If file naming or location mismatches remain unresolved, do not proceed until the final authoritative names are confirmed
5. Then proceed

**If all ITEMS pass:**
→ You're ready to proceed with reorganization
→ Use REORGANIZATION_PLAN.md as execution guide

================================================================================
COMMAND TO RUN THIS ENTIRE CHECKLIST AT ONCE
================================================================================

```powershell
cd "d:\Music\Project 03 Abacus\soroban_project"

Write-Host "Note: Update the filenames below to match the actual finalized filenames and locations before running this script."

# Item 1: Check closure documents
Write-Host "=== CHECKING CLOSURE DOCUMENTS ===" -ForegroundColor Cyan
@("PROJECT_CHARTER.md", "PROJECT_1_CLOSURE_DOCUMENT.md", "PROJECT_2_CLOSURE_DOCUMENT.md", 
  "PROJECT_3_CLOSURE_DOCUMENT.md", "MASTER_RESEARCH_SUMMARY.md", "FINAL_INTERPRETATION_MAP.md") | 
  ForEach-Object { 
    if (Test-Path $_) { Write-Host "✓ $_" } else { Write-Host "✗ MISSING: $_" } 
  }

# Item 2: Check code files
Write-Host "`n=== CHECKING CODE FILES ===" -ForegroundColor Cyan
@("src/models/residual_logic_adder.py", 
  "src/train/phase_26c_failure_audit.py", "src/train/phase_27c_architecture_audit.py",
  "src/train/phase_30_multidigit_learning.py", "src/train/phase_30b_stress_test.py",
  "src/train/project_3_residual_logic_layer.py", "src/train/project_3_killer_test_adversarial_carry_chain.py") | 
  ForEach-Object { 
    if (Test-Path $_) { Write-Host "✓ $_" } else { Write-Host "✗ MISSING: $_" } 
  }

# Item 3 & 4: Count phases & variants
Write-Host "`n=== ARCHIVABLE FILES ===" -ForegroundColor Cyan
$phases = @(Get-ChildItem -Path "src/train" -Filter "phase_*.py" -Exclude "*26c*", "*27c*", "*30*" -ErrorAction SilentlyContinue).Count
$variants = @(Get-ChildItem -Path "src/train" -Filter "project_3_v*.py" -ErrorAction SilentlyContinue).Count
Write-Host "Exploratory phases to archive: $phases"
Write-Host "Failed variants to archive: $variants"

# Item 6: Check MASTER_RESEARCH_SUMMARY uniqueness
Write-Host "`n=== CHECKING DUPLICATES ===" -ForegroundColor Cyan
$masters = @(Get-ChildItem -Recurse -Filter "MASTER_RESEARCH_SUMMARY.md" -ErrorAction SilentlyContinue)
if ($masters.Count -eq 1) { 
  Write-Host "✓ Single authoritative version: $($masters[0].FullName)" 
} else { 
  Write-Host "✗ Multiple versions found (delete duplicates):"
  $masters | ForEach-Object { Write-Host "  - $($_.FullName)" }
}

# Item 10: Test killer test
Write-Host "`n=== TESTING KILLER TEST ===" -ForegroundColor Cyan
if (Test-Path "src/train/project_3_killer_test_adversarial_carry_chain.py") {
  Write-Host "✓ Killer test file exists"
  Write-Host "  Run it manually to verify: python src/train/project_3_killer_test_adversarial_carry_chain.py"
} else {
  Write-Host "✗ Killer test file missing!"
}

Write-Host "`n=== AUDIT COMPLETE ===" -ForegroundColor Green
```

Save this as: `audit_checklist.ps1`
Run it: `.\audit_checklist.ps1`

================================================================================
DECISION: PROCEED OR HOLD?
================================================================================

**If output shows all ✓:**
→ SAFE TO PROCEED with reorganization

**If output shows any ✗:**
→ HOLD and FIX before proceeding

The goal: Ensure you don't delete anything important during cleanup.

================================================================================
Document created: March 29, 2026
Purpose: Pre-reorganization audit checklist
Status: Ready to use (update filenames as needed for current state)
Next step: Run checklist, resolve any mismatches, then proceed with REORGANIZATION_PLAN.md
================================================================================
