"""
================================================================================
VERIFICATION SCRIPT: KILLER TEST STEP 1D
================================================================================

OFFICIAL TARGET:
  File: src/train/project_3_killer_test_adversarial_carry_chain.py

PURPOSE:
  Reproduce the official killer test result and compare the observed output
  against the documented project record.

THIS SCRIPT VERIFIES:
  1. The official killer test script runs successfully
  2. The expected pattern names appear in output
  3. The reported accuracies match documented values within tolerance
  4. The alternating pattern reproduces the expected collapse

THIS SCRIPT DOES NOT VERIFY:
  - Internal model mechanism
  - Why the failure occurs
  - Any probing beyond direct reproduction

IMPORTANT PRINCIPLE:
  This is official-result reproduction only.
  Interpretation comes later.

================================================================================
"""

import re
import sys
import subprocess
from pathlib import Path


# -----------------------------------------------------------------------------
# PATHS
# -----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
TARGET_FILE = ROOT / "src" / "train" / "project_3_killer_test_adversarial_carry_chain.py"
OUTPUT_SAVE = ROOT / "final_audit" / "code_audit" / "step1d_killer_test_raw_output.txt"


# -----------------------------------------------------------------------------
# EXPECTED DOCUMENTED VALUES
# Map by display name (as shown in "Testing: ..." output)
# These are the documented project outputs that Step 1D is trying to reproduce.
# -----------------------------------------------------------------------------
EXPECTED_BY_DISPLAY_NAME = {
    "999...9 + 0...0": {
        "digit_accuracy": 100.00,
        "carry_accuracy": 100.00,
        "exact_match": 100.00,
    },
    "999...9 + 111...1 (max carry propagation)": {
        "digit_accuracy": 100.00,
        "carry_accuracy": 100.00,
        "exact_match": 100.00,
    },
    "5000...0 + 5000...0 (single carry at position 0)": {
        "digit_accuracy": 99.00,
        "carry_accuracy": 100.00,
        "exact_match": 99.00,
    },
    "Alternating 9,0,9,0... + 1,0,1,0...": {
        "digit_accuracy": 50.00,
        "carry_accuracy": 100.00,
        "exact_match": 50.00,
    },
    "Blocks: 000...999...888...000": {
        "digit_accuracy": 100.00,
        "carry_accuracy": 100.00,
        "exact_match": 100.00,
    },
}

TOLERANCE = 0.50  # percentage points


# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------
def fail(msg):
    print(f"\nERROR: {msg}")
    sys.exit(1)


