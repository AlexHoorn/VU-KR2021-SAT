import argparse
from multiprocessing import Pool, cpu_count, freeze_support
from typing import Optional

import pandas as pd
from os import path

from sattools.solvers import DPLL
from sattools.sudoku import Sudoku
from sattools.utils import read_collections


def main(
    collection: str,
    heuristic: str,
    grid_size: int,
    repeat: int = 1,
    n_max: Optional[int] = None,
    ids_path: Optional[str] = None,
):
    # Grid as a string
    grid = f"{grid_size}x{grid_size}"

    # Get external ids
    if ids_path:
        with open(ids_path) as f:
            ids = f.read().splitlines()

    # Construct sudokus
    sudokus_collection = read_collections(collection, size=grid_size)[:n_max]
    sudokus = [Sudoku(sudoku, grid) for sudoku in sudokus_collection]
    # Make an iterator to construct DPLL solvers, zip with ids if available otherwise just enumerate
    sudokus_iter = zip(ids, sudokus) if ids_path else enumerate(sudokus)
    # Construct solvers
    solvers = [
        DPLL(sudoku.get_all_clauses(), heuristic=heuristic, identifier=identifier)
        for identifier, sudoku in sudokus_iter
    ]
    # Run every multiple times
    solvers = solvers * repeat

    stats_collection = []
    n_solvers = len(solvers)
    print(f"Solving {len(solvers)} sudokus, {heuristic = }, n threads = {cpu_count()}")

    # Enable multiprocessing
    with Pool() as pool:
        for i, stats in enumerate(pool.imap_unordered(solve_sudoku, solvers)):
            stats_collection.append(stats)
            print(stats, f"{i+1}/{n_solvers}")

    # Gathered statistic to a dataframe so it can be easily written as csv
    dataframe = pd.DataFrame(stats_collection)
    filename, _ = path.splitext(path.basename(collection))
    dataframe.to_csv(f"experiments/{grid}_{heuristic}_{filename}.csv", index=False)


def solve_sudoku(dpll: DPLL):
    dpll.solve()
    stats = dict(
        identifier=dpll.identifier,
        backtracks=dpll.backtrack_count,  # n backtracks
        propagations=dpll.propagation_count,  # n propagations
        duration=round(dpll.solve_duration, 2),  # duration in seconds
        constraint_size=len(
            dpll.determine_unit_clauses(dpll.cnf)
        ),  # size of original sudoku
        assignment_size=len(dpll.solution),  # size of final assignment
        satisfied=dpll.satisfied,  # true or false if satisfied
    )
    return stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SAT solving experiment")
    parser.add_argument("collection", help="Filepath to collection of sudokus")
    parser.add_argument(
        "--heuristic", default="random", help="The heuristic to use",
    )
    parser.add_argument(
        "--grid", default=9, type=int, help="Gridsize of the sudoku, e.g. 9 for 9x9"
    )
    parser.add_argument(
        "--repeat", default=1, type=int, help="Repeat every solve n times"
    )
    parser.add_argument(
        "--n_max", default=None, type=int, help="Max amount of sudokus to run"
    )
    parser.add_argument(
        "--ids", default=None, help="Filepath to ids to use instead of enumeration"
    )

    args = parser.parse_args()

    freeze_support()
    main(args.collection, args.heuristic, args.grid, args.repeat, args.n_max, args.ids)
