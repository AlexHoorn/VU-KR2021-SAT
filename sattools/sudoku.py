from os import path
from typing import Union

from .utils import CNFtype, read_dimacs


class Sudoku:
    def __init__(self, sudoku: Union[str, CNFtype], rules="9x9") -> None:
        """Implements the Sudoku puzzle."""
        self.base_rules = read_dimacs(filepath=self.get_rules_filepath(rules))

        if isinstance(sudoku, str):
            self.constraints = read_dimacs(filepath=sudoku)
        elif isinstance(sudoku, list):
            self.constraints = sudoku

    def get_rules_filepath(self, rules: str) -> str:
        filepath = path.join(path.dirname(__file__), "sudoku_rules", f"{rules}.txt")
        return filepath

    def get_all_clauses(self) -> CNFtype:
        """Return all clauses in the puzzle (rules + constraints + answers)."""
        return self.base_rules + self.constraints