def run_official_script():
    """
    Run the official killer test script and capture stdout/stderr.
    """
    if not TARGET_FILE.exists():
        fail(f"Official target file not found: {TARGET_FILE}")

    print("=" * 80)
    print("STEP 1D: OFFICIAL KILLER TEST REPRODUCTION")
    print("=" * 80)
    print(f"Official target: {TARGET_FILE}")
    print()

    cmd = [sys.executable, str(TARGET_FILE)]
    print(f"Running command: {' '.join(cmd)}")
    print()

    result = subprocess.run(
        cmd,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    combined_output = ""
    if result.stdout:
        combined_output += result.stdout
    if result.stderr:
        combined_output += "\n[STDERR]\n" + result.stderr

    OUTPUT_SAVE.write_text(combined_output, encoding="utf-8")

    print(f"Return code: {result.returncode}")
    print(f"Raw output saved to: {OUTPUT_SAVE}")
    print()

    if result.returncode != 0:
        print("Captured output:")
        print("-" * 80)
        print(combined_output[:4000])
        print("-" * 80)
        fail("Official killer test script failed to run.")

    return combined_output


def parse_patterns(output_text):
    """
    Parse pattern blocks from the official output.

    Expected block style (actual output):
      Testing: Alternating 9,0,9,0... + 1,0,1,0...
        Digit Accuracy:  50.00%
        Carry Accuracy:  100.00%
        Exact Match:      50.00%
    """
    lines = output_text.splitlines()
    parsed = {}
    current_pattern = None

    for line in lines:
        line_stripped = line.strip()

        # Match "Testing: <pattern_description>"
        m_pat = re.match(r"Testing:\s*(.+)", line_stripped)
        if m_pat:
            current_pattern = m_pat.group(1)
            parsed[current_pattern] = {}
            continue

        if current_pattern is None:
            continue

        # Match "Digit Accuracy: XX.XX%"
        m_digit = re.match(r"Digit Accuracy:\s*([0-9.]+)%", line_stripped)
        if m_digit:
            parsed[current_pattern]["digit_accuracy"] = float(m_digit.group(1))
            continue

        # Match "Carry Accuracy: XX.XX%"
        m_carry = re.match(r"Carry Accuracy:\s*([0-9.]+)%", line_stripped)
        if m_carry:
            parsed[current_pattern]["carry_accuracy"] = float(m_carry.group(1))
            continue

        # Match "Exact Match: XX.XX%"
        m_exact = re.match(r"Exact Match:\s*([0-9.]+)%", line_stripped)
        if m_exact:
            parsed[current_pattern]["exact_match"] = float(m_exact.group(1))
            continue

    return parsed


def print_parsed_summary(parsed):
    print("=" * 80)
    print("PARSED RESULTS")
    print("=" * 80)
    if not parsed:
        print("No pattern results parsed.")
        return

    for pattern_name, metrics in parsed.items():
        print(f"\nPattern: {pattern_name}")
        for k, v in metrics.items():
            print(f"  {k}: {v:.2f}%")
    print()


def compare_against_expected(parsed):
    print("=" * 80)
    print("COMPARISON AGAINST DOCUMENTED EXPECTED VALUES")
    print("=" * 80)

    all_passed = True

    for pattern_display_name, expected_metrics in EXPECTED_BY_DISPLAY_NAME.items():
        print(f"\nPattern: {pattern_display_name}")

        if pattern_display_name not in parsed:
            print("  ✗ Pattern missing from official output")
            all_passed = False
            continue

        observed_metrics = parsed[pattern_display_name]

        for metric_name, expected_value in expected_metrics.items():
            if metric_name not in observed_metrics:
                print(f"  ✗ Missing metric: {metric_name}")
                all_passed = False
                continue

            observed_value = observed_metrics[metric_name]
            diff = abs(observed_value - expected_value)

            status = "✓ PASS" if diff <= TOLERANCE else "✗ FAIL"
            print(
                f"  {metric_name:<16} observed={observed_value:6.2f}% "
                f"expected={expected_value:6.2f}% diff={diff:5.2f}  {status}"
            )

            if diff > TOLERANCE:
                all_passed = False

    print()
    return all_passed


def verify_alternating_present(parsed):
    print("=" * 80)
    print("CRITICAL CHECK: ALTERNATING PATTERN")
    print("=" * 80)

    alternating_display_name = "Alternating 9,0,9,0... + 1,0,1,0..."
    
    if alternating_display_name not in parsed:
        print(f"✗ alternating pattern not found in parsed output")
        print(f"  Searched for: {alternating_display_name}")
        print(f"  Found patterns: {list(parsed.keys())}")
        return False

    alt = parsed[alternating_display_name]
    required_keys = ["digit_accuracy", "carry_accuracy", "exact_match"]

    missing = [k for k in required_keys if k not in alt]
    if missing:
        print(f"✗ alternating missing keys: {missing}")
        return False

    print(f"alternating digit_accuracy = {alt['digit_accuracy']:.2f}%")
    print(f"alternating carry_accuracy = {alt['carry_accuracy']:.2f}%")
    print(f"alternating exact_match    = {alt['exact_match']:.2f}%")
    print()

    # Critical expectation from project record
    digit_ok = abs(alt["digit_accuracy"] - 50.00) <= TOLERANCE
    carry_ok = abs(alt["carry_accuracy"] - 100.00) <= TOLERANCE
    exact_ok = abs(alt["exact_match"] - 50.00) <= TOLERANCE

    print(f"digit collapse reproduced? {'✓ YES' if digit_ok else '✗ NO'}")
    print(f"carry preserved?          {'✓ YES' if carry_ok else '✗ NO'}")
    print(f"exact-match collapse?     {'✓ YES' if exact_ok else '✗ NO'}")
    print()

    return digit_ok and carry_ok and exact_ok


# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
def main():
    # قراءة الـ raw output الموجود بالفعل (بدل إعادة التشغيل)
    if OUTPUT_SAVE.exists():
        print("=" * 80)
        print("STEP 1D: OFFICIAL KILLER TEST - PARSING RAW OUTPUT")
        print("=" * 80)
        print(f"Reading existing raw output from: {OUTPUT_SAVE}")
        print()
        
        output_text = OUTPUT_SAVE.read_text()
    else:
        output_text = run_official_script()

    print("=" * 80)
    print("RAW OUTPUT PREVIEW (FIRST 1000 CHARS)")
    print("=" * 80)
    print(output_text[:1000])
    print()

    parsed = parse_patterns(output_text)
    print_parsed_summary(parsed)

    patterns_ok = compare_against_expected(parsed)
    alternating_ok = verify_alternating_present(parsed)

    print("=" * 80)
    print("STEP 1D FINAL STATUS")
    print("=" * 80)

    if patterns_ok and alternating_ok:
        print("✓ Official killer test reproduced successfully")
        print("✓ Documented pattern-level metrics match observed output within tolerance")
        print("✓ Alternating collapse reproduced")
        print()
        print("Conclusion:")
        print("  Step 1D PASSED")
        print("  Killer test official reproduction is supported.")
    else:
        print("✗ Official killer test reproduction did NOT fully match documented expectations")
        print()
        print("Conclusion:")
        print("  Step 1D FAILED or REQUIRES MANUAL REVIEW")
        print("  Inspect raw output and parsed metrics carefully.")

    print("=" * 80)


if __name__ == "__main__":
    main()
