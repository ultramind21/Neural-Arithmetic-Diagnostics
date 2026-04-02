================================================================================
POST-REORGANIZATION VERIFICATION CHECKLIST
Repository Cleanup Verification Template
================================================================================

Use this checklist after reorganization work is completed or whenever the final repository structure needs to be audited.
Purpose: verify that the intended final organization is in place and that no critical files were lost or duplicated.

Important note:
This checklist describes the intended final repository organization. It should be interpreted as a verification template, not as evidence that the reorganization has already been completed.

================================================================================
VERIFICATION ITEMS
================================================================================

## ✓ ITEM 1: Verify Final Directory Structure Matches Intended Plan

**Action:** Check that directory structure matches the intended final organization

Expected structure:
```
soroban_project/
├── [6 root documentation files]
├── src/
│   ├── models/
│   │   └── residual_logic_adder.py (1 file only)
│   └── train/
│       └── [6 reference scripts + 1 killer test = 7 files total]
├── Papers/
│   └── [supporting analysis only]
├── archive/
│   ├── exploratory_phases/
│   ├── failed_variants/
│   ├── diagnostic_scripts/
│   └── big_data/
└── [other folders: checkpoints, data, etc.]
```

Command to verify:
```powershell
Write-Host "=== DIRECTORY STRUCTURE ===" -ForegroundColor Cyan

Write-Host "`nRoot documentation:"
(Get-ChildItem -Path "." -MaxDepth 1 -File -Filter "*DOCUMENT.md" -o -Filter "PROJECT_*.md" -o -Filter "MASTER_*.md" -o -Filter "FINAL_*.md" -o -Filter "*CHARTER.md").Count | 
  ForEach-Object { Write-Host "  Files found: $_" }

Write-Host "`nsrc/models/"
(Get-ChildItem -Path "src/models" -File).Count | 
  ForEach-Object { Write-Host "  Files: $_ (should be 1)" }

Write-Host "`nsrc/train/"
(Get-ChildItem -Path "src/train" -File).Count | 
  ForEach-Object { Write-Host "  Files: $_ (should be 7)" }

Write-Host "`narchive/"
if (Test-Path "archive") { 
  Write-Host "  ✓ Exists (with subdirs: exploratory_phases, failed_variants, diagnostic_scripts, big_data)"
} else {
  Write-Host "  ✗ Missing!"
}
```

Checklist:
- [ ] Root has 6+ documentation files (all DOCUMENT.md names, no *_FINAL.md)
- [ ] src/models/ has exactly 1 file: residual_logic_adder.py
- [ ] src/train/ has exactly 7 files (the reference benchmarks + killer test)
- [ ] Papers/ exists with supporting analysis
- [ ] archive/ exists with 4 subdirectories
- [ ] Old phases (10-25) are NOT in src/train/ (they're in archive/)
- [ ] Old variants (v4c, v4d, v3*) are NOT in src/train/ (they're in archive/)

---

## ✓ ITEM 2: Verify src/train/ Contains The Approved Final Training Scripts

**Action:** List all files in src/train/ and verify they match the intended final set

Intended final files:
```
phase_26c_failure_audit.py
phase_27c_architecture_audit.py
phase_30_multidigit_learning.py
phase_30b_stress_test.py
project_3_residual_logic_layer.py
project_3_killer_test_adversarial_carry_chain.py
```

Command:
```powershell
$expected = @(
  "phase_26c_failure_audit.py",
  "phase_27c_architecture_audit.py", 
  "phase_30_multidigit_learning.py",
  "phase_30b_stress_test.py",
  "project_3_residual_logic_layer.py",
  "project_3_killer_test_adversarial_carry_chain.py"
)

$actual = Get-ChildItem -Path "src/train" -Filter "*.py" | Select-Object -ExpandProperty Name | Sort-Object

$missing = $expected | Where-Object { $actual -notcontains $_ }
$unexpected = $actual | Where-Object { $expected -notcontains $_ }

