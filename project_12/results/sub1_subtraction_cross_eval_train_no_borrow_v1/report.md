# Phase SUB0 Subtraction Smoke — Evaluation Report

## Configuration

| Key | Value |
|-----|-------|
| Seed | 0 |
| Train Size | 100 |
| Eval Size | 100 |
| Epochs | 3 |
| Operation | Subtraction (a >= b) |
| Obs Size | 78 |
| Action Size | 18 |
| Device | cpu |

## Results

| Metric | Value |
|--------|-------|
| Final Train Loss | 1.969538 |
| Final Eval Accuracy | 0.5700 |

## Training History

- Epoch 1: loss=2.656176, eval_acc=0.2900
- Epoch 2: loss=2.270751, eval_acc=0.4500
- Epoch 3: loss=1.969538, eval_acc=0.5700


## Notes

This is a MVP smoke run for subtraction. Model learns to predict actions for a - b where a >= b.
Not a validated claim. Simply demonstrates feasibility of subtraction in soroban environment.
