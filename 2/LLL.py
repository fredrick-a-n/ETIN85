from sage.all import *


def check_orthogonal(B):
    """
    B: Matrix whose columns are vectors to be checked for orthogonality
    """
    m = B.ncols()
    for i in range(m):
        for j in range(i):
            if abs(B.column(i).dot_product(B.column(j))) > 1e-6:
                return False
    return True


def check_LLL_condition(B, delta=0.75):
    """
    B: Matrix whose columns are basis vectors to be checked
    delta: Reduction parameter
    """
    m = B.ncols()
    Bs = gram_schmidt(B)

    # Size reduction
    for i in range(m):
        for j in range(i):
            if abs(mu(i, j, B, Bs)) > 0.5:
                return False

    # Lovasz condition
    for i in range(1, m):
        if Bs.column(i).dot_product(Bs.column(i)) < (delta - mu(i, i-1, B, Bs)**2) * Bs.column(i-1).dot_product(Bs.column(i-1)):
            return False

    return True


def mu(i, j, B, Bs):
    """
    Calculate the Gram-Schmidt coefficient
    i: index of the column of B
    j: index of the column of Bs
    B: Matrix whose columns are basis vectors
    Bs: Matrix whose columns are orthogonalized basis vectors
    """
    return B.column(i).dot_product(Bs.column(j)) / Bs.column(j).dot_product(Bs.column(j))


def gram_schmidt(B):
    """
    Orthogonalize the columns of matrix B using Gram-Schmidt process
    B: Matrix whose columns are vectors to be orthogonalized
    """
    m = B.ncols()
    Bs = Matrix(QQ, B.nrows(), m)
    Bs[:, 0] = B.column(0)
    for i in range(1, m):
        v = B.column(i)
        for j in range(i):
            proj = mu(i, j, B, Bs) * Bs.column(j)
            v = v - proj
        Bs[:, i] = v
    return Bs


def LLL(B, delta=0.75):
    """
    Perform LLL reduction on matrix B with reduction parameter delta
    B: Matrix whose columns are basis vectors to be reduced
    delta: Reduction parameter
    """
    if not (0.25 < delta < 1):
        raise ValueError("delta should be in (1/4, 1)")

    BB = copy(B)
    Bs = gram_schmidt(BB)
    m = BB.ncols()
    i = 1
    while i < m:
        for j in range(i-1, -1, -1):
            mus = mu(i, j, BB, Bs) 
            if abs(mus) > 0.5:
                BB[:, i] -= round(mus) * BB[:, j]
                Bs = gram_schmidt(BB)
        if Bs.column(i).dot_product(Bs.column(i)) <= (delta - mu(i, i-1, BB, Bs)**2) * Bs.column(i-1).dot_product(Bs.column(i-1)):
            BB.swap_columns(i, i-1)
            i = max(i-1, 1)
            Bs = gram_schmidt(BB)
        else:
            i += 1

    return BB
