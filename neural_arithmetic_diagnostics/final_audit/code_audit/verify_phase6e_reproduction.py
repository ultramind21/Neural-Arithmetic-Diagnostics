"""
================================================================================
VERIFICATION SCRIPT: PHASE 6E
================================================================================

OFFICIAL TARGET:
  File: soroban_project/src/train/phase_30_multidigit_learning.py

PURPOSE:
  Attempt bounded official reproduction of the Phase 30 multidigit learning file
  and verify:
  - whether it runs,
  - whether output can be captured,
  - whether reported metrics can be parsed,
  - and whether printed values are internally coherent.

THIS SCRIPT VERIFIES:
  1. Official script launch
  2. Completion within bounded runtime, or timeout status
  3. Capture of stdout/stderr
  4. Parsing of key reported metrics if available
  5. Internal coherence of reported metric values at the range/format level

THIS SCRIPT DOES NOT VERIFY:
  - Broader historical interpretation of Phase 30
  - Deep causal explanations of the crisis
  - Any claims beyond the bounded official run and printed outputs

IMPORTANT PRINCIPLE:
  Step 6E asks:
    "Can the official Phase 30 script be run and its printed outputs be captured
     and checked for internal coherence?"
  It does NOT ask:
    "Does this by itself resolve every historical inconsistency?"

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
TARGET_FILE = ROOT / "src" / "train" / "phase_30_multidigit_learning.py"
RAW_OUTPUT_FILE = ROOT / "final_audit" / "code_audit" / "step6e_phase30_raw_output.txt"

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


def parse_metrics(stdout_text):
    """
    Conservative metric parser for Phase 30 output.
    Looks for common reporting patterns such as:
      digit_acc: 0.95
      carry_acc: 0.88
      exact_match: 0.80
    or percentage-style outputs.
    """
    patterns = {
        "digit_acc": [
            r"digit[_ ]?acc(?:uracy)?\s*[:=]\s*([0-9.]+)",
            r"digit accuracy\s*[:=]\s*([0-9.]+)",
        ],
        "carry_acc": [
            r"carry[_ ]?acc(?:uracy)?\s*[:=]\s*([0-9.]+)",
            r"carry accuracy\s*[:=]\s*([0-9.]+)",
        ],
        "exact_match": [
            r"exact[_ ]?match\s*[:=]\s*([0-9.]+)",
            r"exact match\s*[:=]\s*([0-9.]+)",
        ],
    }

    found = {}

    for key, plist in patterns.items():
        for pattern in plist:
            m = re.search(pattern, stdout_text, flags=re.IGNORECASE)
            if m:
                found[key] = float(m.group(1))
                break

    return found


def normalize_metric(x):
    if x > 1.0:
        return x / 100.0
    return x


def range_checks(metrics):
    ok = True
    msgs = []
    normalized = {k: normalize_metric(v) for k, v in metrics.items()}

    for k, v in normalized.items():
        if 0.0 <= v <= 1.0:
            msgs.append(f"✓ {k} in valid range after normalization: {v:.6f}")
        else:
            ok = False
            msgs.append(f"✗ {k} out of valid range after normalization: {v}")

    return ok, msgs, normalized


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PHASE 6E: PHASE-30 OFFICIAL REPRODUCTION / RESULT VERIFICATION")
    print(f"Official target: {TARGET_FILE}")
    print(f"Raw output file: {RAW_OUTPUT_FILE}")
    print(f"Timeout: {TIMEOUT_SECONDS} seconds")

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
            print_header("STEP 6E FINAL DECISION")
            print("✗ FAIL")
            print()
            print("Finding:")
            print("  Official Phase 30 script execution returned a non-zero exit code.")
            print("  Reproduction cannot yet be considered successful.")
            print()
            print("Qualification:")
            print("  Raw stdout/stderr were saved for inspection.")
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

        print_header("STEP 6E FINAL DECISION")
        print("⚠ INCOMPLETE / TIMEOUT")
        print()
        print("Finding:")
        print("  Official reproduction did not complete within the time limit.")
        print("  This is not enough to validate reproduction success or failure.")
        print()
        print("Qualification:")
        print("  Partial output was saved for later inspection.")
        return

    # ------------------------------------------------------------------------
    # Parse metrics
    # ------------------------------------------------------------------------
    print_header("PARSE REPORTED METRICS")

    metrics = parse_metrics(stdout_text)

    if not metrics:
        print("⚠ No parseable summary metrics found in stdout")

        print_header("STEP 6E FINAL DECISION")
        print("⚠ PARTIAL / UNPARSED")
        print()
        print("Finding:")
        print("  Official script ran to completion, but key summary metrics could not")
        print("  be cleanly parsed from stdout.")
        print()
        print("Qualification:")
        print("  Raw output has been saved and may still support manual review.")
        return

    print("Parsed metrics:")
    for k, v in metrics.items():
        print(f"  {k}: {v}")

    ok, msgs, normalized = range_checks(metrics)

    print("\nRange checks:")
    for msg in msgs:
        print(f"  {msg}")

    print_header("STEP 6E FINAL DECISION")

    if ok:
        print("✓ PASS")
        print()
        print("Finding:")
        print("  The official Phase 30 script ran successfully and exposed")
        print("  parseable summary metrics that are internally coherent at the")
        print("  range/format level checked here.")
        print()
        print("Normalized metrics:")
        for k, v in normalized.items():
            print(f"  {k}: {v:.6f}")
    else:
        print("⚠ PARTIAL / QUALIFIED")
        print()
        print("Finding:")
        print("  The official script ran, but one or more parsed metrics were not")
        print("  internally coherent at the level checked here.")
        print()
        print("Qualification:")
        print("  Raw output has been saved for inspection.")

    print()
    print("Next step if accepted by user:")
    print("  Phase 6 closure summary")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
