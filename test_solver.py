# %%
from collections import Counter

from sattools.solvers import DPLL
from sattools.sudoku import Sudoku
from sattools.utils import flatten_list, read_dimacs, write_dimacs

import cProfile
import pstats
import io

profiler = cProfile.Profile()
profiler.enable()

s = Sudoku("sudoku-example.txt")

cnf = s.get_all_clauses()
dpll = DPLL(cnf, verbose=True, heuristic="weighted")

print("Solving cnf")
dpll.solve()

if dpll.satisfied:
    print(f"Solution length = {len(dpll.solution)}")

    write_dimacs(dpll.solution, "sudoku-example-answer-custom.txt")
    answers = flatten_list(read_dimacs("sudoku-example-answer-custom.txt"))

    s.add_answer(answers)

    print("Sudoku satisfied =", s.get_satisfaction())

else:
    print("Couldn't find satisfaction")

print(
    f"Backtracks = {dpll.backtrack_count}, propagations = {dpll.propagation_count}, {dpll.solve_duration = :.2f}s"
)

answers = [a for a in answers if a >= 0]

count = Counter([str(a)[:2] for a in answers])

for pos, i in count.items():
    assert i == 1, f"position {pos}, has {i} answers"

print("Answer is valid")

profiler.disable()
stream = io.StringIO()
ps = pstats.Stats(profiler, stream=stream).sort_stats("tottime")
ps.print_stats()

with open("profiled.txt", "w+") as f:
    f.write(stream.getvalue())
