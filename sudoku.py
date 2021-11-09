from typing import List
import numpy as np


class Sudoku:
    def __init__(self, filename: str) -> None:
        self.base_rules = self.get_base_rules()
        self.constraints = read_dimacs(filename=filename)

        self.answers: List[int] = []

    def get_base_rules(self, filename="sudoku-rules.txt") -> List:
        return read_dimacs(filename=filename)

    def add_answer(self, clause):
        if clause not in self.constraints:
            self.answers.append(clause)

    def clear_answers(self):
        self.answers = []

    def get_all_clauses(self):
        return self.base_rules + self.constraints + self.answers

    def check_satisfied(self):
        rules, negatives = self._get_map(self.base_rules)
        clauses_boolean = list(map(self._map_value, rules, negatives))
        clauses_boolean = list(map(np.any, clauses_boolean))

        return np.all(clauses_boolean)

    def _get_map(self, clauses):
        values = [[abs(v) for v in c] for c in clauses]
        negatives = [[v < 0 for v in c] for c in clauses]

        return values, negatives

    def _map_value(self, values, negatives):
        clause = np.isin(values, self.constraints + self.answers)
        clause = np.where(negatives, clause, ~clause)

        return clause


def read_dimacs(filename: str) -> List:
    with open(filename) as f:
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
