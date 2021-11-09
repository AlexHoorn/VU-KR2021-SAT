from typing import Iterator, List

import numpy as np


class Sudoku:
    def __init__(self, filepath: str) -> None:
        """Implements the Sudoku puzzle.

        Args:
            filepath (str): string of the filepath of Sudoku in DIMACS.
        """
        self.base_rules = self.get_base_rules()
        self.constraints = read_dimacs(filepath=filepath)

        self.answers: List[int] = []

    def __iter__(self) -> Iterator[List]:
        """Iterator that makes iterating over all clauses easy with e.g. `for clause in sudoku`.

        Yields:
            Iterator[List]: every clause in rules + constraints + answers.
        """
        clauses = self.get_all_clauses()
        for c in clauses:
            yield c

    def get_base_rules(self) -> List:
        """Simply wraps read_dimacs with the path to the rules."""
        return read_dimacs(filepath="sudoku-rules.txt")

    def add_answer(self, clause: int) -> None:
        """Add answer to puzzle.

        Args:
            clause (int): int representing answer i.e. 135 row 1, column 3 and value 5.
        """
        if clause not in self.constraints:
            self.answers.append(clause)

    def clear_answers(self) -> None:
        """Empty list of answers."""
        self.answers = []

    def get_all_clauses(self) -> List:
        """Return all clauses in the puzzle (rules + constraints + answers)."""
        return self.base_rules + self.constraints + self.answers

    def get_satisfaction(self) -> bool:
        """Check if puzzle is satisfied with the given answers.

        Returns:
            bool: boolean stating True if satisfied.
        """
        # This runs _get_clause_satisfaction for every clause in base_rules
        satisfactions = list(map(self._get_clause_satisfaction, self.base_rules))
        # Check if ALL clauses have returned True because these are joined by an AND
        satisfied = np.all(satisfactions)

        return satisfied

    def _get_clause_satisfaction(self, clause: List) -> bool:
        """Check for a single given clause whether it's satisfied."""
        # Get the absolutes of the values, makes mapping them easier
        values = np.abs(clause)
        # Determine which have to be negated later
        negations = np.array(clause) < 0

        # Set values to true if they exist in the constraints or answers
        values_bool = np.isin(values, self.constraints + self.answers)
        # Negate the values with the negations array
        values_bool = np.where(negations, ~values_bool, values_bool)

        # Check if ANY in clause is True because a single clause is joined by OR
        satisfied = np.any(values_bool)

        return satisfied


def read_dimacs(filepath: str) -> List[List[int]]:
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
