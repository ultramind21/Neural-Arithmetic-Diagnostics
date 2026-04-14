"""
================================================================================
VERIFICATION SCRIPT: PHASE 27C STEP 3B
================================================================================

OFFICIAL TARGET:
  File: src/train/phase_27c_architecture_audit.py

PURPOSE:
  Verify Project 2 (Phase 27c) data split and generation logic.

CRITICAL QUESTION FOR THIS STEP:
  How are the 30 test pairs generated/selected?
  Are they fair and consistent across architectures?

THIS SCRIPT VERIFIES:
  1. What is the total pair pool being used?
  2. How are the 30 test pairs selected (random? fixed? seeded?)?
  3. Is the train/test split logic visible and auditable?
  4. Are the SAME test pairs used for all architectures (MLP, LSTM, Transformer)?
  5. Is the split/selection logic deterministic (reproducible)?
  6. Are there any signs of data leakage or unfair comparisons?
  7. How does "30 pairs only" affect comparability vs other projects?

THIS SCRIPT DOES NOT VERIFY:
  - Whether ground truth semantics are correct (that comes later in 3C)
  - Whether metrics are computed correctly (that comes later in 3D)
  - Whether results are correct (that comes later in 3E)
  - Full trial execution (that comes later in 3E)

IMPORTANT PRINCIPLE:
  This is structural verification of fairness and transparency.
  We read the code, extract logic, and verify consistency claims.
  No execution of model training - only data generation logic inspection.

================================================================================
"""

import re
import sys
from pathlib import Path


# ============================================================================
# PATHS
# ============================================================================
ROOT = Path(__file__).resolve().parents[2]
TARGET_FILE = ROOT / "src" / "train" / "phase_27c_architecture_audit.py"


# ============================================================================
# HELPERS
# ============================================================================
def fail(msg):
    print(f"\nERROR: {msg}")
    sys.exit(1)


