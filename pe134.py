"""Problem 134"""
from primes import primes_from_2_to
from math import ceil, log10
from typing import Tuple, Iterator


def prime_gen(start: int, stop: int) -> Iterator[Tuple[int, int]]:
    """Generates sequential prime pairs."""
    primes = [i for i in primes_from_2_to(1010000) if i >= start]
    while primes[0] < stop:
        yield primes[0], primes[1]
        primes.pop(0)


def find_smallest_multiple(p1: int, p2: int) -> int:
    """Find smallest multiple of p2 such that p1 is contained in the last digits."""
    d = pow(10, int(ceil(log10(p1))))
    x = pow(p2, -1, d)
    s = (p1 * p2 * x) % (p2 * d)
    return s


def main():
    print('Sum:', sum((find_smallest_multiple(int(p1), int(p2)) for p1, p2 in prime_gen(5, 1000000))))


if __name__ == '__main__':
    main()
