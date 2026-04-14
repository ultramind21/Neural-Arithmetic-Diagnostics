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
| Final Train Loss | 1.245936 |
| Final Eval Accuracy | 0.5993 |

## Training History

- Epoch 1: loss=1.788022, eval_acc=0.5913
- Epoch 2: loss=1.521909, eval_acc=0.5713
- Epoch 3: loss=1.245936, eval_acc=0.5993


## Notes

This is a MVP smoke run for subtraction. Model learns to predict actions for a - b where a >= b.
Not a validated claim. Simply demonstrates feasibility of subtraction in soroban environment.
