# Instruction

## Requirements

Python version >= `3.7`.

Packages:
- Numpy *(tested 1.21.4)*
- Pandas *(tested 1.3.4)*

## Usage

To do a single SAT solve and get its results:
`python run_solver.py PATH_TO_DIMACS_FILE --heuristic HEURISTIC`

Replace `PATH_TO_DIMACS_FILE` with a string to where the SAT in DIMACS format can be found.

Replace `HEURISTIC` with the heuristic to use. Supported are: `["random", "weighted", "weighted_abs", "greedy"]`.

Add `--profile` if you wish to get a `cProfile` report about the exact function runtimes and amount of calls.