from sage.all import *
from LLL import LLL

def g(u, v, N, m, f, x):
    """
    u: integer
    v: integer
    N: modulus
    m: integer
    f: polynomial in SageMath
    """
    p = N**(m-v)
    return p * x**u * f**v

def coppersmiths(c, N):
    """
    c: coefficients of the polynomial, from the lowest degree to the highest
    N: modulus of the polynomial
    """    

    R = PolynomialRing(ZZ, 'x')
    x = R.gen()
    f = R(c)
    d = f.degree()
    m = d
    err = 0
    while True:
        X = int(N**(1/(d - err)))

        gs = [] # list of g(u,v)
        for v in range(m + 1):
            for u in range(d):
                gs.append(g(u, v, N, m, f, x))

        max_degree = max(gi.degree() for gi in gs) + 1
        A = matrix(ZZ, len(gs), max_degree)
        
        # construct the lattice
        for i, gi in enumerate(gs):
            coef = gi.coefficients(sparse=False)
            # apply X*x
            for j in range(len(coef)):
                A[i, j] = coef[j] * X**j

        # LLL reduction
        B = LLL(A)
        u = A.inverse() * B.column(0)
        h = sum(u[i] * gs[i] for i in range(len(u)))
        if h.degree() > 0: 
            return h
        else:
            err += 0.01
            if err > d:
                raise ValueError("Failed to find a solution")
            continue
