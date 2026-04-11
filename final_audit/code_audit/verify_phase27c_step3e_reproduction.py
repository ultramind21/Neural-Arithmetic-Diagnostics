"""
================================================================================
VERIFICATION SCRIPT: PHASE 27C STEP 3E
================================================================================

OFFICIAL TARGET:
  File: soroban_project/src/train/phase_27c_architecture_audit.py

PURPOSE:
  Attempt official reproduction of Phase 27c by running the official script
  itself, capturing its output, and checking whether the reported architecture-
  level summaries are internally coherent.

CRITICAL NOTE (Step 3B Caveat):
  Step 3B established that cross-architecture test-pair distribution is BIASED.
  That caveat remains fully in force.
  Therefore, even if reproduction succeeds, any direct architecture comparison
  must carry the Step 3B qualification.

THIS SCRIPT VERIFIES:
  1. Whether the official Phase 27c script runs successfully
  2. Whether official stdout/stderr can be captured and saved
  3. Whether architecture-level summary blocks can be parsed
  4. Whether printed counts/rates are numerically self-consistent
  5. Whether reproduction completes within a bounded runtime window

THIS SCRIPT DOES NOT VERIFY:
  - Fairness of test-pair distribution (already failed in Step 3B)
  - Ground-truth semantics (verified in Step 3C)
  - Metric semantics (verified in Step 3D)
  - Whether architecture comparisons are methodologically clean
  - Mechanistic interpretation of performance differences

IMPORTANT PRINCIPLE:
  This step asks:
    "Can the official script itself be run and its reported summary results
     be captured and checked for internal coherence?"
  It does NOT ask:
    "Are the architectures fairly compared?" (Step 3B already says no)

================================================================================
"""

import re
import sys
import time
import subprocess
from pathlib import Path


# ============================================================================
# PATHS
# ============================================================================
ROOT = Path(__file__).resolve().parents[2]
TARGET_FILE = ROOT / "src" / "train" / "phase_27c_architecture_audit.py"
RAW_OUTPUT_FILE = ROOT / "final_audit" / "code_audit" / "step3e_phase27c_raw_output.txt"

# Keep bounded so the session does not hang forever.
TIMEOUT_SECONDS = 600


# ============================================================================
# HELPERS
# ============================================================================

