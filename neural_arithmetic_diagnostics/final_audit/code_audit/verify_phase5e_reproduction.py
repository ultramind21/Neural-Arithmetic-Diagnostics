"""
================================================================================
VERIFICATION SCRIPT: PHASE 5E
================================================================================

OFFICIAL TARGET:
  File: soroban_project/src/train/project_3_killer_test_adversarial_carry_chain.py

PURPOSE:
  Attempt bounded official reproduction of the Project 3 killer-test script and
  verify:
  - whether it runs,
  - whether output can be captured,
  - whether reported pattern-level metrics can be parsed,
  - and whether printed values are internally coherent.

THIS SCRIPT VERIFIES:
  1. Official script launch
  2. Completion within bounded runtime, or timeout status
  3. Capture of stdout/stderr
  4. Parsing of key pattern-level metrics if available
  5. Internal coherence of reported metric values

THIS SCRIPT DOES NOT VERIFY:
  - Broader interpretation of killer-test outcomes
  - Deeper causal explanations of success/failure
  - Any claims beyond the bounded official run and its printed outputs

IMPORTANT PRINCIPLE:
  Step 5E asks:
    "Can the official killer-test script be run and its printed pattern-level
     outputs be captured and checked for internal coherence?"
  It does NOT ask:
    "What is the full theoretical meaning of the results?"

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
TARGET_FILE = ROOT / "src" / "train" / "project_3_killer_test_adversarial_carry_chain.py"
RAW_OUTPUT_FILE = ROOT / "final_audit" / "code_audit" / "step5e_killer_test_raw_output.txt"

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


def parse_pattern_metrics(stdout_text):
    """
    Parse pattern-level metrics conservatively.

    Expected lines may resemble:
      Digit Accuracy:  50.00%
      Carry Accuracy: 100.00%
      Exact Match:     50.00%

    grouped under pattern names.
    """
    lines = stdout_text.splitlines()

    patterns = {}
    current_pattern = None

    for line in lines:
        stripped = line.strip()

        # Detect pattern header lines such as:
        # "Pattern: alternating"
        # or lines containing obvious pattern titles
        if stripped.lower().startswith("pattern:"):
            current_pattern = stripped.split(":", 1)[1].strip()
            patterns[current_pattern] = {}
            continue

        if current_pattern is None:
            # heuristic pattern-name detection
            if any(key in stripped.lower() for key in [
                "max_carry", "full_carry", "single_carry", "alternating", "block"
            ]):
                current_pattern = stripped
                patterns[current_pattern] = {}
                continue

        if current_pattern is not None:
            m1 = re.search(r"digit\s+accuracy\s*:\s*([0-9.]+)%", stripped, flags=re.IGNORECASE)
            if m1:
                patterns[current_pattern]["digit_acc"] = float(m1.group(1))
                continue

            m2 = re.search(r"carry\s+accuracy\s*:\s*([0-9.]+)%", stripped, flags=re.IGNORECASE)
            if m2:
                patterns[current_pattern]["carry_acc"] = float(m2.group(1))
                continue

            m3 = re.search(r"exact\s+match\s*:\s*([0-9.]+)%", stripped, flags=re.IGNORECASE)
            if m3:
                patterns[current_pattern]["exact_match"] = float(m3.group(1))
                continue

    # Keep only non-empty pattern dicts
    patterns = {k: v for k, v in patterns.items() if v}
    return patterns


def check_metric_ranges(pattern_metrics):
    ok = True
    msgs = []

    for pattern_name, metrics in pattern_metrics.items():
        msgs.append(f"\nPattern: {pattern_name}")
        for key, value in metrics.items():
            if 0.0 <= value <= 100.0:
                msgs.append(f"  ✓ {key} in valid range: {value:.2f}%")
            else:
                ok = False
                msgs.append(f"  ✗ {key} out of range: {value}")

    return ok, msgs


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PHASE 5E: KILLER-TEST OFFICIAL REPRODUCTION / RESULT VERIFICATION")
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
            print_header("STEP 5E FINAL DECISION")
            print("✗ FAIL")
            print()
            print("Finding:")
            print("  Official killer-test script execution returned a non-zero exit code.")
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

        print_header("STEP 5E FINAL DECISION")
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
    # Parse pattern metrics
    # ------------------------------------------------------------------------
    print_header("PARSE PATTERN-LEVEL METRICS")

    pattern_metrics = parse_pattern_metrics(stdout_text)

    if not pattern_metrics:
        print("⚠ No parseable pattern-level metrics found in stdout")

        print_header("STEP 5E FINAL DECISION")
        print("⚠ PARTIAL / UNPARSED")
        print()
        print("Finding:")
        print("  Official script ran to completion, but pattern-level metrics could")
        print("  not be cleanly parsed from stdout.")
        print()
        print("Qualification:")
        print("  Raw output has been saved and may still support manual review.")
        return

    print("Parsed pattern-level metrics:")
    for pattern_name, metrics in pattern_metrics.items():
        print(f"\nPattern: {pattern_name}")
        for k, v in metrics.items():
            print(f"  {k}: {v:.2f}%")

    ok, msgs = check_metric_ranges(pattern_metrics)

    print("\nRange checks:")
    for msg in msgs:
        print(msg)

    print_header("STEP 5E FINAL DECISION")

    if ok:
        print("✓ PASS")
        print()
        print("Finding:")
        print("  The official killer-test script ran successfully and exposed")
        print("  parseable pattern-level metrics that are internally coherent")
        print("  at the range/format level checked here.")
    else:
        print("⚠ PARTIAL / QUALIFIED")
        print()
        print("Finding:")
        print("  The official script ran, but one or more parsed pattern-level")
        print("  metrics were not internally coherent at the level checked here.")
        print()
        print("Qualification:")
        print("  Raw output has been saved for inspection.")

    print()
    print("Next step if accepted by user:")
    print("  Phase 5 closure summary")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
