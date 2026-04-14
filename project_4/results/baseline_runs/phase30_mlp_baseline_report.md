# PROJECT 4 BASELINE REPORT — phase30_mlp_baseline

## Status
Aligned Phase 30 evaluation-path baseline artifact generated.

## Raw Metrics
- in_distribution: {'digit_acc': 0.4906250104540959, 'carry_acc': 0.9406250030733645, 'combined_acc': 0.48750001040752977, 'exact_match': 0.0625}
- adversarial: {'alternating_carry': {'digit_acc': 0.6000000238418579, 'carry_acc': 1.0, 'combined_acc': 0.6000000238418579, 'exact_match': 0.0}, 'full_propagation_chain': {'digit_acc': 0.6000000238418579, 'carry_acc': 1.0, 'combined_acc': 0.6000000238418579, 'exact_match': 0.0}, 'block_boundary_stress': {'digit_acc': 1.0, 'carry_acc': 1.0, 'combined_acc': 1.0, 'exact_match': 1.0}}
- lengths: {5: {'digit_acc': 0.5171875103842467, 'carry_acc': 0.9328125040046871, 'combined_acc': 0.507812510128133, 'exact_match': 0.0703125}}

## Scorecard Projection
- in_distribution_accuracy: 0.0625
- pattern_breakdown: {'alternating_carry': 0.0, 'full_propagation_chain': 0.0, 'block_boundary_stress': 1.0}
- mean_adversarial_accuracy: 0.3333333333333333
- worst_case_pattern_accuracy: 0.0
- length_summary: {'training_max_length': 5, 'tested_lengths': [5], 'accuracies': [0.0703125], 'reference_accuracy': 0.0625, 'relative_drops': [-0.125], 'trend_label': 'stable'}
- rounding_sensitivity: 0.0
- carry_corruption_summary: {'corruption_levels': [0.0, 0.1, 0.2, 0.5], 'accuracies': [0.0625, 0.0625, 0.0625, 0.0625], 'baseline_accuracy': 0.0625, 'degradation': [0.0, 0.0, 0.0, 0.0], 'trend_label': 'flat'}

## Regime Guidance
- tentative regime: Mixed / Borderline
- rationale: ['in-distribution accuracy is weak (0.0625)', 'mean adversarial accuracy is low (0.3333)', 'worst-case pattern accuracy is poor (0.0000)', "low-performing adversarial patterns detected: ['alternating_carry', 'full_propagation_chain']", 'rounding sensitivity is low (0.0000)', 'length extrapolation is stable', 'carry corruption shows flat response']
- cautions: ['carry_corruption_requires_joint_interpretation', 'final_regime_assignment_must_not_be_single_metric_based']

## Adapter Metadata
- adapter metadata: {'source_file': 'D:\\Music\\Project 03 Abacus\\soroban_project\\src\\train\\phase_30_multidigit_learning.py', 'model_type': 'mlp', 'device': 'cpu', 'import_successful': True, 'adapter_scope': 'runtime_construction_only', 'notes': ['This adapter wraps phase_30_multidigit_learning.py model classes.', 'It supports model instantiation and optional checkpoint loading.', 'It does not by itself establish a complete Project 4 evaluation path.', 'Project 4 runtime/evaluation logic must still be defined at baseline-runner level.']}

## Qualification Notes
- This baseline artifact uses the actual Phase 30 digit/carry evaluation semantics.
- Project 4 scorecard projection currently maps in-distribution and adversarial values using exact_match as the closest aligned scalar.
- Rounding sensitivity remains placeholder until an alternate aligned decode path is explicitly defined.
- Carry corruption remains placeholder until direct aligned intervention wiring is implemented.
- Final regime assignment must remain human-reviewed.

## Artifact Path
- D:\Music\Project 03 Abacus\soroban_project\project_4\results\baseline_runs\phase30_mlp_baseline_artifact.json
