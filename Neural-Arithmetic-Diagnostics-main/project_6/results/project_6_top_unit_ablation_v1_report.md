# PROJECT 6 TOP UNIT ABLATION V1

## Top Units
- top_units: [7, 19, 11, 0, 28]
- top_scores: [21.95582389831543, 19.320987701416016, 18.087909698486328, 17.590211868286133, 16.352413177490234]

## Performance Comparison
- baseline: {'digit_acc': 0.945, 'carry_acc': 1.0, 'exact_acc': 0.945}
- ablated: {'digit_acc': 0.665, 'carry_acc': 1.0, 'exact_acc': 0.665}

## Interpretation Boundary
- This is a first causal-style perturbation on top diagnostic units.
- It does not yet prove a full circuit, but it tests whether the identified units matter functionally.
