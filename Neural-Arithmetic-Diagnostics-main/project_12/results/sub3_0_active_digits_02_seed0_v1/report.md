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
| Active Digits | 2 |
| Device | cpu |

## Results

| Metric | Value |
|--------|-------|
| Final Train Loss | 0.308290 |
| Final Eval Accuracy | 0.9080 |

## Training History

- Epoch 1: loss=1.552824, eval_acc=0.6627
- Epoch 2: loss=0.730464, eval_acc=0.9253
- Epoch 3: loss=0.308290, eval_acc=0.9080


## Notes

This is a MVP smoke run for subtraction. Model learns to predict actions for a - b where a >= b.
Not a validated claim. Simply demonstrates feasibility of subtraction in soroban environment.
