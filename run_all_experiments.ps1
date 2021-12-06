$heuristics = "dlis", "dlcs", "random", "weighted", "jw", "jwtwo", "moms", "mams"
$n_max = 100

foreach ($heuristic in $heuristics) {
    python ./run_experiment.py "test_sudokus/4x4.txt" --heuristic $heuristic --grid 4 --n_max $n_max
    python ./run_experiment.py "test_sudokus/1000 sudokus.txt" --heuristic $heuristic --grid 9 --n_max $n_max
    python ./run_experiment.py "test_sudokus/Sudokus_Rated.txt" --heuristic $heuristic --grid 9 --repeat 20 --ids "test_sudokus\Sudokus_Difficulty.txt"
    python ./run_experiment.py "test_sudokus/16x16.txt" --heuristic $heuristic --grid 16 --n_max 32
}
