# Phase SUB0 Subtraction Smoke — Evaluation Report

## Configuration

| Key | Value |
|-----|-------|
| Seed | 0 |
| Train Size | 4000 |
| Eval Size | 1500 |
| Epochs | 3 |
| Operation | Subtraction (a >= b) |
| Obs Size | 78 |
| Action Size | 18 |
| Device | cpu |

## Results

| Metric | Value |
|--------|-------|
| Final Train Loss | 1.610390 |
| Final Eval Accuracy | 0.5993 |

## Training History

- Epoch 1: loss=1.839268, eval_acc=0.5980
- Epoch 2: loss=1.681488, eval_acc=0.5980
- Epoch 3: loss=1.610390, eval_acc=0.5993


## Notes

This is a MVP smoke run for subtraction. Model learns to predict actions for a - b where a >= b.
Not a validated claim. Simply demonstrates feasibility of subtraction in soroban environment.
