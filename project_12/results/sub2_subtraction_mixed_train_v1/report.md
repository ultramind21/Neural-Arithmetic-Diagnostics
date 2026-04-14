# Phase SUB0 Subtraction Smoke — Evaluation Report

## Configuration

| Key | Value |
|-----|-------|
| Seed | 0 |
| Train Size | 3000 |
| Eval Size | 1000 |
| Epochs | 3 |
| Operation | Subtraction (a >= b) |
| Obs Size | 78 |
| Action Size | 18 |
| Device | cpu |

## Results

| Metric | Value |
|--------|-------|
| Final Train Loss | 1.643588 |
| Final Eval Accuracy | 0.5990 |

## Training History

- Epoch 1: loss=1.883295, eval_acc=0.5990
- Epoch 2: loss=1.703185, eval_acc=0.5990
- Epoch 3: loss=1.643588, eval_acc=0.5990


## Notes

This is a MVP smoke run for subtraction. Model learns to predict actions for a - b where a >= b.
Not a validated claim. Simply demonstrates feasibility of subtraction in soroban environment.
