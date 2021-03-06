from itertools import chain
from os import mkdir, path
from typing import Any, Iterable, List, Set

CNFtype = List[Set[int]]


def read_dimacs(filepath: str) -> CNFtype:
    """Read a DIMACS file."""
    with open(filepath, encoding="UTF-8") as f:
        # Read the file and split by newlines into a list
        dimacs_lines = f.read().splitlines()

    clause_list = []
    for row in dimacs_lines:
        if row[0] in ("c", "p"):
            # Currently does nothing if the line is a comment
            ...

        else:
            row = row.rstrip("0")  # Remove the trailing 0
            row = row.strip()  # Remove leading and trailing spaces
            clauses = row.split(" ")  # Split into statements
            clauses_int = {int(i) for i in clauses}  # Convert to integers
            clause_list.append(clauses_int)

    return clause_list


def write_dimacs(iterable: Iterable[Any], filepath: str):
    with open(filepath, "w") as f:
        for i in iterable:
            if isinstance(i, int):
                i = [i]
            line = " ".join([str(i) for i in i])
            f.write(f"{line} 0\n")


def flatten_list(list_: Iterable[Iterable[Any]]) -> List[Any]:
    flattened = list(chain.from_iterable(list_))
    return flattened


def read_sudoku_collections(filepath: str, size=9, write=False) -> List[CNFtype]:
    """Read a collection of sudokus in *txt files.

    Args:
        filepath (str): path to where file is.
        size (int): size of the sudoku, default 9x9

    Returns:
        a list of lists containing the dimacs rows as elements -> need another function to get them? 
        or writing single DIMACS files?
    """

    with open(filepath, encoding="UTF-8") as f:
        # Read the file and split by newlines into a list
        single_sudokus = f.read().splitlines()

    sudoku_collection = []

    if write:
        write_dir = filepath.split(".")[0]
        try:
            mkdir(write_dir)
        except FileExistsError:
            pass

    for num, row in enumerate(single_sudokus):

        sudoku = []
        # a list containing all starting positions in DIMACS as string

        vals = list(row)

        # not sure wether its row by row or column by column
        # doesnt really matter tho, its just a transposition
        # here its row by row
        for i in range(0, size):
            for j in range(0, size):

                if vals[i * size + j] == ".":
                    ...

                else:

                    if size == 16:

                        if vals[i * size + j] in "ABCDEFG":
                            if vals[i * size + j] == "A":
                                vals[i * size + j] = "10"
                            elif vals[i * size + j] == "B":
                                vals[i * size + j] = "11"
                            elif vals[i * size + j] == "C":
                                vals[i * size + j] = "12"
                            elif vals[i * size + j] == "D":
                                vals[i * size + j] = "13"
                            elif vals[i * size + j] == "E":
                                vals[i * size + j] = "14"
                            elif vals[i * size + j] == "F":
                                vals[i * size + j] = "15"
                            elif vals[i * size + j] == "G":
                                vals[i * size + j] = "16"

                        sudoku.append(
                            {
                                int(
                                    (i + 1) * 289
                                    + (j + 1) * 17
                                    + int(vals[i * size + j])
                                )
                            }
                        )

                    else:
                        sudoku.append({int(f"{i+1}{j+1}{vals[i*size + j]}")})

        sudoku_collection.append(sudoku)

        if write:
            write_file = path.join(write_dir, f"{str(num)}.txt")
            write_dimacs(sudoku, write_file)

    return sudoku_collection


def neg_abs(x):
    return -abs(x)
