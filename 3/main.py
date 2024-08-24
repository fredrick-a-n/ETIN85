import random

def check_test(alice_bloodtype: tuple[int, int, int], bob_bloodtype: tuple[int, int, int]):
    """ Check if the bloodtype is compatible. """
    if bob_bloodtype[0] > alice_bloodtype[0] or bob_bloodtype[1] > alice_bloodtype[1] or bob_bloodtype[2] > alice_bloodtype[2]:
        return False
    return True

def share_secret(value):
    """Alice shares a secret bit value between Alice and Bob."""
    rand = random.randint(0, 1)
    alice_share = value ^ rand
    bob_share = rand
    return alice_share, bob_share

def xor_constant_gate(alice_x, bob_x, constant):
    """Computes XOR on a secret shared value and a constant."""
    alice_z = alice_x ^ constant
    bob_z = bob_x
    return alice_z, bob_z

def xor_gate(alice_x, bob_x, alice_y, bob_y):
    """Computes XOR on secret shared values."""
    alice_z = alice_x ^ alice_y
    bob_z = bob_x ^ bob_y
    return alice_z, bob_z

def open_secret(alice_x, bob_x):
    """Opens the secret shared value."""
    return alice_x ^ bob_x

def and_constant_gate(alice_x, bob_x, constant):
    """Computes AND on a secret shared value and a constant."""
    alice_z = alice_x & constant
    bob_z = bob_x & constant
    return alice_z, bob_z

def and_gate(alice_x, bob_x, alice_y, bob_y, dealer):
    """Computes AND on secret shared values using a dealer."""
    alice_u, bob_u = dealer['u']
    alice_v, bob_v = dealer['v']
    alice_w, bob_w = dealer['w']
    
    alice_d, bob_d = xor_gate(alice_x, bob_x, alice_u, bob_u)
    
    alice_e, bob_e = xor_gate(alice_y, bob_y, alice_v, bob_v)
    
    d = open_secret(alice_d, bob_d)
    e = open_secret(alice_e, bob_e)
    
    # [z] = [w] ⊕ e · [x] ⊕ d · [y] ⊕ e · d
    alice_z, bob_z = xor_constant_gate(*xor_gate(*xor_gate(alice_w, bob_w, *and_constant_gate(alice_x, bob_x, e)), *and_constant_gate(alice_y, bob_y, d)), e & d)
    
    return alice_z, bob_z

def dealer_setup():
    """Sets up the dealer's random triples for AND gate."""
    u = random.randint(0, 1)
    v = random.randint(0, 1)
    w = u & v
    return {'u': share_secret(u), 'v': share_secret(v), 'w': share_secret(w)}


def individual_part(alice_t: int, bob_t: int, print_output=False, type=""):
    """Computes the result of the indiviual part of the bloodtype.
       (T_b AND (T_a XOR 1)) XOR 1 
    """
    # share secrets
    # [t_a] <- t_a ⊕ R
    # [t_b] <- t_b ⊕ R
    alice_t_a, bob_t_a = share_secret(alice_t)
    alice_t_b, bob_t_b = share_secret(bob_t)

    if print_output:
        print(f"alice_{type}_a: {alice_t_a}, bob_{type}_a {bob_t_a}")
        print(f"alice_{type}_b: {alice_t_b}, bob_{type}_b: {bob_t_b}")

    # not of Alice's bloodtype
    # [t_a_not] <- [t_a] ⊕ 1
    alice_t_a_not, bob_t_a_not = xor_constant_gate(alice_t_a, bob_t_a, 1)
    
    if print_output:
        print(f"alice_{type}_a_not: {alice_t_a_not}, bob_{type}_a_not: {bob_t_a_not}")

    # AND
    # [t_and] <- [t_b] AND [t_a_not]
    alice_t_and, bob_t_and = and_gate(alice_t_b, bob_t_b, alice_t_a_not, bob_t_a_not, dealer_setup())

    if print_output:
        print(f"alice_{type}_and: {alice_t_and}, bob_{type}_and: {bob_t_and}")

    # NOT of the AND result
    # [t_result] <- [t_and] ⊕ 1
    alice_t_result, bob_t_result = xor_constant_gate(alice_t_and, bob_t_and, 1)

    if print_output:
        print(f"alice_{type}_result: {alice_t_result}, bob_{type}_result: {bob_t_result}")

    return alice_t_result, bob_t_result


def bloodtype_test(alice_bloodtype: tuple[int, int, int], bob_bloodtype: tuple[int, int, int], print_output=False):
    """Bloodtype test using BeDOZa protocol. Checks if Bob can donate to Alice."""

    alice_a_result, bob_a_result = individual_part(alice_bloodtype[0], bob_bloodtype[0], print_output, "A")
    alice_b_result, bob_b_result = individual_part(alice_bloodtype[1], bob_bloodtype[1], print_output, "B")
    alice_s_result, bob_s_result = individual_part(alice_bloodtype[2], bob_bloodtype[2], print_output, "S")

    # AND of the separate results
    # [result] <- [a_result] AND [b_result] AND [s_result]
    alice_result, bob_result = and_gate(alice_a_result, bob_a_result, alice_b_result, bob_b_result, dealer_setup())
    alice_result, bob_result = and_gate(alice_result, bob_result, alice_s_result, bob_s_result, dealer_setup())

    if print_output:
        print(f"alice_result: {alice_result}, bob_result: {bob_result}")

    # Open the result
    # result <- Open([result])
    return open_secret(alice_result, bob_result)


def map_to_string(a,b,s):
    output = ""
    match (a,b,s):
        case (0,0,0):
            output = "O-"
        case (0,0,1):
            output = "O+"
        case (0,1,0):
            output = "B-"
        case (0,1,1):
            output = "B+"
        case (1,0,0):
            output = "A-"
        case (1,0,1):
            output = "A+"
        case (1,1,0):
            output = "AB-"
        case (1,1,1):
            output = "AB+"
        case _:
            raise ValueError("Invalid bloodtype")
    return output

def test():
    for a_a in [0,1]:
        for b_a in [0,1]:
            for s_a in [0,1]:
                for a_b in [0,1]:
                    for b_b in [0,1]:
                        for s_b in [0,1]:
                            res = bloodtype_test((a_a,b_a,s_a), (a_b,b_b,s_b))
                            print(f"Bloodtype: {map_to_string(a_b,b_b,s_b)} -> {map_to_string(a_a,b_a,s_a)}")
                            print(f"BeDOZa: {res == 1}")
                            print(f"Table check: {check_test((a_a,b_a,s_a), (a_b,b_b,s_b))}")
                            if res != check_test((a_a,b_a,s_a), (a_b,b_b,s_b)):
                                print("ERROR")
                                return
                            print("\n")

if __name__ == '__main__':
    # a_blood = (0, 1, 1)
    # b_blood = (0, 0, 1)

    # res = bloodtype_test(a_blood, b_blood, True)
    # print(f"Bloodtype: {map_to_string(*b_blood)} -> {map_to_string(*a_blood)}")
    # print(f"BeDOZa: {res == 1}")
    # print(f"Table check: {check_test(a_blood, b_blood)}")

    test()