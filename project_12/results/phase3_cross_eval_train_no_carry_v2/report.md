# Phase 2 Transformer Smoke — Evaluation Report

## Configuration

| Key | Value |
|-----|-------|
| Seed | 0 |
| Train Size | 3000 |
| Eval Size | 1000 |
| Epochs | 3 |
| Train Mode | no_carry |
| Eval Modes | no_carry, carry_heavy |
| Obs Size | 78 |
| Action Size | 16 |
| Device | cpu |

## Results

| Mode | Accuracy |
|------|----------|
| no_carry | 0.7220 |
| carry_heavy | 0.5030 |


## Training History

- Epoch 1: loss=1.689154, eval_acc=0.7150
- Epoch 2: loss=1.339565, eval_acc=0.7150
- Epoch 3: loss=1.260044, eval_acc=0.7150

Git Commit: `4e60e6c713a3b2925ee1b51ffd1574cd59e97f64`
Timestamp: 2026-04-14T03:13:32.171268Z
