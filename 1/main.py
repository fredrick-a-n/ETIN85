from elliptic_curve import *
from el_gamal import *

def test_elliptic():
    curve = EllipticCurve(1, 1, 101, 1)
    p1 = curve.random_point()
    p2 = curve.random_point()
    while p1 == p2:
        p2 = curve.random_point()
    print(f"p1 = {p1}")
    print(f"p2 = {p2}")
    print(f"p1 + p2 = {p1 + p2}")
    print(f"p1 - p2 = {p1 - p2}")
    print(f"[2]p1 = {p1*2}")
    print(f"[3]p1 = {p1*3}")

    g = p1.get_cyclic_group()
    print(f"p1 cyclic group: \n")
    print(f"Group size: {len(g)}")
    print(f"Group: \n")
    for i, point in enumerate(g):
        print(f"{i}: {point}")


def test_elgamal():
    curve = EllipticCurve(1, 1, 1000003, 1)
    elgamal = ElGamal(curve, G=EllipticPoint(curve, 613420, 643318, 1))
    G = elgamal.get_point()
    public_key = elgamal.get_public_key()
    print(f"G = {G}")
    print(f"public_key = {public_key}")
    print(f"private_key = {elgamal.get_private_key()}")

    message = EllipticPoint(curve, 600768, 817884, 1)
    #message = curve.random_point()
    print(f"Message: {message}")

    c1, c2 = encrypt(curve, public_key, G, message)
    print(f"c1 = {c1}")
    print(f"c2 = {c2}")

    decrypted = elgamal.decrypt(c1, c2)
    print(f"Decrypted: {decrypted}")


if __name__ == "__main__":
    # test_elgamal()
    test_elliptic()