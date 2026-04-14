# Phase SUB0 Subtraction Smoke — Evaluation Report

## Configuration

| Key | Value |
|-----|-------|
| Seed | 0 |
| Train Size | 1000 |
| Eval Size | 300 |
| Epochs | 3 |
| Operation | Subtraction (a >= b) |
| Obs Size | 78 |
| Action Size | 18 |
| Device | cpu |

## Results

| Metric | Value |
|--------|-------|
| Final Train Loss | 1.493472 |
| Final Eval Accuracy | 0.5667 |

## Training History

- Epoch 1: loss=2.182930, eval_acc=0.5667
- Epoch 2: loss=1.623673, eval_acc=0.5667
- Epoch 3: loss=1.493472, eval_acc=0.5667


## Notes

This is a MVP smoke run for subtraction. Model learns to predict actions for a - b where a >= b.
Not a validated claim. Simply demonstrates feasibility of subtraction in soroban environment.
