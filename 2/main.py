from sage.all import *
from coppersmiths import coppersmiths


def solve_mod_poly(c, N, printline: bool=false):
    """
    c: coefficients of the polynomial, from the lowest degree to the highest
    N: modulus of the polynomial
    """
    R = PolynomialRing(ZZ, 'x')
    f = R(c)

    if printline:
        print(f"Trying to solve for N = {N} and f = {f}")

    cc = coppersmiths(c, N)

    if printline:
        print(f"Found solution: {cc}")

    Rmod = IntegerModRing(N)
    ccmod = cc.change_ring(Rmod)

    if printline:
        print(f"Solution mod N: {ccmod}")

    sol = ccmod.roots()
    for s in sol:
        if f(s[0]) % N == 0:
            return s[0]
    return None

def test_polynomial():
    N = 7
    c = [1, 1, 1]
    print("Solving for N = 7 and c = [1, 1, 1]")
    s = solve_mod_poly(c, N, True)
    return s
    
def toy_polynomial():
    N = 1073741827
    c = [507878743171, 9003, 1]
    print("Solving for N = 1073741827 and c = [507878743171, 9003, 1]")
    s = solve_mod_poly(c, N, True)
    return s
    

if __name__ == '__main__':
    print(f"Root: {test_polynomial()}")
    print(f"Root: {toy_polynomial()}") 

