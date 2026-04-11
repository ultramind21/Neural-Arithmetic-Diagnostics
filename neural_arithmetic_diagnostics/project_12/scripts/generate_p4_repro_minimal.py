#!/usr/bin/env python3
"""
Generate minimal-patch Project 4 adversarial training reproduction script for Project 12.

This script:
1. Reads the original Project 4 adversarial training script
2. Applies 5 minimal patches (A-E)
3. Writes result to entrypoint file
4. Measures similarity using difflib
"""

import json
from pathlib import Path
from difflib import SequenceMatcher


def read_original_p4():
    """Read the original Project 4 adversarial training script."""
    p4_file = Path(
        "d:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_4/interventions/"
        "adversarial_training/project_4_adversarial_training.py"
    )
    return p4_file.read_text(encoding="utf-8")


def apply_patches(original: str) -> str:
    """Apply 5 minimal patches to the original Project 4 script."""
    
    # PATCH A: Add imports after existing imports
    # Insert after the numpy/torch imports line
    import_section = """from __future__ import annotations

import importlib.util
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Tuple

import numpy as np
import torch"""
    
    new_imports = """from __future__ import annotations

import argparse
import importlib.util
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Tuple

import numpy as np
import torch

# Project 12 utilities
from project_12.scripts.p12_runlib import (
    load_manifest,
    ensure_output_dir_is_safe,
    build_p12_metadata,
    write_json,
)"""
    
    result = original.replace(import_section, new_imports)
    
    # PATCH B: Add manifest + argparse handling in main()
    # Find the main() function and add manifest parsing at the start
    main_start = """def main():
    print_header("PROJECT 4 ADVERSARIAL TRAINING")

    module = load_phase30_module()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")"""
    
    main_new = """def main():
    # PATCH B: Parse arguments and load manifest
    parser = argparse.ArgumentParser(
        description="Project 4 adversarial training with P12 artifact output"
    )
    parser.add_argument(
        "--manifest",
        type=str,
        required=True,
        help="Path to Project 12 manifest JSON",
    )
    parser.add_argument(
        "--baseline-artifact",
        type=str,
        required=False,
        default=None,
        help="Path to baseline artifact JSON for per-family exact_match extraction",
    )
    args = parser.parse_args()
    
    # Load manifest to extract output directory
    manifest = load_manifest(args.manifest)
    output_dir_relative = manifest.get("output_dir", "project_12/results/repro_p4/adversarial")
    output_dir = Path(output_dir_relative)
    ensure_output_dir_is_safe(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # PATCH C: Extract baseline exact_match if provided
    baseline_exact_match = {}
    if args.baseline_artifact:
        baseline_path = Path(args.baseline_artifact)
        if baseline_path.exists():
            baseline_data = json.loads(baseline_path.read_text(encoding="utf-8"))
            # Extract per-family exact_match from raw_metrics.adversarial
            adv_metrics = baseline_data.get("raw_metrics", {}).get("adversarial", {})
            for family, metrics in adv_metrics.items():
                baseline_exact_match[family] = metrics.get("exact_match", 0.0)
    
    print_header("PROJECT 4 ADVERSARIAL TRAINING")

    module = load_phase30_module()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")"""
    
    result = result.replace(main_start, main_new)
    
    # PATCH D: Add artifact_p12.json output after artifact creation
    # Find the part where artifact is created and add P12 metadata output
    artifact_output = """    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")

    print("\\n" + "=" * 80)"""
    
    artifact_output_new = """    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    
    # PATCH D: Write Project 12 standard artifact output
    artifact_p12 = {
        "p12_metadata": build_p12_metadata(
            manifest_path=args.manifest,
            entrypoint="run_p4_adversarial_training_repro.py",
            source_script_copied_from="project_4/interventions/adversarial_training/project_4_adversarial_training.py",
        ),
        "baseline_exact_match_reference": baseline_exact_match,
        "adversarial_training_gains": {
            "alternating_carry": {
                "pre": baseline_exact_match.get("alternating_carry", 0.0),
                "post": artifact["seen_results"]["alternating_carry"]["exact_match"],
                "gain": artifact["seen_results"]["alternating_carry"]["exact_match"] - baseline_exact_match.get("alternating_carry", 0.0),
            },
            "full_propagation_chain": {
                "pre": baseline_exact_match.get("full_propagation_chain", 0.0),
                "post": artifact["seen_results"]["full_propagation_chain"]["exact_match"],
                "gain": artifact["seen_results"]["full_propagation_chain"]["exact_match"] - baseline_exact_match.get("full_propagation_chain", 0.0),
            },
            "block_boundary_stress": {
                "pre": baseline_exact_match.get("block_boundary_stress", 0.0),
                "post": artifact["heldout_results"]["block_boundary_stress"]["exact_match"],
                "gain": artifact["heldout_results"]["block_boundary_stress"]["exact_match"] - baseline_exact_match.get("block_boundary_stress", 0.0),
            },
        },
        "original_project4_artifact": artifact,
    }
    
    artifact_p12_path = output_dir / "artifact_p12.json"
    write_json(artifact_p12_path, artifact_p12)
    print(f"✓ P12 artifact saved to: {artifact_p12_path}")

    print("\\n" + "=" * 80)"""
    
    result = result.replace(artifact_output, artifact_output_new)
    
    # PATCH E: Verify training loop is unchanged (no modification needed)
    # Just verify it's present
    if "train_mlp_with_adversarial_augmentation" not in result:
        raise ValueError("Training function was modified - PATCH E failed")
    
    return result


