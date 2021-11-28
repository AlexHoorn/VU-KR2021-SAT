import argparse
import cProfile
import pstats
from io import StringIO
from os import path

import pandas as pd

from sattools.solvers import DPLL
from sattools.utils import read_dimacs, write_dimacs


def main(filepath: str, heuristic: str, runs: int, profile: bool):
    # Get filename without extension
    filename, _ = path.splitext(filepath)

    # Enable profiling
    if profile:
        profiler = cProfile.Profile()
        profiler.enable()

    # Get SAT and solve
    cnf = read_dimacs(filepath)

    stats = []

    for i in range(runs):
        dpll = DPLL(cnf, verbose=True, heuristic=heuristic)
        dpll.solve()

        # Feedback about solution
        if dpll.satisfied:
            print(f"Found solution with length {len(dpll.solution)}", end=", ")
            write_dimacs(dpll.solution, f"{filename}_{i}.out")
        else:
            print("Couldn't find satisfaction")

        run_stats = dict(
            backtracks=dpll.backtrack_count,
            propagations=dpll.propagation_count,
            duration=round(dpll.solve_duration, 2),
        )
        stats.append(run_stats)
        print(f"stats: {run_stats}")

    # Disable profiling
    if profile:
        profiler.disable()
        stream = StringIO()
        ps = pstats.Stats(profiler, stream=stream).sort_stats("tottime")
        ps.print_stats()

        # Write profiling report to file
        with open(f"{filename}_profiled.txt", "w+") as f:
            f.write(stream.getvalue())

    if runs > 1:
        df = pd.DataFrame(stats)
        print(df.agg(["mean", "std", "max"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SAT solver")
    parser.add_argument("file", type=str, help="Filepath to dimacs to solve")
    parser.add_argument(
        "--heuristic",
        default="random",
        help=f"The heuristic to use, one of {DPLL.get_available_heuristics()}",
    )
    parser.add_argument(
        "--runs", default=1, type=int, help="Run the solver multiple times",
    )
    parser.add_argument(
        "--profile", action="store_true", help="Enable cProfiler and store to file"
    )

    args = parser.parse_args()
    main(args.file, args.heuristic, args.runs, args.profile)
