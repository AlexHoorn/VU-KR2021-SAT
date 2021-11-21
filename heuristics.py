###Needs to be edited, Taken from https://github.com/Timm877/KR2020_Sudoku_solver_SAT/blob/master/sudoku_heuristics.py

import random
import sys
import itertools

######################################################################################################
# Splitting heuristics:
# RANDOM
######################################################################################################
# DLCS (Dynamic Largest Combined Sum):
#   - Pick v with largest CP(v)+CN(v) (= most frequent v)
#   - If CP(v)>CN(v) then v=1 else v=0
######################################################################################################
# DLIS (Dynamic Largest Individual Sum)
# •Pick v with largest CP(v) or largest CN(v)
# •If CP(v)>CN(v) then v=1 else v=0
######################################################################################################
# Compute for every clause ω and every variable l  (in each phase):
# J(l) := Σ((2)^(-|ω|)) ∀l ∈ ω
# Choose a variable l that maximizes J(l).
# Which means that this strategy gives an exponentially higher weight to literals in shorter clauses.
###
from typing import List, Any


def branching_heuristics_collection(heuristic):
    try:
        return branching_heuristics[heuristic]
    except:
        sys.exit("ERROR: '{}' Unknown/Unimplemented branching heuristic.".format(heuristic) +
                 "\nImplemented heuristics: {}".format(branching_heuristics.keys()))


def most_common_literal_negative(cnf_formula):
    # Returns the negative of literal that occurs the most in cnf
    merged = list(itertools.chain(*cnf_formula))
    return max(set(merged), key=merged.count) * -1


def get_literal_occurrence_frequency(cnf_formula):
    merged = list(itertools.chain.from_iterable(cnf_formula))
    x = [item for item in merged]
    return max(set(x), key=x.count)


def get_absolute_literal_occurrence_frequency(cnf_formula):
    merged = list(itertools.chain.from_iterable(cnf_formula))
    x = [abs(item) for item in merged]
    return max(set(x), key=x.count)


def get_weighted_frequency(cnf_formula, weight=2, is_absolute=False):
    counter = {}
    for clause in cnf_formula:
        if (is_absolute): literal = abs(literal)
        for literal in clause:
            if literal in counter:
                counter[literal] += weight ** -len(clause)
            else:
                counter[literal] = weight ** -len(clause)
    return counter


def get_difference_counter(formula):
    counter = {}
    for clause in formula:
        for literal in clause:
            if literal in counter:
                if literal > 0:
                    counter[literal] += 1
                else:
                    counter[-literal] += - 1
            else:
                if literal > 0:
                    counter[literal] = 1
                else:
                    counter[-literal] = - 1
    return counter


def random_selection(cnf_formula):
    return random.choice(unique_literals(cnf_formula))


def unique_literals(cnf_formula: list()):
    unique_values = list(set(x for l in cnf_formula for x in l))
    return unique_values


### JEROSLOW-WANG
# Compute for every clause ω and every variable l  (in each phase):
# J(l) := Σ((2)^(-|ω|)) ∀l ∈ ω
# Choose a variable l that maximizes J(l).
# Which means that this strategy gives an exponentially higher weight to literals in shorter clauses.
###
def jeroslow_wang(cnf_formula):
    counter = get_weighted_frequency(cnf_formula)
    return max(counter, key=counter.get)


def jeroslow_wang_two_sided(formula):
    counter = get_weighted_frequency(formula, True)
    return max(counter, key=counter.get)


def dynamic_largest_individual_sum(cnf_formula):
    return get_literal_occurrence_frequency(cnf_formula)


def dynamic_largest_combined_sum(cnf_formula):
    return get_absolute_literal_occurrence_frequency(cnf_formula)


branching_heuristics = {
    'RANDOM': random_selection,
    'DLCS': dynamic_largest_combined_sum,  # AKA: most frequent (unsigned) variable
    'DLIS': dynamic_largest_individual_sum,
    'JEROSLOW_WANG': jeroslow_wang,
    'JEROSLOW_WANG_TWO_SIDED': jeroslow_wang_two_sided,
    'DLIS_negated': most_common_literal_negative
}
heuristic_list = list(branching_heuristics.keys())