def print_header(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def read_file_with_line_numbers(filepath):
    """Read file and return list of (line_number, content) tuples."""
    lines = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                lines.append((i, line.rstrip('\n')))
    except Exception as e:
        fail(f"Cannot read file: {e}")
    return lines


def extract_function_body(lines, func_name):
    """
    Extract the full body of a function from the lines.
    Returns: (start_line, end_line, full_body_text)
    """
    func_start = None
    for i, (line_num, content) in enumerate(lines):
        if f"def {func_name}" in content:
            func_start = i
            break
    
    if func_start is None:
        return None
    
    # Find the end (next function or class definition at same indentation level)
    func_indent = len(lines[func_start][1]) - len(lines[func_start][1].lstrip())
    func_end = len(lines)
    
    for i in range(func_start + 1, len(lines)):
        line_num, content = lines[i]
        if content.strip() == "":
            continue
        current_indent = len(content) - len(content.lstrip())
        if current_indent <= func_indent and content.strip():
            func_end = i
            break
    
    body = '\n'.join(f"{lines[j][0]:05d}: {lines[j][1]}" 
                     for j in range(func_start, func_end))
    return (lines[func_start][0], lines[func_end - 1][0], body)


def extract_imports_and_seeds(lines):
    """Extract import statements and seed settings."""
    results = {
        'imports': [],
        'seeds': [],
        'torch_seed': None,
        'np_seed': None
    }
    
    for line_num, content in lines[:50]:  # Check first 50 lines
        if content.strip().startswith('import '):
            results['imports'].append((line_num, content.strip()))
        elif 'seed' in content.lower():
            results['seeds'].append((line_num, content.strip()))
            if 'torch.manual_seed' in content:
                match = re.search(r'torch\.manual_seed\((\d+)\)', content)
                if match:
                    results['torch_seed'] = int(match.group(1))
            elif 'np.random.seed' in content:
                match = re.search(r'np\.random\.seed\((\d+)\)', content)
                if match:
                    results['np_seed'] = int(match.group(1))
    
    return results


def find_pair_reference(lines):
    """Find references to pair creation/selection."""
    refs = []
    for line_num, content in lines:
        if any(keyword in content.lower() for keyword in 
               ['pair', '30', 'test_pair', 'all_pair', 'range(', 'sample']):
            refs.append((line_num, content.strip()))
    return refs


# ============================================================================
# MAIN
# ============================================================================
def main():
    print_header("PHASE 27C STEP 3B: DATA SPLIT / GENERATION VERIFICATION")
    print(f"Official target: {TARGET_FILE}")
    print()

    if not TARGET_FILE.exists():
        fail(f"Official target file not found: {TARGET_FILE}")
    
    lines = read_file_with_line_numbers(TARGET_FILE)
    
    # Extract seeds
    print_header("REPRODUCIBILITY: SEEDS & RANDOMNESS")
    print()
    
    seeds = extract_imports_and_seeds(lines)
    
    if seeds['torch_seed'] is not None:
        print(f"✓ torch.manual_seed({seeds['torch_seed']}) found")
    else:
        print("⚠️  torch.manual_seed not found or not clearly set")
    
    if seeds['np_seed'] is not None:
        print(f"✓ np.random.seed({seeds['np_seed']}) found")
    else:
        print("⚠️  np.random.seed not found or not clearly set")
    
    print()
    
    # Now extract data generation functions
    print_header("DATA GENERATION FUNCTIONS")
    print()
    
    # Extract create_train_data
    result = extract_function_body(lines, "create_train_data")
    if result:
        start, end, body = result
        print(f"create_train_data (lines {start}-{end}):")
        print("-" * 80)
        print(body)
        print()
    else:
        print("⚠️  create_train_data function not found")
        print()
    
    # Extract create_test_data_simple
    result = extract_function_body(lines, "create_test_data_simple")
    if result:
        start, end, body = result
        print(f"create_test_data_simple (lines {start}-{end}):")
        print("-" * 80)
        print(body)
        print()
    else:
        print("⚠️  create_test_data_simple function not found")
        print()
    
    # Find pair references
    print_header("PAIR GENERATION & SELECTION CLUES")
    print()
    
    pair_refs = find_pair_reference(lines)
    
    print("Key references to 'pair' / '30' / 'sample' / number iteration:")
    print()
    
    for line_num, content in pair_refs[:15]:
        print(f"  {line_num:04d}: {content}")
    
    if len(pair_refs) > 15:
        print(f"  ... and {len(pair_refs) - 15} more")
    
    print()
    
    # Find run_trial function to see evaluation logic
    print_header("TRIAL EXECUTION & EVALUATION LOGIC")
    print()
    
    result = extract_function_body(lines, "run_trial")
    if result:
        start, end, body = result
        print(f"run_trial (lines {start}-{end}):")
        print("-" * 80)
        print(body)
        print()
    else:
        print("⚠️  run_trial function not found")
        print()
    
    # Analysis questions
    print_header("CRITICAL VERIFICATION QUESTIONS")
    print()
    
    questions = [
        ("Q1", "Are the 30 test pairs fixed and deterministic?", 
         "Look for: fixed pair list, seeded random generation, or explicit enumeration"),
        
        ("Q2", "Are the SAME 30 test pairs used by all architectures (MLP, LSTM, Transformer)?",
         "Look for: shared test_pairs variable, or regeneration at each architecture"),
        
        ("Q3", "Is the train/test split logic visible and auditable?",
         "Look for: explicit data split, separation of train/test generation"),
        
        ("Q4", "Is there any chance of data leakage (train pairs appearing in test)?",
         "Look for: disjoint set operations, or independent generation"),
        
        ("Q5", "How does the 30-pair setup compare to baseline expectations?",
         "Context: this is MUCH smaller than Phase 1 baseline (100 pairs)"),
        
        ("Q6", "Is there explicit documentation of 'trial' semantics?",
         "Look for: comments about what variations across trials, reproducibility"),
    ]
    
    for q_id, question, guidance in questions:
        print(f"{q_id}: {question}")
        print(f"    Hint: {guidance}")
        print()
    
    # Summary
    print_header("STEP 3B VERIFICATION CHECKLIST")
    print()
    
    checks = [
        ("Deterministic seeding", seeds['torch_seed'] is not None and seeds['np_seed'] is not None),
        ("Data generation functions exist", result is not None),
        ("Pair references visible in code", len(pair_refs) > 0),
    ]
    
    for check_name, success in checks:
        status = "✓" if success else "⚠️"
        print(f"  {status} {check_name}")
    
    print()
    print("=" * 80)
    print("STEP 3B ASSESSMENT")
    print("=" * 80)
    print()
    print("What this step can confirm:")
    print("  - Whether data generation is deterministic (seeded)")
    print("  - whether pair generation logic is visible and understandable")
    print("  - Whether train/test split protocol is fair and transparent")
    print("  - Whether 30-pair constraint affects reproducibility/fairness")
    print()
    print("What remains open after this step:")
    print("  - Whether generated pairs are actually correct (comes in 3C)")
    print("  - Whether metrics are correctly computed (comes in 3D)")
    print("  - Whether reproduction results are correct (comes in 3E)")
    print("  - Whether behavioral patterns are meaningful (comes in 3F)")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