if ($missing.Count -eq 0 -and $unexpected.Count -eq 0) {
  Write-Host "✓ src/train/ contains exactly the approved final scripts"
} else {
  if ($missing) { Write-Host "✗ Missing files: $missing" }
  if ($unexpected) { Write-Host "✗ Unexpected files: $unexpected" }
}
```

Checklist:
- [ ] Exactly 6 files in src/train/ (the approved final training scripts)
- [ ] All 6 reference scripts present
- [ ] NO other .py files (old phases moved to archive)

---

## ✓ ITEM 3: Verify No Duplicate Documents in Root

**Action:** Check for conflicting document names

Command:
```powershell
Get-ChildItem -Path "." -MaxDepth 1 -File | Where-Object { 
  $_.Name -match "CLOSURE|RESEARCH|CHARTER|INTERPRETATION" 
} | ForEach-Object {
  Write-Host $_.Name
}
```

Expected output (no duplicates):
```
PROJECT_1_CLOSURE_DOCUMENT.md
PROJECT_2_CLOSURE_DOCUMENT.md
PROJECT_3_CLOSURE_DOCUMENT.md
MASTER_RESEARCH_SUMMARY.md
PROJECT_CHARTER.md
FINAL_INTERPRETATION_MAP.md
```

Checklist:
- [ ] NO files ending in *_FINAL.md (should be *_DOCUMENT.md)
- [ ] NO duplicate PROJECT_2_CLOSURE_FINAL.md
- [ ] Exactly one MASTER_RESEARCH_SUMMARY.md
- [ ] All official documents in root (not scattered elsewhere)

---

## ✓ ITEM 4: Verify Archive Has All Exploratory Phases

**Action:** Count moved files in archive/exploratory_phases/

Command:
```powershell
$count = @(Get-ChildItem -Path "archive/exploratory_phases" -Recurse -Filter "*.py" -ErrorAction SilentlyContinue).Count
Write-Host "Files in archive/exploratory_phases: $count"
Write-Host "  (Should be roughly 50+ files from phases 10-25)"
```

Checklist:
- [ ] archive/exploratory_phases/ contains phase_10_* through phase_25_*
- [ ] Count is substantial (30+)
- [ ] These files are NOT in src/train/
- [ ] README in archive explains what these are

---

## ✓ ITEM 5: Verify Archive Has All Failed Variants

**Action:** Count moved files in archive/failed_variants/

Command:
```powershell
$count = @(Get-ChildItem -Path "archive/failed_variants" -Recurse -Filter "*.py" -ErrorAction SilentlyContinue).Count
Write-Host "Files in archive/failed_variants: $count"
Write-Host "  (Should be roughly 10-20 files: v4c, v4d, v3*, etc.)"
```

Checklist:
- [ ] archive/failed_variants/ contains v4c_*, v4d_*, v3*_* files
- [ ] Count is reasonable (10+)
- [ ] These files are NOT in src/train/
- [ ] README explains why these failed

---

## ✓ ITEM 6: Verify No Master Duplicates (Papers/ vs Root)

**Action:** Check MASTER_RESEARCH_SUMMARY.md exists only once

Command:
```powershell
$locations = @(
  "MASTER_RESEARCH_SUMMARY.md",
  "Papers/MASTER_RESEARCH_SUMMARY.md",
  "Papers/OLD_MASTER_RESEARCH_SUMMARY.md"
)

