# PROJECT 4 BASELINE REPORT — phase30_lstm_baseline_run2

## Status
Aligned Phase 30 evaluation-path baseline artifact generated.

## Raw Metrics
- in_distribution: {'digit_acc': 0.44687500945292413, 'carry_acc': 0.9562500023748726, 'combined_acc': 0.44687500945292413, 'exact_match': 0.0546875}
- adversarial: {'alternating_carry': {'digit_acc': 0.6000000238418579, 'carry_acc': 1.0, 'combined_acc': 0.6000000238418579, 'exact_match': 0.0}, 'full_propagation_chain': {'digit_acc': 0.6000000238418579, 'carry_acc': 1.0, 'combined_acc': 0.6000000238418579, 'exact_match': 0.0}, 'block_boundary_stress': {'digit_acc': 0.800000011920929, 'carry_acc': 1.0, 'combined_acc': 0.800000011920929, 'exact_match': 0.0}}
- lengths: {5: {'digit_acc': 0.43437500996515155, 'carry_acc': 0.9453125030267984, 'combined_acc': 0.43437500996515155, 'exact_match': 0.03125}}

## Scorecard Projection
- in_distribution_accuracy: 0.0546875
- pattern_breakdown: {'alternating_carry': 0.0, 'full_propagation_chain': 0.0, 'block_boundary_stress': 0.0}
- mean_adversarial_accuracy: 0.0
- worst_case_pattern_accuracy: 0.0
- length_summary: {'training_max_length': 5, 'tested_lengths': [5], 'accuracies': [0.03125], 'reference_accuracy': 0.0546875, 'relative_drops': [0.42857142857142855], 'trend_label': 'sharp_collapse'}
- rounding_sensitivity: 0.0
- carry_corruption_summary: {'corruption_levels': [0.5], 'accuracies': [0.0546875], 'baseline_accuracy': 0.0546875, 'degradation': [0.0], 'trend_label': 'flat'}

## Regime Guidance
- tentative regime: Mixed / Borderline
- rationale: ['in-distribution accuracy is weak (0.0547)', 'mean adversarial accuracy is low (0.0000)', 'worst-case pattern accuracy is poor (0.0000)', "low-performing adversarial patterns detected: ['alternating_carry', 'full_propagation_chain', 'block_boundary_stress']", 'rounding sensitivity is low (0.0000)', 'length extrapolation shows sharp collapse', 'carry corruption shows flat response']
- cautions: ['carry_corruption_requires_joint_interpretation', 'final_regime_assignment_must_not_be_single_metric_based']

## Adapter Metadata
- adapter metadata: {'source_file': 'D:\\Music\\Project 03 Abacus\\soroban_project\\src\\train\\phase_30_multidigit_learning.py', 'model_type': 'lstm', 'device': 'cuda', 'import_successful': True, 'adapter_scope': 'runtime_construction_only', 'notes': ['This adapter wraps phase_30_multidigit_learning.py model classes.', 'It supports model instantiation and optional checkpoint loading.', 'It does not by itself establish a complete Project 4 evaluation path.', 'Project 4 runtime/evaluation logic must still be defined at baseline-runner level.']}

## Qualification Notes
- This baseline artifact uses the actual Phase 30 digit/carry evaluation semantics.
- Project 4 scorecard projection currently maps in-distribution and adversarial values using exact_match as the closest aligned scalar.
- Rounding sensitivity remains placeholder until an alternate aligned decode path is explicitly defined.
- Carry corruption remains placeholder until direct aligned intervention wiring is implemented.
- Final regime assignment must remain human-reviewed.

## Artifact Path
- D:\Music\Project 03 Abacus\soroban_project\project_4\results\baseline_runs\phase30_lstm_baseline_run2_artifact.json
