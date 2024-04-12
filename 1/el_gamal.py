from elliptic_curve import *


class ElGamal:

    def __init__(self, curve: EllipticCurve, G: EllipticPoint=None, private_key: int=None, public_key: EllipticPoint=None):
        self.curve = curve
        if G is None:
            self.G = curve.random_point()
        else:
            self.G = G
        if private_key is  None:
            self.private_key = curve.random_scalar()
        else:
            self.private_key = private_key
        if public_key is None:
            self.public_key = self.G * self.private_key
        else:
            self.public_key = public_key

    def get_point(self):
        return self.G
    
    def get_private_key(self):
        return self.private_key
    
    def get_public_key(self):
        return self.public_key
    
    def decrypt(self, c1: EllipticPoint, c2: EllipticPoint):
        return c2 - c1 * self.private_key

def encrypt(curve: EllipticCurve, public_key: EllipticPoint, G: EllipticPoint, message: EllipticPoint):
    if message.curve != curve or public_key.curve != curve or G.curve != curve:
        raise ValueError("Curve doesn't match with the curve of the points")
    r = curve.random_scalar()
    c1 = G * r
    c2 = message + public_key * r
    return (c1, c2)

    

