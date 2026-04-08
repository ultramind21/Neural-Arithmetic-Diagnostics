"""
PROJECT 10 REGIME C V1: OVERPOWERED UNIVERSAL RESCUE

Purpose:
    Determine if mechanism power can substitute for family-specificity.
    Tests whether boosting universal rescue (40% amplification) allows it
    to overcome the family-aware rescue advantage observed in Regime A V2.

Design:
    - Family structure: Regime A V2 (high heterogeneity, residual ±0.015)
    - Universal rescue: base_gain = 0.42 * shared_failure_factor (0.30 → 0.42, +40%)
    - Family-aware rescue: unchanged from A V2
    - Verdict thresholds: same as A V2

Expected Outcomes:
    1. If universal dominates (wins ≥2): Mechanism power > family-specificity (WEAKENS)
    2. If family-aware persists (wins ≥3): Family structure is fundamental (SUPPORTS)
    3. All other: Competitive balance/boundary (BOUNDARY)

Interpretation:
    This test bridges internal evidence (Laws 1&3) and external falsification (Regimes A&B).
    If mechanism power can overcome family-specificity, then the higher-order candidate
    is based on a false premise. If family-specificity persists, the candidate is sound.
"""

import json
import datetime
import numpy as np
from pathlib import Path


def build_regime():
    """
    Construct Regime C test cases with high family heterogeneity
    (replicates Regime A V2 structure for direct comparison).
    """
    families = []
    
    # Family A: High competence, moderate global deficit
    families.append({
        'name': 'family_A',
        'local_competence': 0.93,
        'base_global_score': 0.48,
        'shared_failure_factor': 0.41,
        'residual_family_factor': 0.015,
    })
    
    # Family B: Slightly lower competence, similar global deficit
    families.append({
        'name': 'family_B',
        'local_competence': 0.92,
        'base_global_score': 0.47,
        'shared_failure_factor': 0.40,
        'residual_family_factor': -0.015,
    })
    
    # Family C: High competence, lower global deficit
    families.append({
        'name': 'family_C',
        'local_competence': 0.94,
        'base_global_score': 0.46,
        'shared_failure_factor': 0.41,
        'residual_family_factor': 0.015,
    })
    
    # Family D: Stable competence, lowest global deficit
    families.append({
        'name': 'family_D',
        'local_competence': 0.93,
        'base_global_score': 0.47,
        'shared_failure_factor': 0.40,
        'residual_family_factor': -0.015,
    })
    
    return families


def universal_rescue(base_global_score, shared_failure_factor):
    """
    Overpowered universal rescue mechanism.
    
    Increased from 0.30 factor (Regime A V2) to 0.42 (+40% boost).
    Tests whether mechanism power alone can overcome family-specificity advantages.
    """
    base_gain = 0.42 * shared_failure_factor
    final_score = base_global_score + base_gain
    return round(final_score, 4)


def family_aware_rescue(base_global_score, shared_failure_factor, residual_family_factor):
    """
    Family-aware rescue mechanism (unchanged from Regime A V2).
    
    Provides targeted help based on family-specific misalignment.
    """
    base_gain = 0.30 * shared_failure_factor
    residual_gain = 0.80 * abs(residual_family_factor)
    final_score = base_global_score + base_gain + residual_gain
    return round(final_score, 4)


def determine_winner(universal_score, family_aware_score, tolerance=0.005):
    """
    Determine winner based on scores.
    Tolerance of 0.005 defines 'near_tie' (within epsilon of each other).
    """
    diff = family_aware_score - universal_score
    
    if abs(diff) <= tolerance:
        return 'near_tie'
    elif diff > tolerance:
        return 'family_aware'
    else:
        return 'universal'


def determine_verdict(universal_wins, family_aware_wins, near_ties, avg_universal, avg_family_aware):
    """
    Determine overall verdict based on per-family results.
    
    Thresholds (same as Regime A V2):
    - WEAKENS if: universal_wins ≥ 2 OR avg_universal ≥ avg_family_aware - 0.005
    - SUPPORTS if: family_aware_wins ≥ 3 AND avg_family_aware - avg_universal > 0.008
    - Else: BOUNDARY
    """
    if universal_wins >= 2 or avg_universal >= avg_family_aware - 0.005:
        return 'WEAKENS HIGHER-ORDER CANDIDATE'
    elif family_aware_wins >= 3 and avg_family_aware - avg_universal > 0.008:
        return 'SUPPORTS HIGHER-ORDER CANDIDATE'
    else:
        return 'BOUNDARY PRESSURE ON HIGHER-ORDER CANDIDATE'


