from itertools import chain
from os import mkdir, pathsep, path, write
from posixpath import dirname
from typing import Any, Iterable, List

CNFtype = List[List[int]]

# Hey Alex, I tried to do it according to your structure
# but oc feel free to change everything as you want
sudoku_collectiontype = List[List[str]]


def read_dimacs(filepath: str) -> CNFtype:
    """Read a DIMACS file.

    Args:
        filepath (str): path to where file is.

    Returns:
        List[np.ndarray]: list of clauses as numpy arrays.
    """
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
            clauses_int = [int(i) for i in clauses]  # Convert to integers

            clause_list.append(clauses_int)

    return clause_list


def write_dimacs(iterable: Iterable[Any], filepath: str):
    with open(filepath, "w") as f:
        for i in iterable:
            f.write(f"{i} 0\n")


def flatten_list(list_: List[List[Any]]) -> List[Any]:
    flattened = list(chain.from_iterable(list_))
    return flattened


def read_collections(filepath: str, size=9, write=False) -> CNFtype:
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
        except:
            ...

    for num, row in enumerate(single_sudokus):

        sudoku = []
        # a list containing all starting positions in DIMACS as string

        vals = list(row)

        # not sure wether its row by row or column by column
        # doesnt really matter tho, its just a transposition
        # here its row by row
        for i in range(0, size):
            for j in range(0, size):

                if vals[i * 9 + j] == ".":
                    ...

                else:
                    sudoku.append([int(f"{i+1}{j+1}{vals[i*9 + j]}")])

        sudoku_collection.append(sudoku)

        if write:
            write_file = path.join(write_dir, f"{str(num)}.txt")
            write_dimacs(sudoku, write_file)

    return sudoku_collection
