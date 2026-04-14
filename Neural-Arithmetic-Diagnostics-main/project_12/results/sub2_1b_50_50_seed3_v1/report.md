# Phase SUB0 Subtraction Smoke — Evaluation Report

## Configuration

| Key | Value |
|-----|-------|
| Seed | 3 |
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
| Final Train Loss | 1.603297 |
| Final Eval Accuracy | 0.5920 |

## Training History

- Epoch 1: loss=1.881580, eval_acc=0.5900
- Epoch 2: loss=1.692923, eval_acc=0.5900
- Epoch 3: loss=1.603297, eval_acc=0.5920


## Notes

This is a MVP smoke run for subtraction. Model learns to predict actions for a - b where a >= b.
Not a validated claim. Simply demonstrates feasibility of subtraction in soroban environment.
