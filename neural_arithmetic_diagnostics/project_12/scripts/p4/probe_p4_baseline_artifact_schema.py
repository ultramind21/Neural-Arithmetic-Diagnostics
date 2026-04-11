"""
Sprint 4B.2C.3 — Baseline Artifact Schema Probe

Purpose:
  Inspect baseline artifact structure to determine exact path for extracting
  per-family exact_match values for each adversarial family.

Output:
  Print diagnostic info to help identify where baseline stores exact_match.
"""

from pathlib import Path
import json


def probe_baseline_schema():
    """Read baseline artifact and extract schema information."""
    baseline_path = Path(
        "project_12/results/repro_p4/baselines/mlp/artifact.json"
    )
    
    # Resolve relative to workspace root
    if not baseline_path.is_absolute():
        # Try from current directory first
        root = Path(__file__).resolve().parents[3]  # neural_arithmetic_diagnostics
        baseline_path = root / baseline_path
    
    print(f"\n{'=' * 80}")
    print("BASELINE ARTIFACT SCHEMA PROBE")
    print(f"{'=' * 80}")
    print(f"\nPath: {baseline_path}")
    print(f"Exists: {baseline_path.exists()}\n")
    
    if not baseline_path.exists():
        print(f"❌ Baseline artifact not found at: {baseline_path}")
        return
    
    with open(baseline_path, "r", encoding="utf-8") as f:
        artifact = json.load(f)
    
    # ========================================================================
    # TOP-LEVEL STRUCTURE
    # ========================================================================
    print("TOP-LEVEL KEYS:")
    top_keys = list(artifact.keys())
    for i, key in enumerate(top_keys[:15], 1):
        key_type = type(artifact[key]).__name__
        print(f"  {i}. {key} ({key_type})")
    if len(top_keys) > 15:
        print(f"  ... and {len(top_keys) - 15} more")
    
    # ========================================================================
    # LOOK FOR raw_metrics
    # ========================================================================
    print("\n" + "-" * 80)
    print("SEARCHING FOR: raw_metrics (P12 format)")
    print("-" * 80)
    
    if "raw_metrics" in artifact:
        raw_metrics = artifact["raw_metrics"]
        print(f"✅ Found 'raw_metrics' at top level")
        print(f"   Type: {type(raw_metrics).__name__}")
        print(f"   Keys: {list(raw_metrics.keys())}")
        
        if "adversarial" in raw_metrics:
            adversarial = raw_metrics["adversarial"]
            print(f"\n   ✅ Found 'raw_metrics.adversarial'")
            print(f"      Families: {list(adversarial.keys())}")
            
            # Check each family for exact_match
            print(f"\n      Per-family exact_match values:")
            for family, metrics in adversarial.items():
                if isinstance(metrics, dict) and "exact_match" in metrics:
                    value = metrics["exact_match"]
                    print(f"        - {family}: {value}")
                else:
                    print(f"        - {family}: ❌ No 'exact_match' key")
        else:
            print(f"   ❌ No 'adversarial' key in raw_metrics")
            print(f"      Available: {list(raw_metrics.keys())}")
    else:
        print(f"❌ 'raw_metrics' not found at top level")
    
    # ========================================================================
    # LOOK FOR ALTERNATIVE: scorecard (alternative schema)
    # ========================================================================
    print("\n" + "-" * 80)
    print("SEARCHING FOR: scorecard (alternative source)")
    print("-" * 80)
    
    if "scorecard" in artifact:
        scorecard = artifact["scorecard"]
        print(f"✅ Found 'scorecard' at top level")
        print(f"   Keys: {list(scorecard.keys())}")
        
        if "pattern_breakdown" in scorecard:
            pattern_breakdown = scorecard["pattern_breakdown"]
            print(f"\n   ✅ Found 'scorecard.pattern_breakdown'")
            print(f"      Families and values:")
            for family, value in pattern_breakdown.items():
                print(f"        - {family}: {value}")
    else:
        print(f"❌ 'scorecard' not found at top level")
    
    # ========================================================================
    # DIAGNOSTIC SUMMARY
    # ========================================================================
    print("\n" + "=" * 80)
    print("EXTRACTION PATH RECOMMENDATIONS")
    print("=" * 80)
    
    path_found = False
    
    # Check P12 path
    if ("raw_metrics" in artifact and
        "adversarial" in artifact.get("raw_metrics", {}) and
        all(f in artifact["raw_metrics"]["adversarial"]
            for f in ["alternating_carry", "full_propagation_chain", "block_boundary_stress"])):
        
        print("\n✅ RECOMMENDED PATH (P12 Format):")
        print("   artifact['raw_metrics']['adversarial'][FAMILY]['exact_match']")
        print("\n   Code:")
        print("   ```python")
        print("   adversarial_metrics = artifact['raw_metrics']['adversarial']")
        print("   exact_match = {")
        print("       'alternating_carry': adversarial_metrics['alternating_carry']['exact_match'],")
        print("       'full_propagation_chain': adversarial_metrics['full_propagation_chain']['exact_match'],")
        print("       'block_boundary_stress': adversarial_metrics['block_boundary_stress']['exact_match'],")
        print("   }")
        print("   ```")
        path_found = True
    
    # Check scorecard path as fallback
    if (not path_found and
        "scorecard" in artifact and
        "pattern_breakdown" in artifact["scorecard"] and
        all(f in artifact["scorecard"]["pattern_breakdown"]
            for f in ["alternating_carry", "full_propagation_chain", "block_boundary_stress"])):
        
        print("\n⚠️  FALLBACK PATH (Scorecard Format):")
        print("   artifact['scorecard']['pattern_breakdown'][FAMILY]")
        print("\n   Code:")
        print("   ```python")
        print("   pattern_breakdown = artifact['scorecard']['pattern_breakdown']")
        print("   exact_match = {")
        print("       'alternating_carry': pattern_breakdown['alternating_carry'],")
        print("       'full_propagation_chain': pattern_breakdown['full_propagation_chain'],")
        print("       'block_boundary_stress': pattern_breakdown['block_boundary_stress'],")
        print("   }")
        print("   ```")
        path_found = True
    
    if not path_found:
        print("\n❌ NEITHER path found!")
        print("   Please manually inspect artifact structure above.")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    probe_baseline_schema()
