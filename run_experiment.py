import argparse
from multiprocessing import Pool, cpu_count, freeze_support

import pandas as pd
from os import path

from sattools.solvers import DPLL
from sattools.sudoku import Sudoku
from sattools.utils import read_collections


def main(collection: str, heuristic: str, grid: int):
    grid = f"{grid}x{grid}"

    sudokus_collection = read_collections(collection)
    sudokus = [Sudoku(sudoku, grid) for sudoku in sudokus_collection]
    solvers = [
        DPLL(sudoku.get_all_clauses(), heuristic=heuristic) for sudoku in sudokus
    ]

    stats_collection = []
    n_solvers = len(solvers)
    with Pool() as pool:
        print(f"Solving {len(solvers)} sudokus with {cpu_count()} threads")
        # stats = list(pool.map(solve_sudoku, solvers))

        for i, stats in enumerate(pool.imap_unordered(solve_sudoku, solvers)):
            stats_collection.append(stats)
            print(stats, f"{i}/{n_solvers}")

    dataframe = pd.DataFrame(stats_collection)
    filename, _ = path.splitext(path.basename(collection))
    dataframe.to_csv(f"experiments/{grid}_{heuristic}_{filename}.csv")


def solve_sudoku(dpll: DPLL):
    dpll.solve()
    stats = dict(
        backtracks=dpll.backtrack_count,
        propagations=dpll.propagation_count,
        duration=round(dpll.solve_duration, 2),
        satisfied=dpll.satisfied,
    )
    return stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SAT solving experiment")
    parser.add_argument(
        "collection", type=str, help="Filepath to collection of sudokus"
    )
    parser.add_argument(
        "--heuristic", default="random", help="The heuristic to use",
    )
    parser.add_argument(
        "--grid", default=9, help="Gridsize of the sudoku, e.g. 9 for 9x9"
    )

    args = parser.parse_args()

    freeze_support()
    main(args.collection, args.heuristic, args.grid)
