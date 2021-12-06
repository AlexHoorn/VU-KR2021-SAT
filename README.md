# VU-KR2021-SAT
A SAT solving project for the Vrije Universiteit 2021 course Knowledge and Data.

## Implemented heuristics
```python
    'dlcs' : 'Dynamic largest combined sum'
    'dlis' : 'Dynamic largest individual sum'
      'jw' : 'Jeroslow-Wang one-sided'
   'jwtwo' : 'Jeroslow-Wang two-sided'
    'mams' : 'DLIS plus MOMS'
    'moms' : 'Maximum occurence in clauses of minimum size'
  'random' : 'Random with equal weights'
'weighted' : 'Random with weighting by amount of occurences'
```

## Instruction

### Requirements

Python version >= `3.7`.

Optionally the requirements `Pebble == 4.6.3` and `pandas == 1.3.4` have to be met if you wish to run `run_experiment.py`. The main program is provided in `SAT.py` which does not have any additional requirements.

To install both optional packages just run:
```console
pip install -r requirements.txt
```

### Usage

To do a single SAT solve and get its results run:
```console
python SAT.py PATH_TO_DIMACS_FILE --heuristic HEURISTIC
```
The resulting answer will be stored in `PATH_TO_DIMACS_FILE_n.out`

Replace `PATH_TO_DIMACS_FILE` with a string to where the SAT in DIMACS format can be found. As an example `sudoku-example_NxN.txt` are provided.

Replace `HEURISTIC` with the heuristic to use (default `random`). Supported heuristics are: `['dlcs', 'dlis', 'jw', 'jwtwo', 'mams', 'moms', 'random', 'weighted']`. Additionally the heuristic can be suffixed with either `_pos` or `_neg` to force a `True` or `False` assignment respectively. So then the heuristic given becomes e.g. `random_neg`.

Add `--runs n` if you wish to run and solve the solver `n` times. Each solution will be seperately stored.

Add `--profile` if you wish to get a `cProfile` report about the exact function runtimes and amount of calls.
