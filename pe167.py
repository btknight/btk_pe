"""
https://projecteuler.net/problem=167



For two positive integers a and b, the Ulam sequence U(a,b) is defined by U(a,b)1 = a, U(a,b)2 = b and for k > 2,
U(a,b)k is the smallest integer greater than U(a,b)(k-1) which can be written in exactly one way as the sum of two
distinct previous members of U(a,b).

For example, the sequence U(1,2) begins with
1, 2, 3 = 1 + 2, 4 = 1 + 3, 6 = 2 + 4, 8 = 2 + 6, 11 = 3 + 8;
5 does not belong to it because 5 = 1 + 4 = 2 + 3 has two representations as the sum of two previous members, likewise
7 = 1 + 6 = 3 + 4.

Find ∑ U(2,2n+1)k for 2 ≤ n ≤10, where k = 10^11.
"""


from itertools import combinations, product
from collections import defaultdict, namedtuple
from typing import Dict
from datetime import datetime, timedelta
import sys


COMPUTE_UPDATE_FREQ = 10
UlamParm = namedtuple('UlamParm', ['diff', 'period'])
max_j = 1
ulam_parms: Dict[int, UlamParm] = {
    5: UlamParm(126, 32),
    7: UlamParm(126, 26),
    9: UlamParm(1778, 444),
    11: UlamParm(6510, 1628),
    13: UlamParm(23622, 5906),
    15: UlamParm(510, 80),
    17: UlamParm(507842, 126960),
    19: UlamParm(1523526, 380882),
    21: UlamParm(8388606, 2097152),
    23: UlamParm(4194302, 1047588),
}


def zero():
    return 0


def ulam_2u(v: int):
    diff, period = ulam_parms[v]
    if v % 2 == 0 or v < 5:
        raise ValueError(f'v must be an odd number 5 or larger')
    ulam_seq = [2, v, 2 + v]
    ulam_seq_periodic = []
    def ulam_compute(i: int):
        nonlocal ulam_seq, ulam_seq_periodic
        td = timedelta(seconds=COMPUTE_UPDATE_FREQ)
        next_update = datetime.now() + td
        while i >= len(ulam_seq):
            sum_d: Dict[int, int] = defaultdict(zero)
            for a, b in combinations(ulam_seq, 2):
                if a + b > ulam_seq[-1]:
                    sum_d[a + b] += 1
            new_val = min([k for k, val in sum_d.items() if val == 1])
            ulam_seq.append(new_val)
            if next_update < datetime.now():
                print(f'  Compute: {len(ulam_seq)} / {i}')
                next_update = datetime.now() + td
        ulam_seq_periodic = ulam_seq[6:]

    def ulam_term(k: int):
        nonlocal ulam_seq, v
        k_pd = k - 7
        if k < 1:
            raise ValueError(f'k must be a positive integer greater than 0: {k}')
        if k_pd < period:
            ulam_compute(k - 1)
            return ulam_seq[k - 1]
        else:
            ulam_compute((k_pd % period) + 7)
            periodic_product = (k_pd // period) * diff
            seq_add = ulam_seq_periodic[k_pd % period]
            retval = periodic_product + seq_add
            return retval
    return ulam_term


def main():
    sum = 0
    i = 0
    for n in range(2, 11):
        print(f'Ulam(2, {2 * n + 1})')
        v = 2 * n + 1
        diff, period = ulam_parms[v]
        print(f'  diff = {diff}, period = {period}')
        print(f'  Need up to {(10**11 - 7) % period} computes in Ulam seq')
        ulam_term = ulam_2u(v)
        for i in range(1, 51):
            print(f'  {i} = {ulam_term(i)}')
        #val = ulam_term(10**11)
        #print(f'  U(2, {v})[10**11] = {val}')
        #sum += val
    print(f'sum = {sum}')


if __name__ == '__main__':
    main()