def print_header(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def fail(msg):
    print(f"\nERROR: {msg}")
    sys.exit(1)


def save_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def parse_architecture_blocks(stdout_text):
    """
    Extract summary information per architecture from official stdout.

    Expected sections resemble:

      MLP FINAL RESULTS:
        Test accuracy: 73.1% ± 4.2%
        Total evaluations: 1800
        Total failures: 484

        CARRY cases (904 total):
          Failures: 391
          Failure rate: 43.3%

        NON-CARRY cases (896 total):
          Failures: 304
          Failure rate: 33.9%

        Difference: +9.4%
        Carry is 1.27× harder
    """
    architectures = ["MLP", "LSTM", "Transformer"]
    parsed = {}

    for arch in architectures:
        pattern = re.compile(
            rf"{arch}\s+FINAL RESULTS:\s*"
            rf"Test accuracy:\s*([0-9.]+)%\s*±\s*([0-9.]+)%\s*"
            rf"Total evaluations:\s*([0-9]+)\s*"
            rf"Total failures:\s*([0-9]+)\s*"
            rf"(?:CARRY cases\s*\(([0-9]+)\s*total\):\s*"
            rf"Failures:\s*([0-9]+)\s*"
            rf"Failure rate:\s*([0-9.]+)%\s*)?"
            rf"(?:NON-CARRY cases\s*\(([0-9]+)\s*total\):\s*"
            rf"Failures:\s*([0-9]+)\s*"
            rf"Failure rate:\s*([0-9.]+)%\s*)?"
            rf"(?:Difference:\s*([+-]?[0-9.]+)%\s*)?"
            rf"(?:Carry is\s*([0-9.]+)×\s*harder)?",
            re.MULTILINE | re.DOTALL
        )

        match = pattern.search(stdout_text)
        if match:
            parsed[arch] = {
                "test_accuracy_pct": float(match.group(1)),
                "test_std_pct": float(match.group(2)),
                "total_evaluations": int(match.group(3)),
                "total_failures": int(match.group(4)),
                "carry_examples": int(match.group(5)) if match.group(5) else None,
                "carry_failures": int(match.group(6)) if match.group(6) else None,
                "carry_failure_rate_pct": float(match.group(7)) if match.group(7) else None,
                "noncarry_examples": int(match.group(8)) if match.group(8) else None,
                "noncarry_failures": int(match.group(9)) if match.group(9) else None,
                "noncarry_failure_rate_pct": float(match.group(10)) if match.group(10) else None,
                "difference_pct": float(match.group(11)) if match.group(11) else None,
                "carry_harder_ratio": float(match.group(12)) if match.group(12) else None,
            }

    return parsed


def check_internal_coherence(metrics):
    """
    Check basic numeric self-consistency of one architecture summary block.
    Returns (ok: bool, messages: list[str]).
    """
    msgs = []
    ok = True

    total_evaluations = metrics["total_evaluations"]
    total_failures = metrics["total_failures"]
    test_accuracy_pct = metrics["test_accuracy_pct"]

    if not (0.0 <= test_accuracy_pct <= 100.0):
        ok = False
        msgs.append(f"✗ Test accuracy out of range: {test_accuracy_pct}")
    else:
        msgs.append(f"✓ Test accuracy in range: {test_accuracy_pct}%")

    if total_failures < 0 or total_failures > total_evaluations:
        ok = False
        msgs.append(f"✗ Total failures invalid: {total_failures} / {total_evaluations}")
    else:
        msgs.append(f"✓ Total failures in valid range: {total_failures} / {total_evaluations}")

    implied_accuracy = (total_evaluations - total_failures) / total_evaluations * 100.0
    if abs(implied_accuracy - test_accuracy_pct) > 0.2:
        ok = False
        msgs.append(
            f"✗ Accuracy mismatch: printed={test_accuracy_pct:.1f}% "
            f"vs implied={implied_accuracy:.1f}%"
        )
    else:
        msgs.append(
            f"✓ Accuracy consistent with failures: printed={test_accuracy_pct:.1f}% "
            f"vs implied={implied_accuracy:.1f}%"
        )

    carry_examples = metrics["carry_examples"]
    carry_failures = metrics["carry_failures"]
    carry_failure_rate_pct = metrics["carry_failure_rate_pct"]

    noncarry_examples = metrics["noncarry_examples"]
    noncarry_failures = metrics["noncarry_failures"]
    noncarry_failure_rate_pct = metrics["noncarry_failure_rate_pct"]

    if carry_examples is not None and noncarry_examples is not None:
        if carry_examples + noncarry_examples != total_evaluations:
            ok = False
            msgs.append(
                f"✗ Evaluation count mismatch: carry+noncarry="
                f"{carry_examples + noncarry_examples} vs total={total_evaluations}"
            )
        else:
            msgs.append(
                f"✓ Evaluation counts consistent: carry+noncarry="
                f"{carry_examples + noncarry_examples} = total={total_evaluations}"
            )

    if carry_failures is not None and noncarry_failures is not None:
        if carry_failures + noncarry_failures != total_failures:
            ok = False
            msgs.append(
                f"✗ Failure count mismatch: carry+noncarry="
                f"{carry_failures + noncarry_failures} vs total={total_failures}"
            )
        else:
            msgs.append(
                f"✓ Failure counts consistent: carry+noncarry="
                f"{carry_failures + noncarry_failures} = total={total_failures}"
            )

    if carry_examples and carry_failure_rate_pct is not None:
        implied_carry_rate = carry_failures / carry_examples * 100.0
        if abs(implied_carry_rate - carry_failure_rate_pct) > 0.2:
            ok = False
            msgs.append(
                f"✗ Carry failure rate mismatch: printed={carry_failure_rate_pct:.1f}% "
                f"vs implied={implied_carry_rate:.1f}%"
            )
        else:
            msgs.append(
                f"✓ Carry failure rate consistent: printed={carry_failure_rate_pct:.1f}% "
                f"vs implied={implied_carry_rate:.1f}%"
            )

    if noncarry_examples and noncarry_failure_rate_pct is not None:
        implied_noncarry_rate = noncarry_failures / noncarry_examples * 100.0
        if abs(implied_noncarry_rate - noncarry_failure_rate_pct) > 0.2:
            ok = False
            msgs.append(
                f"✗ Non-carry failure rate mismatch: printed={noncarry_failure_rate_pct:.1f}% "
                f"vs implied={implied_noncarry_rate:.1f}%"
            )
        else:
            msgs.append(
                f"✓ Non-carry failure rate consistent: printed={noncarry_failure_rate_pct:.1f}% "
                f"vs implied={implied_noncarry_rate:.1f}%"
            )

    return ok, msgs


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PHASE 27C STEP 3E: OFFICIAL REPRODUCTION / RESULT VERIFICATION")
    print(f"Official target: {TARGET_FILE}")
    print(f"Raw output file: {RAW_OUTPUT_FILE}")
    print(f"Timeout: {TIMEOUT_SECONDS} seconds")

    print_header("STEP 3B CAVEAT")
    print("Step 3B established that cross-architecture test-pair distribution is BIASED.")
    print("This caveat remains fully in force.")
    print("Any reproduced architecture comparison must carry that qualification.")

    if not TARGET_FILE.exists():
        fail(f"Official target file not found: {TARGET_FILE}")

    print_header("RUN OFFICIAL SCRIPT")
    command = [sys.executable, str(TARGET_FILE)]
    print("Command:")
    print(" ", " ".join(f'"{c}"' if " " in c else c for c in command))

    start = time.time()

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS
        )
        elapsed = time.time() - start

        stdout_text = result.stdout or ""
        stderr_text = result.stderr or ""
        combined_text = (
            "===== STDOUT =====\n"
            + stdout_text
            + "\n\n===== STDERR =====\n"
            + stderr_text
        )
        save_text(RAW_OUTPUT_FILE, combined_text)

        print(f"\nReturn code: {result.returncode}")
        print(f"Elapsed time: {elapsed:.1f} seconds")
        print(f"Raw output saved to: {RAW_OUTPUT_FILE}")

        if result.returncode != 0:
            print_header("STEP 3E FINAL DECISION")
            print("✗ FAIL")
            print()
            print("Finding:")
            print("  Official script execution returned a non-zero exit code.")
            print("  Reproduction cannot yet be considered successful.")
            print()
            print("Qualification:")
            print("  Raw stdout/stderr were saved for inspection.")
            print("  Step 3B caveat remains unchanged.")
            return

    except subprocess.TimeoutExpired as e:
        elapsed = time.time() - start
        stdout_text = e.stdout or ""
        stderr_text = e.stderr or ""

        if isinstance(stdout_text, bytes):
            stdout_text = stdout_text.decode(errors="replace")
        if isinstance(stderr_text, bytes):
            stderr_text = stderr_text.decode(errors="replace")

        combined_text = (
            "===== PARTIAL STDOUT (TIMEOUT) =====\n"
            + stdout_text
            + "\n\n===== PARTIAL STDERR (TIMEOUT) =====\n"
            + stderr_text
        )
        save_text(RAW_OUTPUT_FILE, combined_text)

        print(f"\nTimeout after {elapsed:.1f} seconds")
        print(f"Partial output saved to: {RAW_OUTPUT_FILE}")

        print_header("STEP 3E FINAL DECISION")
        print("⚠ INCOMPLETE / TIMEOUT")
        print()
        print("Finding:")
        print("  Official reproduction did not complete within the time limit.")
        print("  This is not enough to validate reproduction success or failure.")
        print()
        print("Qualification:")
        print("  Partial output was saved for later inspection.")
        print("  Step 3B caveat remains unchanged.")
        return

    # ------------------------------------------------------------------------
    # Parse and validate output
    # ------------------------------------------------------------------------
    print_header("PARSE ARCHITECTURE RESULTS")
    parsed = parse_architecture_blocks(stdout_text)

    if not parsed:
        print("No architecture summary blocks could be parsed.")

        print_header("STEP 3E FINAL DECISION")
        print("⚠ PARTIAL / UNPARSED")
        print()
        print("Finding:")
        print("  Official script ran to completion, but summary results could not be")
        print("  cleanly parsed from stdout.")
        print()
        print("Qualification:")
        print("  Raw output has been saved and may still support manual review.")
        print("  Step 3B caveat remains unchanged.")
        return

    overall_ok = True

    for arch_name in ["MLP", "LSTM", "Transformer"]:
        print_header(f"ARCHITECTURE SUMMARY: {arch_name}")
        if arch_name not in parsed:
            overall_ok = False
            print("✗ Could not parse this architecture block.")
            continue

        metrics = parsed[arch_name]
        for k, v in metrics.items():
            print(f"{k:<26}: {v}")

        ok, msgs = check_internal_coherence(metrics)
        for msg in msgs:
            print(msg)

        if not ok:
            overall_ok = False

    print_header("STEP 3E FINAL DECISION")

    if overall_ok and len(parsed) == 3:
        print("✓ PASS")
        print()
        print("Finding:")
        print("  The official Phase 27c script ran successfully, produced parseable")
        print("  results for all 3 architectures, and those summaries were internally")
        print("  numerically coherent.")
        print()
        print("Qualification:")
        print("  This does NOT remove the Step 3B bias finding.")
        print("  Reproduced architecture comparisons still carry a test-pair")
        print("  distribution caveat.")
    else:
        print("⚠ PARTIAL / QUALIFIED")
        print()
        print("Finding:")
        print("  The official script ran, but one or more architecture summaries were")
        print("  missing or numerically inconsistent.")
        print()
        print("Qualification:")
        print("  Raw output has been saved for inspection.")
        print("  Step 3B caveat remains unchanged.")

    print()
    print("Next step if accepted by user:")
    print("  Phase 3 summary / documentation update")
    print("  or optional deeper follow-up depending on project needs")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
