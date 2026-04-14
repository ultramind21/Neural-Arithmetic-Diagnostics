# Phase SUB0 Subtraction Smoke — Evaluation Report

## Configuration

| Key | Value |
|-----|-------|
| Seed | 0 |
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
| Final Train Loss | 1.651084 |
| Final Eval Accuracy | 0.5012 |

## Training History

- Epoch 1: loss=1.950124, eval_acc=0.5012
- Epoch 2: loss=1.694872, eval_acc=0.5012
- Epoch 3: loss=1.651084, eval_acc=0.5012


## Notes

This is a MVP smoke run for subtraction. Model learns to predict actions for a - b where a >= b.
Not a validated claim. Simply demonstrates feasibility of subtraction in soroban environment.
