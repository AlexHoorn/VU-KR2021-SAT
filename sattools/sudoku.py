from os import path
from typing import Iterator, List, Union

from .solvers import Solver
from .utils import CNFtype, read_dimacs


class Sudoku:
    def __init__(self, sudoku: Union[str, CNFtype], rules="9x9") -> None:
        """Implements the Sudoku puzzle."""
        self.base_rules = read_dimacs(filepath=self.get_rules_filepath(rules))

        if isinstance(sudoku, str):
            self.constraints = read_dimacs(filepath=sudoku)
        elif isinstance(sudoku, list):
            self.constraints = sudoku

        self.answers: CNFtype = []

        self.validate_clauses()

    def __iter__(self) -> Iterator[List[int]]:
        """Iterator that makes iterating over all clauses easy with e.g. `for clause in sudoku`."""
        clauses = self.get_all_clauses()
        for c in clauses:
            yield c

    def __getitem__(self, idx):
        return self.get_all_clauses()[idx]

    def get_rules_filepath(self, rules: str) -> str:
        filepath = path.join(path.dirname(__file__), "sudoku_rules", f"{rules}.txt")
        return filepath

    def add_answer(self, clauses: Union[List[int], int]) -> None:
        """Add answer to puzzle."""
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

    def validate_clauses(self):
        clauses = self.get_all_clauses()
        for clause in clauses:
            assert isinstance(
                clause, set
            ), f"found clause {clause} with type {type(clause)}"
            for unit in clause:
                assert isinstance(
                    unit, int
                ), f"found unit {unit} with type {type(unit)}"
