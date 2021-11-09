from typing import List


class Sudoku:
    def __init__(self) -> None:
        self.base_rules = self.get_base_rules()

    def get_base_rules(self) -> List:
        
        #function to read dimacs files
        def read_dimacs(self) -> List:
            my_txt='sudoku-example.txt'
            with open(my_txt) as s:
                my_d=s.readlines()
            
            sudo_list=[]    
            for row in my_d:
                row = row.rstrip(" 0\n")
                row = row.split(" ")
                sudo_list.append(row)
            return sudo_list
        
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