foreach ($loc in $locations) {
  if (Test-Path $loc) {
    Write-Host "Found: $loc"
  }
}
```

Expected: ONLY soroban_project/MASTER_RESEARCH_SUMMARY.md exists

Checklist:
- [ ] Root MASTER_RESEARCH_SUMMARY.md exists ✓
- [ ] NO Papers/MASTER_RESEARCH_SUMMARY.md ✓
- [ ] This is the single source of truth ✓

---

## ✓ ITEM 7: Verify New Reorganization Files Created

**Action:** Check that new organizational files exist

Files created during reorganization:
- [ ] PROJECT_3_CLOSURE_DOCUMENT.md ✓
- [ ] REORGANIZATION_PLAN.md ✓
- [ ] FINAL_DELIVERABLES_OFFICIAL.md ✓
- [ ] PRE_REORGANIZATION_AUDIT_CHECKLIST.md (this file) ✓
- [ ] POST_REORGANIZATION_VERIFICATION_CHECKLIST.md (coming)

Command:
```powershell
$newFiles = @(
  "PROJECT_3_CLOSURE_DOCUMENT.md",
  "REORGANIZATION_PLAN.md",
  "FINAL_DELIVERABLES_OFFICIAL.md",
  "PRE_REORGANIZATION_AUDIT_CHECKLIST.md"
)

foreach ($file in $newFiles) {
  if (Test-Path $file) { 
    Write-Host "✓ $file" 
  } else { 
    Write-Host "✗ MISSING: $file" 
  }
}
```

Checklist:
- [ ] All new organizational files present
- [ ] These are in root (not buried elsewhere)
- [ ] They reference each other correctly

---

## ✓ ITEM 8: Verify Killer Test Is Runnable

**Action:** Quick syntax check of killer test code

Command:
```powershell
python -m py_compile "src/train/project_3_killer_test_adversarial_carry_chain.py"
if ($LASTEXITCODE -eq 0) {
  Write-Host "✓ Killer test compiles successfully"
} else {
  Write-Host "✗ Killer test has syntax errors"
}
```

Checklist:
- [ ] Killer test compiles without errors ✓
- [ ] No import errors when importing ✓
- [ ] File size is reasonable (not corrupted during move) ✓

---

## ✓ ITEM 9: Verify README Files In Archive Exist

**Action:** Check that archive/ has explanatory README files

Expected:
- [ ] archive/README.md (explains why things are archived, how to navigate)
- [ ] archive/exploratory_phases/README.md (explains these phases)
- [ ] archive/failed_variants/README.md (explains why they failed)
- [ ] archive/diagnostic_scripts/README.md (explains what these do)

Command:
```powershell
@(
  "archive/README.md",
  "archive/exploratory_phases/README.md",
  "archive/failed_variants/README.md",
  "archive/diagnostic_scripts/README.md"
) | ForEach-Object {
  if (Test-Path $_) { Write-Host "✓ $_" } else { Write-Host "✗ MISSING: $_" }
}
```

Checklist:
- [ ] archive/README.md exists (main index)
- [ ] Each subdirectory has its own README explaining purpose
- [ ] READMEs reference the main MASTER_RESEARCH_SUMMARY.md

---

## ✓ ITEM 10: Final Sanity Check - Can You Find Everything?

**Action:** Simulate being a new reader. Can you find key files?

Test questions (Can you answer from the repo structure?):
```
Q1: Where is the official Project 3 closure?
A:  PROJECT_3_CLOSURE_DOCUMENT.md (root) ✓ or ✗

Q2: Where is the killer test code?
A:  src/train/project_3_killer_test_adversarial_carry_chain.py ✓ or ✗

Q3: Where are the main findings?
A:  MASTER_RESEARCH_SUMMARY.md ✓ or ✗

Q4: Where are intermediate phases?
A:  archive/exploratory_phases/ ✓ or ✗

Q5: Where do I find what all 13 final files are?
A:  FINAL_DELIVERABLES_OFFICIAL.md ✓ or ✗
```

If you can answer all 5 in 30 seconds with the intended structure:
- [ ] Repository organization matches the plan ✓

If you can't:
- [ ] Something is missing or misplaced

---

================================================================================
SCORING & DECISION
================================================================================

**Count checkmarks:**
- Total possible: 50+
- Reorganization successful if: 95%+ pass
- Requires fixing if: <95%

**If any ITEM fails:**
1. Identify what failed
2. Fix that specific thing
3. Re-run that item's verification
4. Consider if failures are acceptable or must be fixed before closure

**If all ITEMS pass:**
→ Reorganization is complete and verified
→ Repository structure is clean and internally consistent
→ The final file layout can be treated as the maintained reference version

================================================================================
COMPLETE VERIFICATION SCRIPT
================================================================================

Note: Update the filename checks below to match the actual finalized file names before running this script.

Save this as: `verify_reorganization.ps1`

```powershell
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║ POST-REORGANIZATION VERIFICATION                             ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green

