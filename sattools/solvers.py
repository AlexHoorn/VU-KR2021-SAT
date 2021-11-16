from copy import deepcopy
from typing import Iterable, List, Optional, Set

import numpy as np

from .utils import CNFtype, flatten_list


class SolverBase:
    def __init__(self, cnf: CNFtype, verbose=False) -> None:
        self.cnf = cnf
        self.verbose = verbose

        self.literals = self.determine_literals(cnf)
        self.satisfied = False
        self.solution = []

    def set_solution(self, solution: Iterable[int]):
        """Set the solution"""
        self.solution = list(solution)

    @staticmethod
    def determine_literals(cnf: CNFtype) -> Set[int]:
        """Determine all unique literals"""
        return set(np.unique(flatten_list(cnf)))

    @staticmethod
    def determine_unit_clauses(cnf: CNFtype) -> List[int]:
        """Return the pure literals in a cnf"""
        # Count the amount of literals in every clause
        clause_lenghts = np.fromiter(map(len, cnf), dtype=np.int_)
        # Keep clauses with count == 1
        literals = np.array(cnf, dtype=np.object_)[clause_lenghts == 1]
        # Literals in now an array with lists of single clauses, flatten this
        literals = flatten_list(literals)

        return literals

    @staticmethod
    def remove_literal(cnf: CNFtype, literal: int):
        cnf = deepcopy(cnf)
        cnf = SolverBase.remove_clauses_with_literal(cnf, literal)
        cnf = SolverBase.shorten_clauses_with_literal(cnf, -literal)

        return cnf

    @staticmethod
    def remove_clauses_with_literal(cnf: CNFtype, literal: int):
        """Remove clauses from the cnf with the given literal"""
        return [clause for clause in cnf if literal not in clause]

    @staticmethod
    def shorten_clauses_with_literal(cnf: CNFtype, literal: int):
        """Shorten clauses from cnf with given literal"""
        return [[c for c in clause if c != literal] for clause in cnf]


class DPLL(SolverBase):
    def __init__(self, cnf: CNFtype, verbose=False) -> None:
        super().__init__(cnf, verbose)
        self.backtrack_count = 0

    def solve(self) -> None:
        """Kick off solving algorithm"""

        if self.backtrack(self.cnf, set(), None):
            self.satisfied = True
        else:
            self.satisfied = True

        if self.verbose:
            if self.satisfied:
                print("Satisfied")
            else:
                print("Cannot satisfied")

    def backtrack(
        self,
        cnf: CNFtype,
        partial_assignment: Optional[Set[int]],
        literal: Optional[int],
    ) -> bool:
        # Print some information every 100 backtracks
        if self.verbose:
            if self.backtrack_count % 100 == 0:
                info_strings = [
                    f"{self.backtrack_count = }",  # amount of backtracks
                    f"{len(partial_assignment) = }",  # amount of assignments
                    f"{len(cnf) = }",  # length of unsolved cnf
                ]
                print(", ".join(info_strings))

        # Keep the count of backtracks
        self.backtrack_count += 1

        # Determine unit clauses
        unit_clauses = set(self.determine_unit_clauses(cnf))
        # Remove pure literals from cnf
        for unit_clause in unit_clauses:
            cnf = self.remove_literal(cnf, unit_clause)

        # Copy partial assignments so parent doesn't get overwritten when changed
        partial_assignment = deepcopy(partial_assignment)
        # Add unit clauses to partial assignment
        partial_assignment = partial_assignment | unit_clauses

        # Add selected literal to partial assignment and remove from cnf
        if isinstance(literal, int):
            partial_assignment.add(literal)
            cnf = self.remove_literal(cnf, literal)

        # Finish if cnf contains no clauses: satisfied
        if len(cnf) == 0:
            self.set_solution(partial_assignment)
            return True

        # Stop if cnf contains empty clauses: unsatisfied
        elif np.isin(0, np.fromiter(map(len, cnf), dtype=np.int_)):
            return False

        # Pick a random literal without considering those already in partial assignment
        literal = int(np.random.choice(list(self.literals - partial_assignment)))

        # Try negation of the picked literal
        if self.backtrack(cnf, partial_assignment, -literal):
            return True

        # Try picked value
        return self.backtrack(cnf, partial_assignment, literal)
