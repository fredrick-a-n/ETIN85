from sage.all import *
from LLL import LLL


def knapsack_density(values):
    '''
    values: list of integers
    N: knapsack value
    '''
    mm = max([log(v, 2) for v in values])
    return len(values) / mm


def solve_knapsack_lll(values, N, printline: bool = False):
    '''
    values: list of integers
    N: knapsack value
    '''
    print(
        f"Knapsack density: {knapsack_density(values)}") if printline else None
    m = len(values)
    A = matrix(QQ, m+1, m+1)

    for i in range(m):
        A[i, i] = 1
        A[m, i] = copy(values[i])
        A[i, m] = 1/2
    A[m, m] = N
    print(f"A = {A}") if printline else None
    B = LLL(A)
    print(f"B = {B}") if printline else None
    Ai = A.inverse()
    for i in range(m+1):
        y = B.column(i)
        print(f"y = {y}") if printline else None
        x = Ai * y
        print(f"x = {x}") if printline else None
        if x[m] == 0 or any([(xi > 0 if x[m] > 0 else xi < 0) for xi in x[:-1]]):
            continue
        v = x[m]
        x = x[:-1]
        x = [xi/-v for xi in x]
        return x

    return None