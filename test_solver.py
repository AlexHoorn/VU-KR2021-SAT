# %%
from sattools.solvers import DPLL
from sattools.sudoku import Sudoku
from sattools.utils import read_dimacs, write_dimacs

s = Sudoku("sudoku-example.txt")

cnf = s.get_all_clauses()
dpll = DPLL(cnf, verbose=True)

print("Solving cnf")
dpll.solve()

if dpll.satisfied:
    print(f"Solution\n {dpll.solution=}")

    write_dimacs(dpll.solution, "sudoku-example-answer-custom.txt")
    answers = read_dimacs("sudoku-example-answer-custom.txt")

    s.add_answer(answers)
    print(
        "Sudoku satisfied = ", s.get_satisfaction()
    )  # this function seems broken, keep that in mind

else:
    print("Couldn't find satisfaction")

print(f"Backtracks = {dpll.backtrack_count}")
