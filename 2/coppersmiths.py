import sympy as sp
from sympy.polys.polytools import Poly
from LLL import LLL

def g(u,v,N,m,f,x):
    """
    u: integer
    v: integer
    N: modulus
    m: integer
    f: sympy polynomial
    """
    p = N**(m-v) 
    return p * Poly(x**u,x) * f**v


def coppersmiths(c, N):
    """
    c: coefficients of the polynomial, from the lowest degree to the highest
    N: modulus of the polynomial
    """    

    x = sp.symbols('x')
    f = Poly.from_list(c, gens=x)
    d = f.degree()
    m = d
    X = int(N**(1/d)) 

    while True:
        print(f"Trying with X = {X}, m = {m}, d = {d}, N = {N}, f = {f}")

        gs = [] # list of g(u,v)
        for v in range(0, m+1):
            for u in range(0, d):
                gs.append(g(u,v,N,m,f,x))

        max_degree = max(sp.degree(gi) for gi in gs) + 1
        A = sp.zeros(len(gs), max_degree)
        
        # construct the lattice
        for i, gi in enumerate(gs):
            coef = gi.all_coeffs()
            coef = [c for c in reversed(coef)]
            # apply X*x
            for j in range(len(coef)):
                A[i, j] = coef[j] * X**j

        # LLL reduction
        B = LLL(A)
        u = A.inv() * B[:,0]
        h = sum(Poly(u[i],x) * gs[i] for i in range(len(u)))

        print(f"Solution h: {h}")

        # Check that the polynomial is not a constant
        if len(h.free_symbols) == 0:
            X = X+1
            continue
        else:
            return h
 