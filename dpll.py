#pseudocode, not sure how to integrade it with the rest of the code yet

def dpll(X, literal):
    remove clauses from X containing literal
    shorten clauses from X containing not literal
    if X contains no clauses:
        return True;
    if X contains empty clause:
        return False;

    choose P in X:
    if (dpll(X , not P)):
        return True;
  
    return dpll(X, P)
