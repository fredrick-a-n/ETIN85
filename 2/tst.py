from sage.all import *

def lambdaa(p1, p2, a1, a2, a3, a4, a6):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]

    if x1 == x2:
        return (3*x1**2 + 2*a2*x1 + a4 - a1*y1) / (2*y1 + a1*x1 + a3)
    else:
        return (y2 - y1) / (x2 - x1)
    
def mu(p1, p2, a1, a2, a3, a4, a6):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]

    if x1 == x2:
        return (-x1**3 + a4*x1 + 2*a6 - a3*y1) / (2*y1 + a1*x1 + a3)
    else:
        return (y1*x2 - y2*x1) / (x2 - x1)
    

def add(p1, p2, a1, a2, a3, a4, a6, mod):
    # y^2 + a1xy + a3y = x^3 + a2x^2 + a4x + a6
    R = IntegerModRing(mod)
    p1 = (R(p1[0]), R(p1[1]))
    p2 = (R(p2[0]), R(p2[1]))
    a1 = R(a1)
    a2 = R(a2)
    a3 = R(a3)
    a4 = R(a4)
    a6 = R(a6)

    l = lambdaa(p1, p2, a1, a2, a3, a4, a6)
    m = mu(p1, p2, a1, a2, a3, a4, a6)
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]

    x3 = l**2 + a1*l - a2 - x1 - x2
    y3 = -(l + a1) * x3 - m - a3

    return (x3, y3)

def group(p, a1, a2, a3, a4, a6, mod):
    R = IntegerModRing(mod)
    a1 = R(a1)
    a2 = R(a2)
    a3 = R(a3)
    a4 = R(a4)
    a6 = R(a6)
    p = (R(p[0]), R(p[1]))
    pa = []
    pc = p
    while pa.__contains__(pc) == False:
        pa.append(pc)
        pc = add(pc, p, a1, a2, a3, a4, a6, mod)
    return pa
        
