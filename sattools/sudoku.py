from typing import Iterator, List, Union

from .solvers import Solver
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

            self.answers.append([clause])

    def clear_answers(self) -> None:
        """Empties list of answers."""
        self.answers = []

    def get_all_clauses(self) -> CNFtype:
        """Return all clauses in the puzzle (rules + constraints + answers)."""
        return self.base_rules + self.constraints + self.answers

    def get_satisfaction(self) -> bool:
        """Check if puzzle is satisfied with the given answers."""
        cnf = self.get_all_clauses()
        cnf, _ = Solver.simplify(cnf)
        satisfied = Solver.check_satisfaction(cnf)

        # check_satisfaction(...) returns either True is satisfied, False if not satisfiable or None
        # if it can be further reduced. This makes sure either simply True or False is returned
        return bool(satisfied)
