# PROJECT 4 ADVERSARIAL TRAINING REPORT

## Status
Bounded MVP adversarial training artifact generated.

## Core Question
Does adversarial training improve seen-family robustness only, or also transfer to held-out adversarial structure?

## Seen Adversarial Families
- alternating_carry: {'digit_acc': 1.0, 'carry_acc': 1.0, 'combined_acc': 1.0, 'exact_match': 1.0}
- full_propagation_chain: {'digit_acc': 0.6000000238418579, 'carry_acc': 1.0, 'combined_acc': 0.6000000238418579, 'exact_match': 0.0}

## Held-Out Adversarial Family
- block_boundary_stress: {'digit_acc': 0.6000000238418579, 'carry_acc': 0.800000011920929, 'combined_acc': 0.6000000238418579, 'exact_match': 0.0}

## Baseline Reference
- in_distribution: compare against PROJECT_4_BASELINE_CLASSIFICATION_SUMMARY.md
- heldout_block_boundary_reference: compare against stable baseline matrix

## Qualification
- This is a bounded MVP intervention artifact.
- Stronger robustness claims require repeated-run validation and later synthesis.
