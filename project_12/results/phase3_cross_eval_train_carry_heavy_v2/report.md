# Phase 2 Transformer Smoke — Evaluation Report

## Configuration

| Key | Value |
|-----|-------|
| Seed | 0 |
| Train Size | 3000 |
| Eval Size | 1000 |
| Epochs | 3 |
| Train Mode | carry_heavy |
| Eval Modes | carry_heavy, no_carry |
| Obs Size | 78 |
| Action Size | 16 |
| Device | cpu |

## Results

| Mode | Accuracy |
|------|----------|
| carry_heavy | 0.8440 |
| no_carry | 0.0260 |


## Training History

- Epoch 1: loss=1.689372, eval_acc=0.5000
- Epoch 2: loss=1.248985, eval_acc=0.5270
- Epoch 3: loss=0.835581, eval_acc=0.8610

Git Commit: `4e60e6c713a3b2925ee1b51ffd1574cd59e97f64`
Timestamp: 2026-04-14T03:13:41.696732Z
