from typing import List


class Sudoku:
    def __init__(self) -> None:
        self.base_rules = self.get_base_rules()

    def get_base_rules(self) -> List:
        with open("sudoku-rules.txt") as f:
            rules = f.readlines()

        rule_clauses = []
        for clause in rules:
            if clause[0] in ("p", "c"):
                ...

            else:
                clause = clause.rstrip(" 0\n")
                clause = clause.split(" ")
                rule_clauses.append(clause)

        return rule_clauses
