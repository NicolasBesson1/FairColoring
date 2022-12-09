from mip import Model, xsum, BINARY, OptimizationStatus
import math


def min_fair_coloring(D, kappa):
    """
    Input: Digraph D = (V,A) on n := |V| vertices and m := |A| arcs (D is the incidence matrix of dimension n x m) as well as a parameter kappa
    Output: a minimum kappa-fair coloring of the vertices of D (assignment array of length n)
    
    """
    
    # Get parameters from incidence matrix
    n = len(D)
    m = len(D[0])
    Colors = [i for i in range(n)]
    a = [[0 for v in range(n)] for u in range(n)] # a represents the arcs
    for u in range(n):
        for v in range(n):
            for arc in range(m):
                if D[u][arc] == -1 and D[v][arc] == 1: # arc uv is in D
                    a[u][v] = 1
    B = -min(sum(D[v][arc] for arc in range(m) if D[v][arc] == -1) for v in range(n)) # for the Big M constraint
    
    # Initialize optimization model M (minimization by default)
    M = Model()
    
    # Create variables
    x = [ M.add_var(var_type=BINARY) for c in Colors ]
    y = [ [ M.add_var(var_type=BINARY) for c in Colors] for v in range(n) ]
    
    # Objective function
    M.objective = xsum(x[c] for c in Colors)
    
    # Add constraints
    for v in range(n):
        M += 1 == xsum(y[v][c] for c in Colors)
        for c in Colors:
            M += xsum(y[u][c] for u in range(n) if a[v][u] == 1) <= B*(1-y[v][c]) + math.floor((1/kappa)*(xsum(a[v][u] for u in range(n))))
            M += x[c] >= y[v][c]
    for c in Colors:
        if c < n-1:
            M += x[c] >= x[c+1]
    
    # Solve the problem
    status = M.optimize()
    
    # Interpret and return solution
    if status == OptimizationStatus.OPTIMAL:
        print('Optimal solution with {} colors found'.format(M.objective_value))
        coloring = [c for v in range(n) for c in Colors if x[c].x >= 0.99 and y[v][c].x >= 0.99]
        for v in range(n):
            print('Vertex ' + str(v) + ' is colored ' + str(coloring[v]))
        return coloring
    elif status == OptimizationStatus.NO_SOLUTION_FOUND:
        print('No feasible solution found, lower bound on the number of colors is: {}'.format(M.objective_bound))
        return None
    else:
        return None


# Test instance 1
D = [[-1, 0], [1, -1], [0, 1]] #leaving arcs have value -1, entering arcs have value 1
kappa = 2
min_fair_coloring(D, kappa)

# Test instance 2
D = [[-1, -1, -1, 0, 0, 0, 0, 0, 0], [1, 0, 0, -1, 0, 0, 0, 0, 0], [0, 1, 0, 0, -1, -1, 0, 0, 0], [0, 0, 1, 0, 0, 0, -1, 1, 0], [0, 0, 0, 1, 1, 0, 0, 0, -1], [0, 0, 0, 0, 0, 1, 1, -1, 1]] #leaving arcs have value -1, entering arcs have value 1
kappa = 3
min_fair_coloring(D, kappa)