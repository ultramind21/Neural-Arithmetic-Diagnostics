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
| Active Digits | 4 |
| Device | cpu |

## Results

| Metric | Value |
|--------|-------|
| Final Train Loss | 0.879018 |
| Final Eval Accuracy | 0.8560 |

## Training History

- Epoch 1: loss=1.682235, eval_acc=0.6027
- Epoch 2: loss=1.202805, eval_acc=0.6807
- Epoch 3: loss=0.879018, eval_acc=0.8560


## Notes

This is a MVP smoke run for subtraction. Model learns to predict actions for a - b where a >= b.
Not a validated claim. Simply demonstrates feasibility of subtraction in soroban environment.
