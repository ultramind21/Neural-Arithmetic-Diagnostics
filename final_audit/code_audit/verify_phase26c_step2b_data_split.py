"""
================================================================================
VERIFICATION SCRIPT: PHASE 26C STEP 2B
================================================================================

OFFICIAL TARGET:
  File: src/train/phase_26c_failure_audit.py

PURPOSE:
  Verify the data generation and train/test split logic of the official
  Project 1 baseline script.

THIS SCRIPT VERIFIES:
  1. Whether arithmetic pair generation logic is visible in the official source
  2. Whether train/test split logic is visible and understandable
  3. Whether the split appears to be pair-based and leakage-free
  4. Whether the claimed 70/30 split is structurally plausible
  5. Whether "held-out pairs" appear to mean genuinely unseen arithmetic pairs

THIS SCRIPT DOES NOT VERIFY:
  - Model training
  - Metric correctness
  - Final result reproduction
  - Mechanistic interpretation

IMPORTANT PRINCIPLE:
  This is a source-linked split verification step.
  If automatic extraction is insufficient, the script should still provide
  source excerpts for manual confirmation.

================================================================================
"""

import ast
from pathlib import Path


# -----------------------------------------------------------------------------
# PATHS
# -----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
TARGET_FILE = ROOT / "src" / "train" / "phase_26c_failure_audit.py"


# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------
def print_header(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_source_excerpt(file_path: Path, keywords, context=6):
    print_header(f"SOURCE EXCERPTS: {file_path.name}")

    text = file_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    found_any = False
    for kw in keywords:
        hits = [i for i, line in enumerate(lines) if kw.lower() in line.lower()]
        if hits:
            found_any = True
            print(f"\nKeyword: {kw!r}")
            for hit in hits[:5]:
                start = max(0, hit - context)
                end = min(len(lines), hit + context + 1)
                print("-" * 80)
                for idx in range(start, end):
                    marker = ">>" if idx == hit else "  "
                    print(f"{marker} {idx+1:04d}: {lines[idx]}")
                print("-" * 80)

    if not found_any:
        print("No keyword matches found.")


def parse_literal_assignments(file_text):
    """
    Attempt to recover simple literal assignments from source code using AST.
    This is best-effort only.
    """
    results = {}
    try:
        tree = ast.parse(file_text)
    except Exception:
        return results

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    name = target.id
                    try:
                        value = ast.literal_eval(node.value)
                        results[name] = value
                    except Exception:
                        pass
    return results


def inspect_for_split_indicators(file_text):
    """
    Search for strong indicators of pair generation and train/test splitting.
    """
    indicators = {
        "pair_generation": False,
        "train_test_split": False,
        "shuffle": False,
        "held_out": False,
        "explicit_70_30": False,
        "all_pairs_enumeration": False,
    }

    lower = file_text.lower()

    if "pair" in lower or "pairs" in lower:
        indicators["pair_generation"] = True
    if "train_test_split" in lower or ("train" in lower and "test" in lower and "split" in lower):
        indicators["train_test_split"] = True
    if "shuffle" in lower or "random.shuffle" in lower:
        indicators["shuffle"] = True
    if "held-out" in lower or "held_out" in lower or "unseen" in lower:
        indicators["held_out"] = True
    if "0.7" in lower or "70/30" in lower or "70%" in lower or "0.3" in lower:
        indicators["explicit_70_30"] = True
    if "for a in range(10)" in lower and "for b in range(10)" in lower:
        indicators["all_pairs_enumeration"] = True

    return indicators


def print_indicator_summary(indicators):
    print_header("STRUCTURAL INDICATORS")
    for k, v in indicators.items():
        print(f"{k:<22}: {'✓ FOUND' if v else '✗ NOT FOUND'}")


def try_reconstruct_pair_space():
    """
    Independent reference for the full single-digit pair space.
    """
    pairs = [(a, b) for a in range(10) for b in range(10)]
    print_header("INDEPENDENT REFERENCE: FULL PAIR SPACE")
    print(f"Total single-digit ordered pairs: {len(pairs)}")
    print(f"First 20 pairs: {pairs[:20]}")
    print(f"Last 10 pairs:  {pairs[-10:]}")
    print()
    print("Expected if full ordered pair space is used: 10 x 10 = 100 pairs.")
    print("Expected 70/30 split if exact: 70 train / 30 test.")


# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
def main():
    print_header("PHASE 26C STEP 2B: DATA GENERATION / SPLIT VERIFICATION")
    print(f"Official target: {TARGET_FILE}")
    print()

    if not TARGET_FILE.exists():
        print("ERROR: Official target file does not exist.")
        return

    file_text = TARGET_FILE.read_text(encoding="utf-8")

    # 1) Source excerpts for relevant sections
    print_source_excerpt(
        TARGET_FILE,
        keywords=[
            "pair",
            "pairs",
            "train",
            "test",
            "split",
            "shuffle",
            "held",
            "unseen",
            "range(10)",
            "0.7",
            "0.3",
        ],
        context=6
    )

    # 2) Literal assignment extraction (best effort)
    literals = parse_literal_assignments(file_text)
    if literals:
        print_header("RECOVERED SIMPLE LITERAL ASSIGNMENTS (BEST EFFORT)")
        for k, v in sorted(literals.items()):
            print(f"{k} = {v}")
    else:
        print_header("RECOVERED SIMPLE LITERAL ASSIGNMENTS (BEST EFFORT)")
        print("No simple literal assignments recovered.")

    # 3) Structural indicators
    indicators = inspect_for_split_indicators(file_text)
    print_indicator_summary(indicators)

    # 4) Independent reference pair space
    try_reconstruct_pair_space()

    # 5) Final assessment
    print_header("STEP 2B FINAL STATUS")
    print("This step does NOT yet prove the split is correct in execution.")
    print("It verifies whether the source visibly supports the intended interpretation.")
    print()

    print("Questions this step should help answer:")
    print("  ✓ Is the script built around arithmetic pair generation?")
    print("  ✓ Is there visible train/test split logic?")
    print("  ✓ Is there evidence for held-out pair evaluation?")
    print("  ✓ Is a 70/30 split structurally plausible from the source?")
    print()

    print("What remains open after this step:")
    print("  - whether the split is executed exactly as intended")
    print("  - whether train/test overlap actually occurs at runtime")
    print("  - whether the official result reproduces under the same split")
    print()

    print("Next recommended step:")
    print("  Step 2C — Ground-truth and target semantics verification")
    print("=" * 80)


if __name__ == "__main__":
    main()
