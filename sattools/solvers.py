from collections import Counter
from typing import List

import numpy as np

from .utils import CNFtype, flatten_list


class SolverBase:
    def __init__(self, cnf: CNFtype) -> None:
        self.input_cnf = cnf

    def remove_clauses(self, cnf: CNFtype, clauses: CNFtype) -> CNFtype:
        """Function that removes `clauses` from given `cnf`"""
        cnf_array = np.array(cnf, dtype=np.object_)
        clauses_array = np.array(clauses, dtype=np.object_)
        to_remove = np.isin(cnf_array, clauses_array)

        cnf_removed = list(cnf_array[~to_remove])

        return cnf_removed

    def determine_literals(self, cnf: CNFtype) -> List[int]:
        values = flatten_list(cnf)
        value_counts = Counter(values)

        pure_literals = []
        for value in value_counts.keys():
            if -value not in value_counts.keys():
                pure_literals.append(value)

        return pure_literals

