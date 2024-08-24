from elliptic_curve import *

curve = EllipticCurve(1, 4, 7, 1)

p1 = EllipticPoint(curve, 5, 6, 1)

print(p1)

p2 = p1.double()

print(p2)

p3 = p2.double()

print(p3)

p4 = -p3

print(p4)

p5 = EllipticPoint(curve, 6, 4, 1)

print(p5)

p6 = p5 + p4

print(p6)