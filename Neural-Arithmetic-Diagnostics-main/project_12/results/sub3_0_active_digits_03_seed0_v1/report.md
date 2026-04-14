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
| Active Digits | 3 |
| Device | cpu |

## Results

| Metric | Value |
|--------|-------|
| Final Train Loss | 0.598177 |
| Final Eval Accuracy | 0.9107 |

## Training History

- Epoch 1: loss=1.556980, eval_acc=0.5807
- Epoch 2: loss=1.040197, eval_acc=0.8140
- Epoch 3: loss=0.598177, eval_acc=0.9107


## Notes

This is a MVP smoke run for subtraction. Model learns to predict actions for a - b where a >= b.
Not a validated claim. Simply demonstrates feasibility of subtraction in soroban environment.
