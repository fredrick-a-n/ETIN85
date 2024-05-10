import sympy as sp


def check_orthogonal(B):
    """
    B: Vectors to be checked, each column is a vector
    """
    _, m = B.shape
    for i in range(m):
        for j in range(i):
            if sp.Abs(B[:, i].dot(B[:, j])) > 1e-6:
                return False
    return True


def check_LLL_condition(B, delta: float = 0.75):
    """
    B: Basis vectors to be checked, each column is a vector
    delta: reduction parameter
    """
    _, m = B.shape
    Bs = gram_schmidt(B)

    # size reduction
    for i in range(0, m):
        for j in range(i):
            if sp.Abs(mu(i, j, B, Bs)) > 0.5:
                return False

    # Lovasz condition
    for i in range(1, m):
        if Bs[:, i].dot(Bs[:, i]) < (delta - mu(i, i-1, B, Bs)**2) * Bs[:, i-1].dot(Bs[:, i-1]):
            return False

    return True


def mu(i, j, B, Bs):
    """
    i, j: indices of vectors
    B: Basis vectors, each column is a vector
    Bs: Orthogonalized basis vectors, each column is a vector
    """
    return B[:, i].dot(Bs[:, j]) / Bs[:, j].dot(Bs[:, j])


def gram_schmidt(B):
    """
    B: Vectors to be orthogonalized, each column is a vector
    """
    n, m = B.shape
    Bs = sp.zeros(n,m)
    Bs[:, 0] = B[:, 0].copy()
    mus = {}
    for i in range(1, m):
        v = B[:, i].copy()
        for j in range(i):
            if (i, j) in mus:
                v -= mus[(i, j)] * Bs[:, j]
            else:
                mus[(i, j)] = mu(i, j, B, Bs)
                v -= mus[(i, j)] * Bs[:, j]
        Bs[:, i] = v
    return Bs


def LLL(B, delta: float = 0.75):
    """
    B: matrix to be reduced, each column is a vector
    delta: reduction parameter
    """
    if not (0.25 < delta < 1):
        raise ValueError("delta should be in (1/4, 1)")
    
    # Ensuring that the array will be of python int type, therefore almost unlimited precision
    
    BB = B.copy()
    Bs = gram_schmidt(BB)
    _, m = B.shape
    mus = {}
    i = 1
    while i < m:
        for j in reversed(range(0, i)):
            if (i, j) not in mus:
                mus[(i, j)] = mu(i, j, BB, Bs)
            if sp.Abs(mus[(i, j)]) > 0.5:
                # print(f"Reduce {i} by {j}")
                # print(f"Before reduction: {BB}")
                BB[:, i] -= (int(round(mus[(i, j)])) * BB[:, j])
                # print(f"After reduction: {BB}")

                # naive implementation to recalculate the orthogonalized basis
                Bs = gram_schmidt(BB)
                mus = {}
        if (i, i-1) not in mus:
            mus[(i, i-1)] = mu(i, i-1, BB, Bs)
        if Bs[:, i].dot(Bs[:, i]) > (delta - (mus[(i, i-1)]**2)) * Bs[:, i-1].dot(Bs[:, i-1]):
            i += 1
        else:
            # print(f"Swap {i} and {i-1}")
            # print(f"Before swap: {BB}")
            BB[:, i], BB[:, i-1] = BB[:, i-1].copy(), BB[:, i].copy()
            # print(f"After swap: {BB}")
            i = max(i-1, 1)

            # naive implementation to recalculate the orthogonalized basis
            Bs = gram_schmidt(BB)
            mus = {}

    return BB
