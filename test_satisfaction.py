# I wrote this to check whether the sudoku satisfaction check is correct.
# This uses an external solver from python-sat to get the correct answers.

# %%
from pysat.solvers import Glucose3
from sudoku import read_dimacs

g = Glucose3()

sudoku_rules = read_dimacs("sudoku-rules.txt")
sudoku_example = read_dimacs("sudoku-example.txt")

for clause in sudoku_rules + sudoku_example:
    g.add_clause(clause)

print(f"{g.solve() = }")

with open("sudoku-example-answer.txt", "w") as f:
    for v in g.get_model():
        if v > 0 and [v] not in sudoku_example:
            f.write(f"{v} 0\n")


# %%
from sudoku import Sudoku

sudoku_answers = read_dimacs("sudoku-example-answer.txt")

s = Sudoku("sudoku-example.txt")
for a in sudoku_answers:
    s.add_answer(a)

print(f"{s.get_satisfaction() = }")
