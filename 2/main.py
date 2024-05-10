import sympy as sp
from sympy.polys.polytools import Poly
from coppersmiths import coppersmiths

def test_polynomial():
    x = sp.symbols('x')
    f = Poly(x**2 + x + 1)
    N = 7
    c = f.all_coeffs()
    cc = coppersmiths(c, N)
    cc = Poly([coeff % N for coeff in cc.all_coeffs()],x)
    print (cc)
    sol = sp.solve(cc.as_expr(), x)
    
    return sol
    
def toy_polynomial():
    x = sp.symbols('x')
    f = Poly(x**2 + 9003*x + 507878743171)
    N = 1073741827
    c = f.all_coeffs()
    cc = coppersmiths(c, N)
    cc = Poly([coeff % N for coeff in cc.all_coeffs()],x)
    print (cc)
    sol = sp.solveset(sp.Mod(cc.as_expr(), N), x, domain=sp.S.Integers)
    
    return sol

if __name__ == '__main__':
    print(test_polynomial())