$score = 0

# Item 1: Directory structure
Write-Host "`n[1/10] Checking directory structure..." -ForegroundColor Cyan
$required_dirs = @("src/models", "src/train", "Papers", "archive")
$dirs_ok = 0
foreach ($dir in $required_dirs) {
  if (Test-Path $dir) { 
    Write-Host "  ✓ $dir exists"
    $dirs_ok++ 
  } else { 
    Write-Host "  ✗ $dir MISSING"
  }
}
if ($dirs_ok -eq 4) { $score++ }

# Item 2: src/train files
Write-Host "`n[2/10] Checking src/train/ files..." -ForegroundColor Cyan
$required_files = @(
  "src/train/phase_26c_failure_audit.py",
  "src/train/phase_27c_architecture_audit.py",
  "src/train/phase_30_multidigit_learning.py",
  "src/train/phase_30b_stress_test.py",
  "src/train/project_3_residual_logic_layer.py",
  "src/train/project_3_killer_test_adversarial_carry_chain.py"
)
$files_ok = 0
foreach ($file in $required_files) {
  if (Test-Path $file) { 
    Write-Host "  ✓ $(Split-Path $file -Leaf)"
    $files_ok++
  } else { 
    Write-Host "  ✗ MISSING: $(Split-Path $file -Leaf)"
  }
}
if ($files_ok -eq 6) { $score++ }

# Item 3: No duplicates
Write-Host "`n[3/10] Checking for duplicate CLOSURE documents..." -ForegroundColor Cyan
$closure_files = Get-ChildItem -Filter "*CLOSURE*.md" -ErrorAction SilentlyContinue | Measure-Object
if ($closure_files.Count -eq 3) {
  Write-Host "  ✓ Exactly 3 CLOSURE documents (no duplicates)"
  $score++
} else {
  Write-Host "  ✗ Expected 3 CLOSURE documents, found $($closure_files.Count)"
}

# Item 4: Archive exploratory
Write-Host "`n[4/10] Checking archive/exploratory_phases/..." -ForegroundColor Cyan
$archived_phases = @(Get-ChildItem -Path "archive/exploratory_phases" -Recurse -Filter "*.py" -ErrorAction SilentlyContinue).Count
if ($archived_phases -gt 0) {
  Write-Host "  ✓ Found $archived_phases archived phase files"
  $score++
} else {
  Write-Host "  ✗ No archived phases found (should move old phases here)"
}

# Item 5: Archive variants
Write-Host "`n[5/10] Checking archive/failed_variants/..." -ForegroundColor Cyan
$archived_variants = @(Get-ChildItem -Path "archive/failed_variants" -Recurse -Filter "*.py" -ErrorAction SilentlyContinue).Count
if ($archived_variants -gt 0) {
  Write-Host "  ✓ Found $archived_variants archived variant files"
  $score++
} else {
  Write-Host "  ✗ No archived variants found (should move v4c, v4d, v3 here)"
}

# Item 6: Master document uniqueness
Write-Host "`n[6/10] Checking MASTER_RESEARCH_SUMMARY uniqueness..." -ForegroundColor Cyan
$masters = Get-ChildItem -Recurse -Filter "MASTER_RESEARCH_SUMMARY.md" -ErrorAction SilentlyContinue
if ($masters.Count -eq 1) {
  Write-Host "  ✓ Single authoritative version found"
  $score++
} else {
  Write-Host "  ⚠ Found $($masters.Count) version(s) of MASTER_RESEARCH_SUMMARY.md (verify which is the authoritative one)"
}

