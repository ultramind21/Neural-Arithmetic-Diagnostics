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
| Final Train Loss | 1.697108 |
| Final Eval Accuracy | 0.6038 |

## Training History

- Epoch 1: loss=2.250077, eval_acc=0.6038
- Epoch 2: loss=1.741455, eval_acc=0.6038
- Epoch 3: loss=1.697108, eval_acc=0.6038


## Notes

This is a MVP smoke run for subtraction. Model learns to predict actions for a - b where a >= b.
Not a validated claim. Simply demonstrates feasibility of subtraction in soroban environment.