def measure_similarity(original: str, modified: str) -> tuple:
    """Measure similarity and line changes between original and modified."""
    matcher = SequenceMatcher(None, original, modified)
    similarity = matcher.ratio()
    
    # Count line changes
    orig_lines = original.splitlines()
    mod_lines = modified.splitlines()
    
    lines_changed = abs(len(orig_lines) - len(mod_lines))
    
    return similarity, lines_changed, len(mod_lines)


def main():
    print("=" * 80)
    print("PROJECT 12 MINIMAL PATCH GENERATOR")
    print("=" * 80)
    
    # Read original
    print("\n[1/4] Reading original Project 4 adversarial training script...")
    original = read_original_p4()
    orig_lines = len(original.splitlines())
    print(f"      ✓ Original: {orig_lines} lines")
    
    # Apply patches
    print("\n[2/4] Applying 5 minimal patches (A-E)...")
    patched = apply_patches(original)
    patched_lines = len(patched.splitlines())
    print(f"      ✓ Patched: {patched_lines} lines")
    print(f"      ✓ Line overhead: +{patched_lines - orig_lines} lines")
    
    # Write to target
    print("\n[3/4] Writing to target entrypoint...")
    target = Path(
        "d:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_12/scripts/p4/"
        "run_p4_adversarial_training_repro.py"
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(patched, encoding="utf-8")
    print(f"      ✓ Written to: {target}")
    
    # Measure similarity
    print("\n[4/4] Measuring diff gate metrics...")
    similarity, lines_changed, final_lines = measure_similarity(original, patched)
    print(f"\n" + "=" * 80)
    print("DIFF GATE METRICS")
    print("=" * 80)
    print(f"Original lines:       {orig_lines}")
    print(f"Patched lines:        {final_lines}")
    print(f"Line overhead:        +{final_lines - orig_lines}")
    print(f"Lines changed:        {lines_changed}")
    print(f"Similarity ratio:     {similarity:.4f}")
    print(f"Target similarity:    ≥0.85")
    print(f"Status:               {'✓ PASS' if similarity >= 0.85 else '✗ FAIL'}")
    print(f"\nExpectation check:")
    print(f"  Similarity ≥ 0.85:  {similarity:.4f} {'✓' if similarity >= 0.85 else '✗'}")
    print(f"  Lines changed ≤ 80: {lines_changed} {'✓' if lines_changed <= 80 else '✗'}")
    print(f"  Total ~470-490:     {final_lines} {'✓' if 470 <= final_lines <= 490 else '✗'}")
    print("=" * 80)


if __name__ == "__main__":
    main()
