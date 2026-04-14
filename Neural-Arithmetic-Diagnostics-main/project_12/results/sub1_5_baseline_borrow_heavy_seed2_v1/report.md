# Phase SUB0 Subtraction Smoke — Evaluation Report

## Configuration

| Key | Value |
|-----|-------|
| Seed | 2 |
| Train Size | 2000 |
| Eval Size | 800 |
| Epochs | 3 |
| Operation | Subtraction (a >= b) |
| Obs Size | 78 |
| Action Size | 18 |
| Device | cpu |

## Results

| Metric | Value |
|--------|-------|
| Final Train Loss | 1.667788 |
| Final Eval Accuracy | 0.4938 |

## Training History

- Epoch 1: loss=2.077027, eval_acc=0.4938
- Epoch 2: loss=1.696284, eval_acc=0.4938
- Epoch 3: loss=1.667788, eval_acc=0.4938


## Notes

This is a MVP smoke run for subtraction. Model learns to predict actions for a - b where a >= b.
Not a validated claim. Simply demonstrates feasibility of subtraction in soroban environment.
