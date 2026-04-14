# Phase SUB0 Subtraction Smoke — Evaluation Report

## Configuration

| Key | Value |
|-----|-------|
| Seed | 2 |
| Train Size | 4000 |
| Eval Size | 1500 |
| Epochs | 3 |
| Operation | Subtraction (a >= b) |
| Obs Size | 78 |
| Action Size | 18 |
| Active Digits | 8 |
| Device | cpu |

## Results

| Metric | Value |
|--------|-------|
| Final Train Loss | 1.303337 |
| Final Eval Accuracy | 0.6280 |

## Training History

- Epoch 1: loss=1.801906, eval_acc=0.5913
- Epoch 2: loss=1.520324, eval_acc=0.5927
- Epoch 3: loss=1.303337, eval_acc=0.6280


## Notes

This is a MVP smoke run for subtraction. Model learns to predict actions for a - b where a >= b.
Not a validated claim. Simply demonstrates feasibility of subtraction in soroban environment.
