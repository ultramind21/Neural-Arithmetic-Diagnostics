"""
================================================================================
VERIFICATION SCRIPT: PHASE 26C STEP 2E
================================================================================

OFFICIAL TARGET:
  File: src/train/phase_26c_failure_audit.py

PURPOSE:
  Reproduce the official Project 1 baseline script and capture its reported result.

THIS SCRIPT VERIFIES:
  1. The official Phase 26c script runs successfully
  2. Raw stdout/stderr can be captured and archived
  3. Key reported metrics can be extracted from output
  4. The script's reported baseline result can be compared to documented expectations

THIS SCRIPT DOES NOT VERIFY:
  - Why the result occurs
  - Deep model mechanism
  - Whether every interpretation in Project 1 closure is fully justified
  - Any broader claim beyond direct reproduction

IMPORTANT PRINCIPLE:
  This is official-result reproduction only.
  Interpretation comes only after successful reproduction.

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
TARGET_FILE = ROOT / "src" / "train" / "phase_26c_failure_audit.py"
RAW_OUTPUT_FILE = ROOT / "final_audit" / "code_audit" / "step2e_phase26c_raw_output.txt"


# -----------------------------------------------------------------------------
# EXPECTED DOCUMENTED VALUES (INITIAL WORKING REFERENCE)
# -----------------------------------------------------------------------------
# These should be updated if the official documentation gives more precise
# or differently named outputs.
#
# Project 1 accepted baseline range from closure docs:
#   MLP held-out pair ≈ 61–73%
#
# Since exact printed output from phase_26c_failure_audit.py may differ in naming,
# this script uses conservative matching and reports what it finds.
EXPECTED_HELD_OUT_RANGE = (60.0, 75.0)


# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------
def fail(msg):
    print(f"\nERROR: {msg}")
    sys.exit(1)


def print_header(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def run_official_script():
    if not TARGET_FILE.exists():
        fail(f"Official target file not found: {TARGET_FILE}")

    print_header("STEP 2E: OFFICIAL PHASE 26C REPRODUCTION")
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

    RAW_OUTPUT_FILE.write_text(combined_output, encoding="utf-8")

    print(f"Return code: {result.returncode}")
    print(f"Raw output saved to: {RAW_OUTPUT_FILE}")
    print()

    if result.returncode != 0:
        print("Captured output preview:")
        print("-" * 80)
        print(combined_output[:4000])
        print("-" * 80)
        fail("Official Phase 26c script failed to run.")

    return combined_output


def preview_output(text, max_chars=2000):
    print_header(f"RAW OUTPUT PREVIEW (FIRST {max_chars} CHARS)")
    print(text[:max_chars])


def parse_candidate_metrics(text):
    """
    Best-effort extraction of likely accuracy values.

    Because output formatting may vary, this parser searches for broad accuracy-like
    lines and stores them for review rather than assuming one exact format.
    """
    parsed = []

    # Catch generic percentage lines
    patterns = [
        r"([A-Za-z0-9_\-\s()]+Accuracy[A-Za-z0-9_\-\s()]*):\s*([0-9.]+)%",
        r"([A-Za-z0-9_\-\s()]+accuracy[A-Za-z0-9_\-\s()]*):\s*([0-9.]+)%",
        r"([A-Za-z0-9_\-\s()]+Held[- ]?[Oo]ut[A-Za-z0-9_\-\s()]*):\s*([0-9.]+)%",
        r"([A-Za-z0-9_\-\s()]+Test[A-Za-z0-9_\-\s()]*):\s*([0-9.]+)%",
        r"([A-Za-z0-9_\-\s()]+Train[A-Za-z0-9_\-\s()]*):\s*([0-9.]+)%",
    ]

    lines = text.splitlines()
    for line in lines:
        line_stripped = line.strip()
        for pat in patterns:
            m = re.match(pat, line_stripped)
            if m:
                label = m.group(1).strip()
                value = float(m.group(2))
                parsed.append((label, value))
                break

    return parsed


def print_parsed_metrics(parsed):
    print_header("PARSED CANDIDATE METRICS")
    if not parsed:
        print("No candidate metrics parsed.")
        return

    for label, value in parsed:
        print(f"{label}: {value:.2f}%")


def infer_held_out_candidates(parsed):
    """
    Return all parsed metrics whose labels look like held-out or test generalization.
    """
    candidates = []
    for label, value in parsed:
        lower = label.lower()
        if "held" in lower or "unseen" in lower or "test" in lower:
            candidates.append((label, value))
    return candidates


def evaluate_against_documentation(held_out_candidates):
    print_header("DOCUMENTATION CONSISTENCY CHECK (INITIAL)")
    print(f"Expected held-out baseline range from Project 1 closure: {EXPECTED_HELD_OUT_RANGE[0]:.1f}% to {EXPECTED_HELD_OUT_RANGE[1]:.1f}%")
    print()

    if not held_out_candidates:
        print("No held-out/test-like metric was automatically identified.")
        print("Manual review of raw output is required.")
        return False

    matched_any = False
    for label, value in held_out_candidates:
        in_range = EXPECTED_HELD_OUT_RANGE[0] <= value <= EXPECTED_HELD_OUT_RANGE[1]
        status = "✓ IN RANGE" if in_range else "⚠ OUTSIDE RANGE"
        print(f"{label}: {value:.2f}%  -> {status}")
        if in_range:
            matched_any = True

    print()
    return matched_any


# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
def main():
    output_text = run_official_script()
    preview_output(output_text, max_chars=2000)

    parsed = parse_candidate_metrics(output_text)
    print_parsed_metrics(parsed)

    held_out_candidates = infer_held_out_candidates(parsed)
    matched = evaluate_against_documentation(held_out_candidates)

    print_header("STEP 2E FINAL STATUS")
    print("What this step establishes:")
    print("  ✓ Whether the official Phase 26c script runs successfully")
    print("  ✓ Whether raw output is captured and archived")
    print("  ✓ Whether candidate reported metrics can be extracted")
    print()

    if matched:
        print("Initial reproduction status: ✓ PASS (at least one held-out/test metric matches the documented baseline range)")
    else:
        print("Initial reproduction status: ⚠ MANUAL REVIEW REQUIRED")
        print("This does NOT necessarily mean the script is wrong.")
        print("It may mean the output labels differ from parser assumptions.")

    print()
    print("Important:")
    print("  - This step is reproduction only, not interpretation.")
    print("  - If parser assumptions are incomplete, inspect the raw output directly.")
    print("  - Use the raw output file as the authoritative reproduction artifact.")
    print()

    print("Next recommended step:")
    print("  Step 2F — Behavioral error structure (only after reproduction is understood)")
    print("=" * 80)


if __name__ == "__main__":
    main()
