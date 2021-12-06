import argparse
from concurrent.futures import TimeoutError
from multiprocessing import cpu_count, freeze_support
from os import path
from typing import Optional

import pandas as pd
from pebble import ProcessPool
from pebble.common import ProcessExpired

from sattools.solvers import DPLL
from sattools.sudoku import Sudoku
from sattools.utils import read_sudoku_collections


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
    sudokus_collection = read_sudoku_collections(collection, size=grid_size)[:n_max]
    sudokus = [Sudoku(sudoku, grid) for sudoku in sudokus_collection]
    # Make an iterator to construct DPLL solvers, zip with ids if available otherwise just enumerate
    sudokus_iter = zip(ids, sudokus) if ids_path else enumerate(sudokus)
    # Construct solvers
    solvers = [
        DPLL(sudoku.get_all_clauses(), heuristic=heuristic, identifier=identifier,)
        for identifier, sudoku in sudokus_iter
    ]
    # Run every multiple times
    solvers = solvers * repeat

    stats_collection = []
    timeouts = 0
    print(f"Solving {len(solvers)} sudokus, {heuristic = }, n threads = {cpu_count()}")

    # Enable multiprocessing through Pebble
    with ProcessPool() as pool:
        future = pool.map(solve_sudoku, solvers, timeout=600)
        iterator = future.result()

        while True:
            try:
                result = next(iterator)
                stats_collection.append(result)
                print(result)
            except StopIteration:
                break
            except TimeoutError as error:
                timeouts += 1
                print("Timeout")
            except ProcessExpired as error:
                print("Process expired")
            except Exception as error:
                print("function raised %s" % error)
                print(error.traceback)

    # Gather statistic to a dataframe so it can be easily written as csv
    dataframe = pd.DataFrame(stats_collection)
    filename, _ = path.splitext(path.basename(collection))
    outfile = "_".join([grid, heuristic, filename])
    dataframe.to_csv(f"experiments/{outfile}.csv", index=False)

    if timeouts > 0:
        with open(f"experiments/{outfile}_timeouts.txt", "w") as f:
            f.write(str(timeouts))


def solve_sudoku(dpll: DPLL):
    dpll.solve()
    stats = dict(
        identifier=dpll.identifier,
        backtracks=dpll.backtrack_count,  # n backtracks
        propagations=dpll.propagation_count,  # n propagations
        duration=dpll.solve_duration,  # duration in seconds
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
