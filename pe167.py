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


from itertools import combinations
from functools import lru_cache
from collections import defaultdict
from typing import Set, List
import sys


max_j = 1


def find_next_ulam_sum(seq: List[int]) -> int:
    combo_sums = sorted([i + j for i, j in combinations(seq, 2) if i + j > seq[-1]])
    while combo_sums[0] == combo_sums[1]:
        invalid_sum = combo_sums[0]
        while combo_sums[0] == invalid_sum:
            combo_sums.pop(0)
    return combo_sums[0]


def ulam(v: int):
    ulam_seq = [2, v, 2 + v]
    for i in range(0, 3):
        yield ulam_seq[i]
    i = 3
    while True:
        next_term = find_next_ulam_sum(ulam_seq)
        ulam_seq.append(next_term)
        yield next_term


def main():
    i = 0
    for a in ulam(2, 5):
        i += 1
        print(f'{i}: {a}')
        if i == 10000:
            sys.exit()


if __name__ == '__main__':
    main()