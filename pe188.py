from time import perf_counter
from math import log2
from sympy import totient


def find_tet(base: int, tetronent: int, mod: int) -> int:
    """Finds a tetration modulo some number."""
    # https://stackoverflow.com/questions/30713648/how-to-compute-ab-mod-m
    if base % mod == 0:
        return 0
    if tetronent == 1:
        return base
    minimum = int(log2(mod))
    tot = int(totient(mod))
    tet_minus_1 = find_tet(base, tetronent - 1, tot)
    if tet_minus_1 < minimum:
        tet_minus_1 = minimum
    return pow(base, tot + tet_minus_1, mod)


def main():
    base = 1777
    tetronent = 1855
    t0 = perf_counter()
    n = find_tet(base, tetronent, 10**8)
    tf = perf_counter()
    print('Result:', n)
    print('Time taken:', tf - t0)


if __name__ == '__main__':
    main()
