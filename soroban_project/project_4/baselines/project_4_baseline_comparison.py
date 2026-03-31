"""
================================================================================
PROJECT 4 BASELINE COMPARISON
================================================================================

PURPOSE:
  Project 4 baseline comparison runner.

ROLE:
  This script now supports a hybrid execution model:
    - real adapter-backed entries where runtime integration exists
    - demo/scaffold entries where adapters are still pending

IMPORTANT:
  Current Project 4 baseline comparison is still v1.0.
  This means:
    - framework integration is real
    - scorecard generation is real
    - adversarial benchmark integration is real
    - phase30 runtime adapter is connected
    - full scientific baseline evaluation is still partial and adapter-dependent

CRITICAL WARNING:
  Any entry not backed by a real adapter path must remain labeled as
  DEMO / SCAFFOLD ONLY.
  Only adapter-backed entries may be treated as operational runtime outputs.

================================================================================
"""

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Any, List, Optional
import json
import sys
import torch


# ============================================================================
# PATHS
# ============================================================================
PROJECT_4_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PROJECT_4_ROOT.parents[1]

FRAMEWORK_ROOT = PROJECT_4_ROOT / "framework"
DIAGNOSTICS_ROOT = PROJECT_4_ROOT / "diagnostics"
BASELINES_ROOT = PROJECT_4_ROOT / "baselines"

OUTPUT_JSON = BASELINES_ROOT / "project_4_baseline_comparison_output.json"


# Make modules importable
sys.path.insert(0, str(PROJECT_4_ROOT))
sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================================
# IMPORTS FROM PROJECT 4
# ============================================================================
from diagnostics.diagnostic_scorecard import (
    build_scorecard,
    scorecard_to_dict,
)
from diagnostics.benchmark_adversarial_patterns import (
    generate_project4_adversarial_patterns,
)
from diagnostics.regime_classification import (
    classify_regime,
)
from baselines.project_4_baseline_runtime_adapter_phase30 import (
    build_phase30_adapter,
)


# ============================================================================
# DATA CLASS
# ============================================================================
@dataclass
class BaselineSpec:
    name: str
    source_file: str
    adapter_family: str
    adapter_key: Optional[str]
    status: str
    notes: str


# ============================================================================
# HELPERS
# ============================================================================

