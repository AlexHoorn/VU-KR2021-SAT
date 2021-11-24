import random
from typing import Counter, Iterable, List, Set, Tuple, Union

import numpy as np

from .utils import CNFtype, flatten_list
from time import time


class Solver:
    def __init__(self, cnf: CNFtype, verbose=False) -> None:
        self.cnf = cnf
        self.verbose = verbose

        self.literals = self.determine_literals(cnf)
        self.satisfied = False
        self.solution: List[int] = []

    def solve(self) -> None:
        """Kick off solving algorithm"""
        duration = time()
        self.satisfied = self.start()
        duration = time() - duration

        self.solve_duration = duration

        if self.verbose:
            if self.satisfied:
                print("Satisfied")
            else:
                print("Cannot satisfied")

    def start(self) -> bool:
        # NOTE: Implement this function in subclass
        raise NotImplementedError

    def set_solution(self, solution: Iterable[int]):
        """Set the solution"""
        self.solution = list(solution)

    @staticmethod
    def determine_literals(cnf: CNFtype) -> Set[int]:
        """Determine all unique literals"""
        return set(abs(literal) for literal in flatten_list(cnf))

    @classmethod
    def get_literal_random(cls, cnf: CNFtype) -> int:
        """Randomly select a single literal"""
        literals = cls.determine_literals(cnf)
        random_literal = random.choice(list(literals))

        return random_literal

    @classmethod
    def get_literal_random_weighted(cls, cnf: CNFtype) -> int:
        """Randomly select a single literal. This is weighted, i.e.
        variable that occurs more often has a higher chance."""
        literals = flatten_list(cnf)
        random_literal = random.choice(literals)

        return random_literal

    @classmethod
    def get_literal_random_weighted_abs(cls, cnf: CNFtype) -> int:
        """Randomly select a non-negated single literal. This is weighted, i.e.
        variable that occurs more often has a higher chance."""
        literals = flatten_list(cnf)
        literals = [abs(literal) for literal in literals]
        random_literal = random.choice(literals)

        return random_literal

    # TODO: This is not the exact implementation of GSAT but represents roughly how it works
    @classmethod
    def get_literal_greedy(cls, cnf: CNFtype) -> int:
        units = flatten_list(cnf)
        count = Counter(units)
        most_common = [unit for unit, _ in count.most_common()]
        literal = random.choice(most_common)

        return literal

    @classmethod
    def determine_pure_literals(cls, cnf: CNFtype) -> Set[int]:
        """Determine all pure literals"""
        unique_literals = set(flatten_list(cnf))
        # Keep a set of literals when their negation isn't present
        # FYI: { } does a set comprehension
        pure_literals = {ul for ul in unique_literals if -ul not in unique_literals}

        return pure_literals

    @staticmethod
    def determine_unit_clauses(cnf: CNFtype) -> Set[int]:
        """Return the unit clauses in a cnf"""
        return {clause[0] for clause in cnf if len(clause) == 1}

    @classmethod
    def remove_literal(cls, cnf: CNFtype, literal: int):
        # Remove clauses with literal
        cnf = cls.remove_clauses_with_literal(cnf, literal)
        # Shorten clauses with negated literal
        cnf = cls.shorten_clauses_with_literal(cnf, -literal)

        return cnf

    @staticmethod
    def remove_clauses_with_literal(cnf: CNFtype, literal: int):
        """Remove clauses from the cnf with the given literal"""
        return [clause for clause in cnf if literal not in clause]

    @staticmethod
    def shorten_clauses_with_literal(cnf: CNFtype, literal: int):
        """Shorten clauses from cnf with given literal"""
        return [[c for c in clause if c != literal] for clause in cnf]

    # NOTE: This doesn't implement the tautology rule
    @classmethod
    def simplify(cls, cnf: CNFtype) -> Tuple[CNFtype, Set[int]]:
        """Remove unit clauses and pure literals, return new cnf and removed literals"""
        # Determine unit clauses
        unit_clauses = cls.determine_unit_clauses(cnf)
        # Determine pure literals
        pure_literals = cls.determine_pure_literals(cnf)

        remove_literals = unit_clauses | pure_literals

        # Remove pure literals from cnf
        for literal in remove_literals:
            cnf = cls.remove_literal(cnf, literal)

        return cnf, remove_literals

    @staticmethod
    def check_satisfaction(cnf: CNFtype) -> Union[bool, None]:
        # Satisfied is CNF contains no clauses
        if len(cnf) == 0:
            return True

        # Unsatisfied if CNF contains empty clauses
        if np.isin(0, np.fromiter(map(len, cnf), dtype=np.int_)):
            return False

        return None


class DPLL(Solver):
    def __init__(self, cnf: CNFtype, verbose=False, heuristic="random") -> None:
        super().__init__(cnf, verbose=verbose)

        heuristic_techniques = ["random", "weighted", "weighted_abs", "greedy"]
        assert (
            heuristic in heuristic_techniques
        ), f"heuristic must be one of {heuristic_techniques}"
        self.heuristic = heuristic

    def start(self) -> bool:
        # Allows keeping count of backtracks and propagations
        self.backtrack_count = 0
        self.propagation_count = 0

        return self.backtrack(self.cnf, partial_assignment=set())

    def backtrack(self, cnf: CNFtype, partial_assignment: Set[int],) -> bool:
        # Print some information every so often
        if self.verbose and self.propagation_count % 10 == 0:
            info_strings = [
                f"{self.propagation_count:5} propagations",  # amount of function propagations
                f"{self.backtrack_count:5} backtracks",  # amount of backtracks
                f"{len(partial_assignment):5} assignment size",  # amount of assignments
                f"{len(cnf):5} cnf size",  # length of unsolved cnf
            ]
            print(", ".join(info_strings))

        # Increase propagation count
        self.propagation_count += 1

        # Simplify cnf
        cnf, removed_literals = self.simplify(cnf)
        # Add removed literals from simplification
        partial_assignment = partial_assignment | removed_literals

        # Finish if cnf contains no clauses: satisfied
        if len(cnf) == 0:
            self.set_solution(partial_assignment)
            return True

        # Stop if cnf contains empty clauses: unsatisfied
        if np.isin(0, np.fromiter(map(len, cnf), dtype=np.int_)):
            # Keep the count of backtracks
            self.backtrack_count += 1
            return False

        if self.heuristic == "random":
            literal = self.get_literal_random(cnf)
        elif self.heuristic == "weighted":
            literal = self.get_literal_random_weighted(cnf)
        elif self.heuristic == "weighted_abs":
            self.literals = self.get_literal_random_weighted_abs(cnf)
        elif self.heuristic == "greedy":
            literal = self.get_literal_greedy(cnf)

        # Try negation of the picked literal
        satisfied = self.backtrack(
            self.remove_literal(cnf, -literal), partial_assignment | set([-literal])
        )

        if not satisfied:
            # Try non-negated picked value
            satisfied = self.backtrack(
                self.remove_literal(cnf, literal), partial_assignment | set([literal])
            )

        return satisfied