# Item 7: New organizational files
Write-Host "`n[7/10] Checking new organizational files..." -ForegroundColor Cyan
$new_files = @(
  "PROJECT_3_CLOSURE_DOCUMENT.md",
  "REORGANIZATION_PLAN.md",
  "FINAL_DELIVERABLES_OFFICIAL.md"
)
$new_ok = 0
foreach ($file in $new_files) {
  if (Test-Path $file) { 
    Write-Host "  ✓ $file"
    $new_ok++
  }
}
if ($new_ok -eq 3) { $score++ }

# Item 8: Killer test syntax
Write-Host "`n[8/10] Checking killer test syntax..." -ForegroundColor Cyan
$killer_test = "src/train/project_3_killer_test_adversarial_carry_chain.py"
if (Test-Path $killer_test) {
  python -m py_compile $killer_test 2>$null
  if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Killer test compiles successfully"
    $score++
  } else {
    Write-Host "  ✗ Killer test syntax errors"
  }
}

# Item 9: Archive READMEs
Write-Host "`n[9/10] Checking archive README files..." -ForegroundColor Cyan
$archive_readme = Test-Path "archive/README.md"
if ($archive_readme) {
  Write-Host "  ✓ archive/README.md exists"
  $score++
} else {
  Write-Host "  ✗ archive/README.md missing (create it)"
}

# Item 10: Sanity check questions
Write-Host "`n[10/10] Sanity check - Can you find key files?..." -ForegroundColor Cyan
$files_found = 0
if (Test-Path "PROJECT_3_CLOSURE_DOCUMENT.md") { $files_found++ }
if (Test-Path "src/train/project_3_killer_test_adversarial_carry_chain.py") { $files_found++ }
if (Test-Path "MASTER_RESEARCH_SUMMARY.md") { $files_found++ }
if (Test-Path "FINAL_DELIVERABLES_OFFICIAL.md") { $files_found++ }

if ($files_found -eq 4) {
  Write-Host "  ✓ All key files readily locatable"
  $score++
} else {
  Write-Host "  ✗ Missing $($4 - $files_found) key files"
}

# Summary
Write-Host "`n╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║ VERIFICATION SCORE: $score / 10 ✓                            ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green

if ($score -ge 9) {
  Write-Host "`n✓ VERIFICATION COMPLETE - Repository organization matches the plan" -ForegroundColor Green
  exit 0
} elseif ($score -ge 7) {
  Write-Host "`n⚠ VERIFICATION PARTIAL - Some items need attention or clarification" -ForegroundColor Yellow
  exit 1
} else {
  Write-Host "`n✗ VERIFICATION INCOMPLETE - Significant gaps remain" -ForegroundColor Red
  exit 2
}
```

Run: `.\verify_reorganization.ps1`

================================================================================
IF VERIFICATION FAILS
================================================================================

Common issues and fixes:

**Issue 1: Files still in src/train/ that should be archived**
Fix: `mv src/train/phase_10_*.py archive/exploratory_phases/`

**Issue 2: Duplicate MASTER_RESEARCH_SUMMARY.md**
Fix: Delete Papers/MASTER_RESEARCH_SUMMARY.md and keep only root version

**Issue 3: Not all files moved to archive**
Fix: Re-run REORGANIZATION_PLAN.md steps 1-6

**Issue 4: Killer test has syntax errors**
Fix: Verify the file wasn't corrupted during move. If corrupted, restore from backup.

**Issue 5: Missing README files in archive/**
Fix: Create them using template:
```markdown
# archive/[subdirectory]/README.md

This directory contains [description of content].
These were [reason for archiving].
See MASTER_RESEARCH_SUMMARY.md for the official research findings.
```

================================================================================
Status: Verification checklist template ready for use after cleanup
Next: Use this checklist to verify the implementation of REORGANIZATION_PLAN.md
================================================================================
