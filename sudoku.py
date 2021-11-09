from typing import Generator, List, Tuple
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

    def __iter__(self) -> Generator[List]:
        """Iterator that makes iterating over all clauses easy with e.g. `for clause in sudoku`.

        Yields:
            Generator[List]: every clause in rules + constraints + answers.
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

    def check_satisfied(self) -> bool:
        """Check if puzzle is satisfied with the given answers.

        Returns:
            bool: boolean stating True if satisfied.
        """
        # Split values and whether they are negated
        rules, negations = self._get_map(self.base_rules)

        clauses_boolean = list(map(self._map_value, rules, negations))
        clauses_boolean = list(map(np.any, clauses_boolean))

        return np.all(clauses_boolean)

    def _get_map(self, clauses) -> Tuple[List, List]:
        """Split clauses into absolutes of variables and a mask whether they are negated"""
        # TODO: This can be much faster

        # Convert clauses to absolute values
        values = [[abs(v) for v in c] for c in clauses]
        # Determine which values have to be negated
        negations = [[v < 0 for v in c] for c in clauses]

        return values, negations

    def _map_value(self, values, negatives) -> List:
        """"""
        clause = np.isin(values, self.constraints + self.answers)
        clause = np.where(negatives, ~clause, clause)

        return clause


def read_dimacs(filepath: str) -> List:
    with open(filepath) as f:
        dimacs_lines = f.read().splitlines()

    clause_list = []
    for row in dimacs_lines:
        if row[0] in ("c", "p"):
            ...

        else:
            row = row.rstrip(" 0")
            clauses = row.split(" ")
            clauses = [int(i) for i in clauses]

            clause_list.append(clauses)

    return clause_list
