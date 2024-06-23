"""Problem 134"""
from primes import primesfrom2to
from itertools import count
import numpy as np
from datetime import datetime, timedelta


UPDATE_FREQ_SEC = 5


def prime_gen(start: int, stop: int):
    primes = [i for i in primesfrom2to(1010000) if i >= start]
    while primes[0] < stop:
        yield primes[0], primes[1]
        primes.pop(0)


def find_smallest_multiple(p1: int, p2: int) -> int:
    p1_num_digits = int(np.ceil(np.log10(p1)))
    p1_pow10 = np.power(10, p1_num_digits)
    for i in count(1):
        multiple = i * p1_pow10 + p1
        if multiple % p2 == 0:
            return multiple


def main():
    next_update = datetime.now() + timedelta(seconds=UPDATE_FREQ_SEC)
    #sum_s = sum((find_smallest_multiple(*i) for i in prime_gen(5, 1000000)))
    sum_s = 0
    for p1, p2 in prime_gen(5, 1000000):
        s = find_smallest_multiple(p1, p2)
        if datetime.now() > next_update:
            print(f'({p1}, {p2}): {s} (p2*{s // p2})')
            next_update = datetime.now() + timedelta(seconds=UPDATE_FREQ_SEC)
        sum_s += s
    print(f'Sum: {sum_s}')


if __name__ == '__main__':
    main()
