###pseudocode

# def dpll(X, literal):
#     remove clauses from X containing literal
#     shorten clauses from X containing not literal
#     if X contains no clauses:
#         return True;
#     if X contains empty clause:
#         return False;

#     choose P in X:
#     if (dpll(X , not P)):
#         return True;
  
#     return dpll(X, P)
#----------------------------------------------------------------------------

#Checking if there is a unit clause (only one literal clause) 
def check_unit_clause(cnf):
    for clause in cnf:
        if len(clause) == 1:
            return True
        return False
