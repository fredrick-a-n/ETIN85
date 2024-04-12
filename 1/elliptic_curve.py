import galois
from sympy import primefactors
import random
import math

class EllipticCurve:
    def __init__(self, a:int, b:int, p: int, n: int):
        self.field_size = p ** n
        if len(primefactors(self.field_size)) > 1:
            raise ValueError("The field size must only have one prime factor!")
        if p <= 1 or n <= 0 or (p == 2 and n <= 1) :
            raise ValueError("The field must be of a larger degree than 2")
        self.F = galois.GF(self.field_size)
        self.a = self.F(a)
        self.b = self.F(b)
        self._0 = self.F(0)
        self._1 = self.F(1)
        self._2 = self.F(2 % p)
        self._3 = self.F(3 % p)
        self._4 = self.F(4 % p)
        self._8 = self.F(8 % p)
        self._2mulinverse = self.F(1) / self.F(2)
     
    # check y^2=x^3+axz^4+bz^6 over field F
    def is_projective_point_on_curve(self, x, y, z) -> bool:
        return (((y**2) == (x**3) + (self.a * x * z**4 )+ (self.b * z**6))
                or (x == self._0 and y == self._1 and z == self._0)) # point at infinity
        
    def __eq__(self, other) -> bool:
        if isinstance(other, EllipticCurve):
            return self.F == other.F and self.a == other.a and self.b == other.b
        else:
            return False
        
    def __str__(self) -> str:
        return f"y^2 = x^3 + {str(self.a)}xz^4 + {str(self.b)}z^6 over {str(self.F.properties)}"
    
    # naive implementation, can be very slow for big fields.
    def random_point(self):
        while True:
            x = self.F(random.randint(0, self.field_size-1))
            x_3 = x**3
            ax = self.a * x
            for z in range(1, self.field_size):
                z = self.F(z)
                z_2 = z**2
                z_4 = z_2**2
                rhs = x_3 + ax * (z_4) + self.b * (z_2*z_4)
                for y in range(self.field_size):
                    y = self.F(y)
                    if y**2 == rhs:
                        return EllipticPoint(self, x, y, z, check=False)
    
    def random_scalar(self):
        return random.randint(1, self.field_size-1)
                    

    def map_point(self, number):
        if number > self.field_size:
            raise ValueError("Number is too large for the field")
        x = self.F(number)


# Only works with elliptic curves over F_2^m, where m > 3
class EllipticPoint:

    def __init__(self, curve: EllipticCurve, x: int, y: int, z:int=1, check=True):
        self.curve = curve
        if check:
            if curve.F(z) == curve._0 and (curve.F(x) != curve._0 and curve.F(y) != curve._1):
                raise ValueError("z can't be zero")
            if not curve.is_projective_point_on_curve(curve.F(x), curve.F(y), curve.F(z)):
                raise ValueError(f"Point ({x}, {y}, {z}) is not on the curve {curve}")
        self.x = curve.F(x)
        self.y = curve.F(y)
        self.z = curve.F(z)
        self.z_2 = self.z**2
        self.z_3 = self.z**3
        self.z_4 = self.z**4

    
    def __add__(self, other):
        if isinstance(other, EllipticPoint):
            if self.curve != other.curve:
                raise ValueError("Can't add points on different curves")
            if self == other:
                return self.double()
            if self == EllipticPoint(self.curve, 0, 1, 0):
                return other
            if other == EllipticPoint(self.curve, 0, 1, 0):
                return self
            lambda1 = self.x * other.z_2
            lambda2 = other.x * self.z_2
            lambda3 = lambda1 - lambda2
            lambda4 = self.y * other.z_3
            lambda5 = other.y * self.z_3
            lambda6 = lambda4 - lambda5
            lambda7 = lambda1 + lambda2
            lambda8 = lambda4 + lambda5
            z3 = self.z * other.z * lambda3
            lambda3_2 = lambda3**2
            x3 = lambda6**2 - lambda7 * lambda3_2
            lambda9 = lambda7 * lambda3_2 - self.curve._2 * x3
            y3 = (lambda9 * lambda6 - lambda8 * lambda3*lambda3_2) * self.curve._2mulinverse
            if z3 == self.curve._0:
                return EllipticPoint(
                    self.curve,
                    0,
                    1,
                    0
                )
            else:
                return EllipticPoint(
                    self.curve,
                    x3,
                    y3,
                    z3,
                    check=True
                )

        
        else:
            raise ValueError("Can't add point to non-point")
    
    def double(self):
        if self == EllipticPoint(self.curve, 0, 1, 0):
            return self
        lambda1 = self.curve._3 * self.x**2 + self.curve.a * self.z_4
        z3 = self.curve._2 * self.y * self.z
        y_2 = self.y**2
        lambda2 = self.curve._4 * self.x * y_2
        x3 = lambda1**2 - self.curve._2 * lambda2
        lambda3 = self.curve._8 * y_2**2
        y3 = lambda1 * (lambda2 - x3) - lambda3
        if z3 == self.curve._0:
            return EllipticPoint(
                self.curve,
                0,
                1,
                0
            )
        else:
            return EllipticPoint(
                self.curve,
                x3,
                y3,
                z3,
                check=True
            )
        
    # set max order to limit the group size, or None to get the full group
    def get_cyclic_group(self, max_order=None):
        group = [self]
        past = set()
        current = self
        while max_order is None or len(group) < max_order:
            past.add(current)
            current = current + self
            if current in past:
                break
            group.append(current)
        return group
    
    def get_order(self):
        i = self.curve.field_size
        point_at_infinity = EllipticPoint(self.curve, 0, 1, 0)
        current = self * i
        while i > 0:
            current = current - self
            if current == point_at_infinity:
                return i
            i -= 1 

    
    def __mul__(self, n: int):
        if n == 0:
            return EllipticPoint(self.curve, 0, 1, 0)
        if n < 0:
            return (-self) * (-n)
        if n == 1:
            return self
        if n % 2 == 0:
            return (self.double()) * (n // 2)
        else:
            return (self.double()) * (n // 2) + self
        
    def __rmul__(self, n: int):
        return self * n
    
    def __neg__(self):
        if self.z == self.curve._0:
            return self
        else:
            return EllipticPoint(self.curve, self.x, (-self.y), self.z, check=False)
    
    def __sub__(self, other):
        return self + (-other)
    
    def __str__(self) -> str:
        if self.z == self.curve._0:
            return f"Point at infinity in {str(self.curve)}" 
        else:
            return f"({str(self.x / self.z**2)}, {str(self.y / self.z**3)}) in {str(self.curve)}"
    
    def __hash__(self) -> int:
        if self.z == 0:
            return hash(('infinity'))
        nx = self.x * self.z_2
        ny = self.y * self.z_3
        return hash((str(nx), str(ny)))


    def __eq__(self, other: EllipticCurve) -> bool:
        if self.z == self.curve._0 or other.z == other.curve._0:
            return self.z == other.z
        else:
            return (self.x * self.z_2 == other.x * other.z_2) and (self.y * self.z_3 == other.y * other.z_3)
