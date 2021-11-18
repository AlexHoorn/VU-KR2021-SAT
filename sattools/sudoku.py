from typing import Iterator, List, Union

import numpy as np

from .utils import CNFtype, read_dimacs


class Sudoku:
    def __init__(self, filepath: str) -> None:
        """Implements the Sudoku puzzle.

        Args:
            filepath (str): string of the filepath of Sudoku in DIMACS.
        """
        self.base_rules = self.get_base_rules()
        self.constraints = read_dimacs(filepath=filepath)
        self.answers: List[List[int]] = []

    def __iter__(self) -> Iterator[List[int]]:
        """Iterator that makes iterating over all clauses easy with e.g. `for clause in sudoku`.

        Yields:
            Iterator[List]: every clause in rules + constraints + answers.
        """
        clauses = self.get_all_clauses()
        for c in clauses:
            yield c

    def get_base_rules(self) -> CNFtype:
        """Simply wraps read_dimacs with the path to the rules."""
        return read_dimacs(filepath="sudoku-rules.txt")

    def add_answer(self, clauses: Union[List[int], int]) -> None:
        """Add answer to puzzle.

        Args:
            clause (int): int representing answer i.e. 135 row 1, column 3 and value 5.
        """
        if isinstance(clauses, int):
            clauses = [clauses]

        for clause in clauses:
            assert clause not in self.constraints, f"{clause} already in constraints."
            assert -clause not in self.constraints, f"{-clause} already in constraints."

            if clause >= 0:
                self.answers.append([clause])

    def clear_answers(self) -> None:
        """Empties list of answers."""
        self.answers = []

    def get_all_clauses(self) -> CNFtype:
        """Return all clauses in the puzzle (rules + constraints + answers)."""
        return self.base_rules + self.constraints + self.answers

    def get_satisfaction(self) -> np.bool_:
        """Check if puzzle is satisfied with the given answers.

        Returns:
            bool: boolean stating True if satisfied.
        """
        # This runs _get_clause_satisfaction for every clause in base_rules
        satisfactions = np.fromiter(
            map(self._get_clause_satisfaction, self.base_rules), dtype=np.bool_
        )
        # Check if ALL clauses have returned True because these are joined by an AND
        satisfied = np.all(satisfactions)

        return satisfied

    def _get_clause_satisfaction(self, clause: List[int]) -> np.bool_:
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
