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
| Final Train Loss | 2.191905 |
| Final Eval Accuracy | 0.4900 |

## Training History

- Epoch 1: loss=2.797783, eval_acc=0.2200
- Epoch 2: loss=2.469129, eval_acc=0.2200
- Epoch 3: loss=2.191905, eval_acc=0.4900


## Notes

This is a MVP smoke run for subtraction. Model learns to predict actions for a - b where a >= b.
Not a validated claim. Simply demonstrates feasibility of subtraction in soroban environment.
