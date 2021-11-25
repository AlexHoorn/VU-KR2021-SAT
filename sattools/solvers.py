import random
from time import time
from typing import Any, Callable, Counter, Iterable, List, Optional, Set, Tuple, Union

import numpy as np

from .utils import CNFtype, flatten_list, neg_abs


class Solver:
    def __init__(
        self, cnf: CNFtype, verbose=False, identifier: Optional[Any] = None
    ) -> None:
        self.cnf = cnf
        self.verbose = verbose

        self.literals = self.determine_literals(cnf)
        self.satisfied = False
        self.solution: List[int] = []

        # Helps identifying a solution after using unordered multiprocessing
        self.identifier = identifier

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
    def get_literal_weighted(cls, cnf: CNFtype) -> int:
        """Randomly select a single literal. This is weighted, i.e.
        variable that occurs more often has a higher chance."""
        literals = flatten_list(cnf)
        random_literal = random.choice(literals)

        return random_literal

    @classmethod
    def get_literal_dlis(cls, cnf: CNFtype) -> int:
        units = flatten_list(cnf)
        count = Counter(units)
        most_common = [unit for unit, _ in count.most_common()]
        literal = random.choice(most_common)

        return literal

    # greatest combined sum
    @classmethod
    def get_literal_dlcs(cls, cnf: CNFtype) -> int:
        units = flatten_list(cnf)
        units_abs = [abs(unit) for unit in units]

        count = Counter(units_abs)
        literal = random.choice([unit for unit, _ in count.most_common()])

        if units.count(literal) > units.count(literal * -1):
            return literal

        return literal * -1

    # jeroslaw wang one-sided
    @classmethod
    def get_literal_jw(cls, cnf: CNFtype) -> int:
        """ set two_sided = True for two sided JW heuristic"""
        counter = {}
        for clause in cnf:
            # check for one/two sided
            for literal in clause:
                if literal in counter:
                    counter[literal] += 2 ** -len(clause)
                else:
                    counter[literal] = 2 ** -len(clause)


        return max(counter, key=counter.get)

    # Jeroslaw Wang two-sided
    @classmethod
    def get_literal_jwtwo(cls, cnf: CNFtype) -> int:
        """ set two_sided = True for two sided JW heuristic"""

        counter = {}
        for clause in cnf:
            # check for one/two sided
            clause = [abs(literal) for literal in clause]

            for literal in clause:
                if literal in counter:
                    counter[literal] += 2 ** -len(clause)
                else:
                    counter[literal] = 2 ** -len(clause)

        # for two_sided we know only which variable
        max_var = max(counter, key=counter.get)
        counter = {max_var: 0, max_var * -1: 0}

        for clause in cnf:
            if max_var in clause:
                counter[max_var] += 2 ** -len(clause)
            if max_var * -1 in clause:
                counter[max_var * -1] += 2 ** -len(clause)

        return max(counter, key=counter.get)

    @staticmethod
    def determine_pure_literals(cnf: CNFtype) -> Set[int]:
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
    def __init__(
        self, cnf: CNFtype, verbose=False, identifier=None, heuristic="random"
    ) -> None:
        super().__init__(cnf, verbose=verbose, identifier=identifier)

        # To instantaneously triple the options offered a post action for every heuristic is possible
        # i.e. _neg makes sure the chosen literal is negated, _pos the opposite
        heuristics = ["random", "weighted", "dlis", "dlcs", "jw", "jwtwo"]
        heuristics_neg = [f"{h}_neg" for h in heuristics]
        heuristics_pos = [f"{h}_pos" for h in heuristics]

        heuristics = heuristics + heuristics_neg + heuristics_pos
        heuristics.sort()

        # This checks whether the chosen heuristic is allowed
        assert heuristic in heuristics, f"heuristic must be one of {heuristics}"

        # E.g. split "random_neg" into "random" and "neg", just "random" becomes "random" and None
        heuristic, *post = heuristic.split("_")

        # Store the function used to get a new literal, saves a lot of if-statements during solving
        self.get_literal = getattr(self, f"get_literal_{heuristic}")

        # Determine the action to take after a literal is chosen
        post_func: Optional[Callable]
        if post == "neg":
            post_func = neg_abs
        elif post == "pos":
            post_func = abs
        else:
            post_func = None

        # Saves a bunch of if-statements again
        self.get_literal_post = post_func

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

        # Get a new split based on chosen heuristic
        literal = self.get_literal(cnf)
        # Do a post action if set
        if self.get_literal_post:
            literal = self.get_literal_post(literal)

        # Try non-negation of the picked literal
        satisfied = self.backtrack(
            self.remove_literal(cnf, literal), partial_assignment | set([literal])
        )

        if not satisfied:
            # Try negated picked value
            satisfied = self.backtrack(
                self.remove_literal(cnf, -literal), partial_assignment | set([-literal])
            )

        return satisfied
