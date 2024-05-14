from sage.all import *
from coppersmiths import coppersmiths
from knapsack import solve_knapsack_lll
from LLL import check_orthogonal, check_LLL_condition, LLL, gram_schmidt

def test_gram_schmidt():
    B = matrix(ZZ, [[2,1],[0,1]])
    print(f"Matrix B: \n{B}")
    print(f"Orthogonal: {check_orthogonal(B)}")
    Bs = gram_schmidt(B)
    print(f"Orthogonalized B: \n{Bs}")
    print(f"Orthogonal: {check_orthogonal(Bs)}")

def test_gram_schmidt2():
    B = matrix(ZZ, [[1,-1,3],[1,0,5],[1,2,6]])
    print(f"Matrix B: \n{B}")
    print(f"Orthogonal: {check_orthogonal(B)}")
    Bs = gram_schmidt(B)
    print(f"Orthogonalized B: \n{Bs}")
    print(f"Orthogonal: {check_orthogonal(Bs)}")

def test_LLL():
    B = matrix(ZZ, [[2,1],[0,1]])
    print(f"Matrix B: \n{B}")
    print(f"LLL condition: {check_LLL_condition(B)}")
    B = LLL(B)
    print(f"Reduced B: \n{B}")
    print(f"LLL condition: {check_LLL_condition(B)}")

def test_LLL2():
    B = matrix(ZZ, [[1,-1,3],[1,0,5],[1,2,6]])
    print(f"Matrix B: \n{B}")
    print(f"LLL condition: {check_LLL_condition(B)}")
    B = LLL(B)
    print(f"Reduced B: \n{B}")
    print(f"LLL condition: {check_LLL_condition(B)}")


def solve_mod_poly(c, N, printline: bool = false):
    """
    c: coefficients of the polynomial, from the lowest degree to the highest
    N: modulus of the polynomial
    """
    R = PolynomialRing(ZZ, 'x')
    f = R(c)

    print(f"Trying to solve for N = {N} and f = {f}") if printline else None

    cc = coppersmiths(c, N)

    print(f"Found solution: {cc}") if printline else None

    Rmod = IntegerModRing(N)
    ccmod = cc.change_ring(Rmod)

    print(f"Solution mod N: {ccmod}") if printline else None

    sol = ccmod.roots()
    sol = sorted(sol, key=lambda x: x[0])
    for s in sol:
        if f(s[0]) % N == 0:
            return s[0]
    return None


def test_polynomial():
    N = 7
    c = [1, 1, 1]
    print("Solving for N = 7 and c = [1, 1, 1]")
    s = solve_mod_poly(c, N, True)
    
    print(f"Solution: {s}")


def toy_polynomial():
    N = 1073741827
    c = [507878743171, 9003, 1]
    print("Solving for N = 1073741827 and c = [507878743171, 9003, 1]")
    s = solve_mod_poly(c, N, True)

    print(f"Solution: {s}")


def test_knapsack():
    values = [62, 93, 81, 88, 102, 37]
    N = 174

    print(f"Solving for N = {N} and values = {values}")
    s = solve_knapsack_lll(values, N, True)

    print(f"Knapsack composition: {s}")

    k = sum([values[i] * s[i] for i in range(len(values))])

    print(f"Sum of solved knapsack composition: {k}")

def test_knapsack2():
    values = [367, 272, 1753, 708, 17, 1623, 1562, 978]
    N = 3003

    print(f"Solving for N = {N} and values = {values}")
    s = solve_knapsack_lll(values, N, True)

    print(f"Knapsack composition: {s}")

    k = sum([values[i] * s[i] for i in range(len(values))])

    print(f"Sum of solved knapsack composition: {k}")


def knapsack():
    values = [864197523, 1728395046, 3580246881, 7407407340, 6210443074, 3939971331, 8497226607, 8760451975, 435617527, 1858889366, 4828889833, 1917605583, 5193235845, 2893211185, 7391360627, 7536374327, 7949858516, 8900283683, 1949848833, 6121919868, 5614776754, 4723947315, 3065745226, 8847539810, 2585101821, 8133166578, 1403268935, 6016414384, 6391420098, 7264888315, 160539565]
    N = 54145346795

    print(f"Solving for N = {N} and values = {values}")
    s = solve_knapsack_lll(values, N, True)
    
    print(f"Knapsack composition: {s}")

    k = sum([values[i] * s[i] for i in range(len(values))])

    print(f"Sum of solved knapsack composition: {k}")


if __name__ == '__main__':
    test_gram_schmidt()
    # test_gram_schmidt2()
    # test_LLL()
    # test_LLL2()
    # test_polynomial()
    # toy_polynomial()
    # test_knapsack()
    # test_knapsack2()
    # knapsack()
