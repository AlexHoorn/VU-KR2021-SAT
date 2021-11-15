from typing import Any, List
from itertools import chain

CNFtype = List[List[int]]


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


def flatten_list(list_: List[List[Any]]) -> List[Any]:
    flattened = list(chain.from_iterable(list_))
    return flattened