def print_header(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def save_json(path: Path, obj: Dict[str, Any]):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def build_baseline_registry() -> List[BaselineSpec]:
    """
    v1.0 baseline registry.

    phase30-backed entries are now adapter-capable.
    residual remains scaffold-only until a separate adapter is introduced.
    """
    return [
        BaselineSpec(
            name="MLP_baseline_reference",
            source_file="src/train/phase_30_multidigit_learning.py",
            adapter_family="phase30",
            adapter_key="mlp",
            status="adapter_connected_runtime_only",
            notes="Phase 30 MLP adapter connected; scientific evaluation path still partial",
        ),
        BaselineSpec(
            name="LSTM_baseline_reference",
            source_file="src/train/phase_30_multidigit_learning.py",
            adapter_family="phase30",
            adapter_key="lstm",
            status="adapter_connected_runtime_only",
            notes="Phase 30 LSTM adapter connected; scientific evaluation path still partial",
        ),
        BaselineSpec(
            name="Transformer_baseline_reference",
            source_file="src/train/phase_30_multidigit_learning.py",
            adapter_family="phase30",
            adapter_key="transformer",
            status="adapter_connected_runtime_only",
            notes="Phase 30 Transformer adapter connected; scientific evaluation path still partial",
        ),
        BaselineSpec(
            name="Residual_baseline_reference",
            source_file="src/train/project_3_residual_logic_layer.py",
            adapter_family="none",
            adapter_key=None,
            status="pending_adapter",
            notes="Residual baseline remains scaffold-only until dedicated adapter is implemented",
        ),
    ]


def build_demo_scorecard_for_registry_entry(spec: BaselineSpec) -> Dict[str, Any]:
    """
    v1.0 placeholder/demo scorecard.

    IMPORTANT:
      This is NOT a scientific baseline result.
      It is only a pipeline/demo object used to validate framework wiring.
    """
    demo_pattern_breakdown = {
        "alternating_carry": 0.52,
        "full_propagation_chain": 0.95,
        "block_boundary_stress": 0.61,
    }

    scorecard = build_scorecard(
        model_name=spec.name,
        in_distribution_accuracy=0.98,
        pattern_breakdown=demo_pattern_breakdown,
        training_max_length=5,
        accuracy_by_length={
            5: 0.98,
            10: 0.95,
            20: 0.88,
            50: 0.62,
        },
        accuracy_with_rounding=0.98,
        accuracy_without_rounding=0.61,
        accuracy_by_corruption={
            0.0: 0.98,
            0.1: 0.86,
            0.2: 0.73,
            0.5: 0.42,
        },
        notes=[
            "demo scorecard only",
            "adapter not yet connected to official runtime path",
            "not valid for scientific interpretation",
        ],
        tags=["demo", "v1.0", "pending_adapter", "not_scientific_result"],
    )

    guidance = classify_regime(scorecard_to_dict(scorecard))

    return {
        "scientific_result_status": "DEMO_ONLY_NOT_FOR_SCIENTIFIC_USE",
        "baseline_spec": asdict(spec),
        "scorecard": scorecard_to_dict(scorecard),
        "regime_guidance": guidance,
    }


def framework_artifact_check() -> bool:
    required_files = [
        FRAMEWORK_ROOT / "FRAMEWORK_CHANGELOG.md",
        PROJECT_4_ROOT / "validation" / "RESULT_VALIDATION_PROTOCOL.md",
        DIAGNOSTICS_ROOT / "diagnostic_scorecard.py",
        DIAGNOSTICS_ROOT / "benchmark_adversarial_patterns.py",
        DIAGNOSTICS_ROOT / "regime_classification.py",
        BASELINES_ROOT / "PROJECT_4_BASELINE_RESULTS.md",
        BASELINES_ROOT / "project_4_baseline_runtime_adapter_phase30.py",
    ]

    ok = True
    for path in required_files:
        if path.exists():
            print(f"✓ Found: {path.relative_to(PROJECT_ROOT)}")
        else:
            ok = False
            print(f"✗ Missing: {path.relative_to(PROJECT_ROOT)}")
    return ok


def build_demo_scorecard(spec: BaselineSpec) -> Dict[str, Any]:
    demo_pattern_breakdown = {
        "alternating_carry": 0.52,
        "full_propagation_chain": 0.95,
        "block_boundary_stress": 0.61,
    }

    scorecard = build_scorecard(
        model_name=spec.name,
        in_distribution_accuracy=0.98,
        pattern_breakdown=demo_pattern_breakdown,
        training_max_length=5,
        accuracy_by_length={
            5: 0.98,
            10: 0.95,
            20: 0.88,
            50: 0.62,
        },
        accuracy_with_rounding=0.98,
        accuracy_without_rounding=0.61,
        accuracy_by_corruption={
            0.0: 0.98,
            0.1: 0.86,
            0.2: 0.73,
            0.5: 0.42,
        },
        notes=[
            "demo scorecard only",
            "adapter not yet connected to official runtime path",
            "not valid for scientific interpretation",
        ],
        tags=["demo", "v1.0", "pending_adapter", "not_scientific_result"],
    )

    guidance = classify_regime(scorecard_to_dict(scorecard))

    return {
        "scientific_result_status": "DEMO_ONLY_NOT_FOR_SCIENTIFIC_USE",
        "baseline_spec": asdict(spec),
        "scorecard": scorecard_to_dict(scorecard),
        "regime_guidance": guidance,
    }


def build_runtime_placeholder_scorecard(spec: BaselineSpec, adapter_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Runtime-backed placeholder.

    This confirms adapter construction and framework wiring,
    but does NOT yet claim scientific baseline metrics.
    """
    scorecard = build_scorecard(
        model_name=spec.name,
        in_distribution_accuracy=None,
        pattern_breakdown={},
        training_max_length=None,
        accuracy_by_length=None,
        accuracy_with_rounding=None,
        accuracy_without_rounding=None,
        accuracy_by_corruption=None,
        notes=[
            "runtime adapter connected successfully",
            "scientific baseline metrics not yet executed in this stage",
            "adapter-backed runtime object available",
        ],
        tags=["runtime_connected", "v1.0", "partial_execution", "not_final_scientific_result"],
    )

    guidance = classify_regime(scorecard_to_dict(scorecard))

    return {
        "scientific_result_status": "RUNTIME_CONNECTED_NOT_YET_SCIENTIFIC_BASELINE",
        "baseline_spec": asdict(spec),
        "adapter_metadata": adapter_metadata,
        "scorecard": scorecard_to_dict(scorecard),
        "regime_guidance": guidance,
    }


def connect_runtime_if_available(spec: BaselineSpec, device: torch.device) -> Dict[str, Any]:
    if spec.adapter_family == "phase30" and spec.adapter_key is not None:
        adapter = build_phase30_adapter(
            model_type=spec.adapter_key,
            checkpoint_path=None,
            device=device,
        )
        return build_runtime_placeholder_scorecard(spec, adapter.metadata())

    return build_demo_scorecard(spec)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 4 BASELINE COMPARISON — v1.0 HYBRID RUNNER")

    # ------------------------------------------------------------------------
    # 1) Framework artifact check
    # ------------------------------------------------------------------------
    print_header("1) FRAMEWORK ARTIFACT CHECK")
    framework_ok = framework_artifact_check()

    # ------------------------------------------------------------------------
    # 2) Registry
    # ------------------------------------------------------------------------
    print_header("2) BASELINE REGISTRY")
    registry = build_baseline_registry()
    for spec in registry:
        print(f"- {spec.name}")
        print(f"  source_file:    {spec.source_file}")
        print(f"  adapter_family: {spec.adapter_family}")
        print(f"  adapter_key:    {spec.adapter_key}")
        print(f"  status:         {spec.status}")
        print(f"  notes:          {spec.notes}")

    # ------------------------------------------------------------------------
    # 3) Pattern availability
    # ------------------------------------------------------------------------
    print_header("3) ADVERSARIAL BENCHMARK AVAILABILITY")
    patterns = generate_project4_adversarial_patterns(length=20, num_samples=4)
    print(f"✓ Loaded {len(patterns)} Project 4 adversarial patterns")
    for name, pattern in patterns.items():
        print(f"  - {name}: length={pattern.length}, samples={pattern.num_samples}")

    # ------------------------------------------------------------------------
    # 4) Hybrid scorecard generation
    # ------------------------------------------------------------------------
    print_header("4) BASELINE ENTRY GENERATION")
    device = torch.device("cpu")
    results = {}

    for spec in registry:
        try:
            record = connect_runtime_if_available(spec, device=device)
            results[spec.name] = record
            print(f"✓ Built entry for {spec.name}")
            print(f"  scientific_result_status: {record['scientific_result_status']}")
        except Exception as e:
            results[spec.name] = {
                "scientific_result_status": "RUNTIME_CONNECTION_FAILED",
                "baseline_spec": asdict(spec),
                "error": str(e),
            }
            print(f"✗ Failed entry for {spec.name}")
            print(f"  error: {e}")

    # ------------------------------------------------------------------------
    # 5) Save output package
    # ------------------------------------------------------------------------
    print_header("5) SAVE OUTPUT PACKAGE")
    output_obj = {
        "scientific_result_status": "HYBRID_SCAFFOLD_RUNTIME_PACKAGE_NOT_FINAL_BASELINE_RESULT",
        "status": "v1.0 hybrid runner active",
        "framework_ok": framework_ok,
        "baseline_count": len(registry),
        "pattern_count": len(patterns),
        "results": results,
        "notes": [
            "This output is not yet a final scientific baseline result package.",
            "Phase30-backed entries may confirm runtime adapter connectivity only.",
            "Residual entry remains scaffold-only pending dedicated adapter.",
            "Final scientific baseline evaluation still requires explicit evaluation execution paths.",
        ],
    }

    save_json(OUTPUT_JSON, output_obj)
    print(f"✓ Saved output to: {OUTPUT_JSON}")

    # ------------------------------------------------------------------------
    # 6) Final decision
    # ------------------------------------------------------------------------
    print_header("6) FINAL STATUS")

    runtime_connected = [
        k for k, v in results.items()
        if v.get("scientific_result_status") == "RUNTIME_CONNECTED_NOT_YET_SCIENTIFIC_BASELINE"
    ]

    demo_only = [
        k for k, v in results.items()
        if v.get("scientific_result_status") == "DEMO_ONLY_NOT_FOR_SCIENTIFIC_USE"
    ]

    failed = [
        k for k, v in results.items()
        if v.get("scientific_result_status") == "RUNTIME_CONNECTION_FAILED"
    ]

    if framework_ok:
        print("✓ PASS")
        print()
        print("Finding:")
        print("  Project 4 baseline comparison has progressed from pure scaffold")
        print("  to a hybrid runner with real runtime adapter connectivity for")
        print("  Phase 30-backed baselines.")
        print()
        print(f"Runtime-connected entries: {runtime_connected}")
        print(f"Demo-only entries:         {demo_only}")
        print(f"Failed connections:        {failed}")
        print()
        print("Critical warning:")
        print("  Current outputs are still NOT final scientific baseline results.")
        print("  Runtime connectivity is now established for some entries, but")
        print("  evaluation execution paths remain to be implemented.")
    else:
        print("⚠ PARTIAL")
        print()
        print("Finding:")
        print("  Hybrid runner exists, but some framework dependencies are missing.")

    print()
    print("Next recommended step:")
    print("  Implement the first real baseline evaluation execution path")
    print("  for one adapter-backed model (recommended: MLP from Phase 30)")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()   