def main():
    print("=" * 80)
    print("PROJECT 10 REGIME C OVERPOWERED UNIVERSAL RESCUE V1")
    print("=" * 80)
    
    families = build_regime()
    
    # Calculate results for each family
    rows = []
    universal_scores = []
    family_aware_scores = []
    
    for family in families:
        universal_score = universal_rescue(
            family['base_global_score'],
            family['shared_failure_factor']
        )
        family_aware_score = family_aware_rescue(
            family['base_global_score'],
            family['shared_failure_factor'],
            family['residual_family_factor']
        )
        winner = determine_winner(universal_score, family_aware_score)
        
        universal_scores.append(universal_score)
        family_aware_scores.append(family_aware_score)
        
        row = {
            'family': family['name'],
            'local_competence': family['local_competence'],
            'base_global_score': family['base_global_score'],
            'shared_failure_factor': family['shared_failure_factor'],
            'residual_family_factor': family['residual_family_factor'],
            'universal_rescue_score': universal_score,
            'family_aware_rescue_score': family_aware_score,
            'winner': winner,
        }
        rows.append(row)
    
    # Aggregate results
    universal_wins = sum(1 for r in rows if r['winner'] == 'universal')
    family_aware_wins = sum(1 for r in rows if r['winner'] == 'family_aware')
    near_ties = sum(1 for r in rows if r['winner'] == 'near_tie')
    
    avg_universal = round(np.mean(universal_scores), 4)
    avg_family_aware = round(np.mean(family_aware_scores), 4)
    
    verdict = determine_verdict(
        universal_wins, family_aware_wins, near_ties,
        avg_universal, avg_family_aware
    )
    
    # Build artifact
    artifact = {
        'timestamp_utc': datetime.datetime.utcnow().isoformat() + 'Z',
        'experiment': 'project_10_regime_c_overpowered_universal_rescue_v1',
        'regime': 'Regime C — Overpowered Universal Rescue V1',
        'cases': families,
        'rows': rows,
        'summary': {
            'avg_base_global_score': round(np.mean([f['base_global_score'] for f in families]), 4),
            'avg_universal_rescue_score': avg_universal,
            'avg_family_aware_rescue_score': avg_family_aware,
            'universal_wins': universal_wins,
            'family_aware_wins': family_aware_wins,
            'near_ties': near_ties,
            'verdict': verdict,
        },
        'notes': [
            'This is the first Regime C implementation in Project 10.',
            'It tests whether overpowered universal rescue (40% boost) can overcome family-aware advantage.',
            'Family structure identical to Regime A V2 (high heterogeneity, ±0.015).',
            'Only variable: universal rescue factor amplified from 0.30 to 0.42.',
        ],
    }
    
    # Save JSON artifact
    results_dir = Path('project_10/results')
    results_dir.mkdir(parents=True, exist_ok=True)
    
    artifact_path = results_dir / 'project_10_regime_c_overpowered_universal_rescue_v1_artifact.json'
    with open(artifact_path, 'w') as f:
        json.dump(artifact, f, indent=2)
    print(f"✓ JSON artifact saved to: {artifact_path.absolute()}")
    
    # Generate markdown report
    report_path = results_dir / 'project_10_regime_c_overpowered_universal_rescue_v1_report.md'
    report_content = f"""# PROJECT 10 REGIME C OVERPOWERED UNIVERSAL RESCUE V1

## Purpose
Adversarial regime testing whether mechanism power can substitute for family-specificity.

## Summary
- avg_base_global_score: {artifact['summary']['avg_base_global_score']}
- avg_universal_rescue_score: {artifact['summary']['avg_universal_rescue_score']}
- avg_family_aware_rescue_score: {artifact['summary']['avg_family_aware_rescue_score']}
- universal_wins: {artifact['summary']['universal_wins']}
- family_aware_wins: {artifact['summary']['family_aware_wins']}
- near_ties: {artifact['summary']['near_ties']}
- verdict: {artifact['summary']['verdict']}

## Per-Family Results
- family_A: base={families[0]['base_global_score']}, universal={rows[0]['universal_rescue_score']}, family_aware={rows[0]['family_aware_rescue_score']}, winner={rows[0]['winner']}
- family_B: base={families[1]['base_global_score']}, universal={rows[1]['universal_rescue_score']}, family_aware={rows[1]['family_aware_rescue_score']}, winner={rows[1]['winner']}
- family_C: base={families[2]['base_global_score']}, universal={rows[2]['universal_rescue_score']}, family_aware={rows[2]['family_aware_rescue_score']}, winner={rows[2]['winner']}
- family_D: base={families[3]['base_global_score']}, universal={rows[3]['universal_rescue_score']}, family_aware={rows[3]['family_aware_rescue_score']}, winner={rows[3]['winner']}

## Interpretation
This regime amplified universal rescue by 40% (factor 0.30 → 0.42) to test whether mechanism power alone can overcome family-specificity advantages observed in Regime A V2.

**Result**: {artifact['summary']['verdict']}
"""
    
    with open(report_path, 'w') as f:
        f.write(report_content)
    print(f"✓ Markdown report saved to: {report_path.absolute()}")
    
    print(f"✓ Verdict: {verdict}")
    print("=" * 80)


if __name__ == '__main__':
    main()
