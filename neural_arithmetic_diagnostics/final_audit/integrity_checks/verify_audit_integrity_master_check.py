"""
================================================================================
MASTER AUDIT INTEGRITY CHECK
================================================================================

PURPOSE:
  A single meta-consistency check over the completed audit archive.

THIS SCRIPT VERIFIES:
  1. Critical verification scripts still run successfully
  2. Raw-output artifacts exist and are non-empty
  3. Phase closure summaries contain the locked outcomes
  4. Master summary is consistent with phase summaries
  5. Locked caveats are present where expected

THIS SCRIPT DOES NOT VERIFY:
  - Full scientific truth from scratch
  - Deep mechanistic explanations
  - Exhaustive rerun of all training

IMPORTANT PRINCIPLE:
  This is a final integrity / consistency test for the audit backbone,
  not a replacement for the individual phase verifications.

================================================================================
"""

import subprocess
import sys
from pathlib import Path


# ============================================================================
# PATHS
# ============================================================================
# This script is at: final_audit/code_audit/verify_audit_integrity_master_check.py
# So parents[0] = code_audit, parents[1] = final_audit

CURRENT_DIR = Path(__file__).resolve().parent
CODE_AUDIT = CURRENT_DIR  # final_audit/code_audit
FINAL_AUDIT = CURRENT_DIR.parent  # final_audit

PYTHON = sys.executable


# ============================================================================
# HELPERS
# ============================================================================

def print_header(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def run_script(path):
    try:
        result = subprocess.run(
            [PYTHON, str(path)],
            capture_output=True,
            text=True,
            timeout=180
        )
        return result.returncode == 0, result
    except Exception as e:
        return False, e


def check_file_nonempty(path):
    return path.exists() and path.is_file() and path.stat().st_size > 0


def read_text(path):
    return path.read_text(encoding="utf-8") if path.exists() else ""


# ============================================================================
# CHECKS
# ============================================================================

def check_scripts():
    print_header("1) CRITICAL SCRIPT SPOT-CHECKS")

    scripts = [
        CODE_AUDIT / "verify_phase27c_step3b_diagnostic_shuffle.py",
        CODE_AUDIT / "verify_phase27c_step3c_ground_truth.py",
        CODE_AUDIT / "verify_phase27c_step3d_metrics.py",
        CODE_AUDIT / "verify_phase4c_ground_truth.py",
        CODE_AUDIT / "verify_phase4d_metrics.py",
        CODE_AUDIT / "verify_phase5d_metrics.py",
        CODE_AUDIT / "verify_phase6d_metrics.py",
    ]

    ok_all = True

    for script in scripts:
        if not script.exists():
            ok_all = False
            print(f"✗ Missing script: {script.name}")
            continue

        ok, result = run_script(script)
        if ok:
            print(f"✓ {script.name} executed successfully")
        else:
            ok_all = False
            if hasattr(result, "returncode"):
                print(f"✗ {script.name} failed (return code {result.returncode})")
            else:
                print(f"✗ {script.name} failed ({result})")

    return ok_all


def check_raw_outputs():
    print_header("2) RAW OUTPUT ARTIFACTS")

    files = [
        CODE_AUDIT / "step2e_phase26c_raw_output.txt",
        CODE_AUDIT / "step3e_phase27c_raw_output.txt",
        CODE_AUDIT / "step4e_project3_raw_output.txt",
        CODE_AUDIT / "step5e_killer_test_raw_output.txt",
        CODE_AUDIT / "step6e_phase30_raw_output.txt",
    ]

    ok_all = True
    for path in files:
        if check_file_nonempty(path):
            print(f"✓ Present and non-empty: {path.name}")
        else:
            ok_all = False
            print(f"✗ Missing or empty: {path.name}")

    return ok_all


def check_phase_summaries():
    print_header("3) PHASE SUMMARY CONSISTENCY")

    checks = [
        (
            CODE_AUDIT / "PHASE_3_CLOSURE_SUMMARY.md",
            ["FAIL / BIASED", "INCOMPLETE / TIMEOUT"]
        ),
        (
            CODE_AUDIT / "PHASE_4_CLOSURE_SUMMARY.md",
            ["VERIFIED AT BASELINE LEVEL", "PASS"]
        ),
        (
            CODE_AUDIT / "PHASE_5_CLOSURE_SUMMARY.md",
            ["PASS WITH QUALIFICATIONS", "parser coverage"]
        ),
        (
            CODE_AUDIT / "PHASE_6_CLOSURE_SUMMARY.md",
            ["INCOMPLETE / TIMEOUT", "MIXED"]
        ),
    ]

    ok_all = True

    for path, required_strings in checks:
        text = read_text(path)
        if not text:
            ok_all = False
            print(f"✗ Missing summary: {path.name}")
            continue

        missing = [s for s in required_strings if s not in text]
        if not missing:
            print(f"✓ {path.name} contains expected locked outcomes")
        else:
            ok_all = False
            print(f"✗ {path.name} missing expected strings: {missing}")

    return ok_all


def check_master_summary():
    print_header("4) MASTER SUMMARY CONSISTENCY")

    path = FINAL_AUDIT / "MASTER_AUDIT_SUMMARY_PHASES_1_TO_6.md"
    text = read_text(path)

    if not text:
        print("✗ Missing master audit summary")
        return False

    required = [
        "Phase 1",
        "Phase 2",
        "Phase 3",
        "Phase 4",
        "Phase 5",
        "Phase 6",
        "SUBSTANTIALLY RECOVERED WITH LOCKED QUALIFICATIONS",
    ]

    missing = [s for s in required if s not in text]
    if not missing:
        print("✓ Master audit summary contains expected global closure markers")
        return True
    else:
        print(f"✗ Master audit summary missing: {missing}")
        return False


def check_locked_caveats():
    print_header("5) LOCKED CAVEAT PRESENCE")

    files = [
        FINAL_AUDIT / "EXECUTIVE_SUMMARY_FINAL.md",
        FINAL_AUDIT / "QUICK_REFERENCE_FINAL.md",
        FINAL_AUDIT / "MASTER_AUDIT_SUMMARY_PHASES_1_TO_6.md",
    ]

    required_tokens = [
        "Phase 27c",
        "biased",
        "bounded official reproduction",
    ]

    ok_all = True

    for path in files:
        text = read_text(path)
        if not text:
            ok_all = False
            print(f"✗ Missing file: {path.name}")
            continue

        missing = [tok for tok in required_tokens if tok.lower() not in text.lower()]
        if not missing:
            print(f"✓ {path.name} includes key locked caveat references")
        else:
            ok_all = False
            print(f"✗ {path.name} missing caveat references: {missing}")

    return ok_all


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("MASTER AUDIT INTEGRITY CHECK")

    results = {
        "scripts": check_scripts(),
        "raw_outputs": check_raw_outputs(),
        "phase_summaries": check_phase_summaries(),
        "master_summary": check_master_summary(),
        "locked_caveats": check_locked_caveats(),
    }

    print_header("FINAL INTEGRITY DECISION")

    failed = [name for name, ok in results.items() if not ok]

    if not failed:
        print("✓ PASS")
        print()
        print("Finding:")
        print("  The audit archive is internally consistent at the integrity-check level.")
        print("  Critical scripts run, artifacts exist, phase summaries align,")
        print("  and locked caveats are present in the final documentation.")
    else:
        print("⚠ PARTIAL / NEEDS REVIEW")
        print()
        print("Finding:")
        print("  The audit archive is largely present, but some integrity checks failed.")
        print(f"  Failed sections: {failed}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
