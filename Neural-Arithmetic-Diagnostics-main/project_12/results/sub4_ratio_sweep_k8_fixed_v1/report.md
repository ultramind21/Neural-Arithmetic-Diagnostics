# SUB4 ratio sweep (active_digits=8)

- Fixed: active_digits=8, train_size=4000, eval_size=1500, epochs=3
- Variable: train_mix ratio (no_borrow vs borrow_heavy)
- Replicates: seeds 0..2

- seed=0 mix={'no_borrow': 0.1, 'borrow_heavy': 0.9}: {'no_borrow': 0.586, 'borrow_heavy': 0.514}
- seed=1 mix={'no_borrow': 0.1, 'borrow_heavy': 0.9}: {'no_borrow': 0.5753333333333334, 'borrow_heavy': 0.5006666666666667}
- seed=2 mix={'no_borrow': 0.1, 'borrow_heavy': 0.9}: {'no_borrow': 0.5993333333333334, 'borrow_heavy': 0.5653333333333334}
- seed=0 mix={'no_borrow': 0.3, 'borrow_heavy': 0.7}: {'no_borrow': 0.6226666666666667, 'borrow_heavy': 0.5033333333333333}
- seed=1 mix={'no_borrow': 0.3, 'borrow_heavy': 0.7}: {'no_borrow': 0.6346666666666667, 'borrow_heavy': 0.5253333333333333}
- seed=2 mix={'no_borrow': 0.3, 'borrow_heavy': 0.7}: {'no_borrow': 0.6093333333333333, 'borrow_heavy': 0.5113333333333333}
- seed=0 mix={'no_borrow': 0.5, 'borrow_heavy': 0.5}: {'no_borrow': 0.6313333333333333, 'borrow_heavy': 0.49933333333333335}
- seed=1 mix={'no_borrow': 0.5, 'borrow_heavy': 0.5}: {'no_borrow': 0.6260, 'borrow_heavy': 0.5066666666666667}
- seed=2 mix={'no_borrow': 0.5, 'borrow_heavy': 0.5}: {'no_borrow': 0.6313333333333333, 'borrow_heavy': 0.5266666666666667}
- seed=0 mix={'no_borrow': 0.7, 'borrow_heavy': 0.3}: {'no_borrow': 0.6606666666666667, 'borrow_heavy': 0.48}
- seed=1 mix={'no_borrow': 0.7, 'borrow_heavy': 0.3}: {'no_borrow': 0.6573333333333333, 'borrow_heavy': 0.4746666666666667}
- seed=2 mix={'no_borrow': 0.7, 'borrow_heavy': 0.3}: {'no_borrow': 0.636, 'borrow_heavy': 0.4933333333333333}
- seed=0 mix={'no_borrow': 0.9, 'borrow_heavy': 0.1}: {'no_borrow': 0.7073333333333334, 'borrow_heavy': 0.48}
- seed=1 mix={'no_borrow': 0.9, 'borrow_heavy': 0.1}: {'no_borrow': 0.68, 'borrow_heavy': 0.4813333333333333}
- seed=2 mix={'no_borrow': 0.9, 'borrow_heavy': 0.1}: {'no_borrow': 0.6853333333333333, 'borrow_heavy': 0.48}
