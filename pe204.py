"""<p>A Hamming number is a positive number which has no prime factor larger than $5$.<br>
So the first few Hamming numbers are $1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15$.<br>
There are $1105$ Hamming numbers not exceeding $10^8$.</p>

<p>We will call a positive number a generalised Hamming number of type $n$, if it has no prime factor larger than $n$.<br>
Hence the Hamming numbers are the generalised Hamming numbers of type $5$.</p>

<p>How many generalised Hamming numbers of type $100$ are there which don't exceed $10^9$?</p>
"""
import time

from primes import primes_from_2_to
from math import log, ceil
import time
from typing import List, Iterator


def max_power(base: int, limit: int) -> int:
    """Returns the maximum exponent for a number that fits under a limit."""
    return int(ceil(log(limit, base)))


def get_power_list(p: int, limit: int) -> Iterator[int]:
    return (p**i for i in range(0, max_power(p, limit)))


def get_count_of_hamming_numbers(primes: List[int], limit: int, product_so_far: int = 1) -> int:
    """Recursive function to count Hamming numbers under a given limit."""
    if len(primes) == 1:
        return len([i for i in get_power_list(primes[0], limit) if i*product_so_far <= limit])
    count = 0
    for i in get_power_list(primes[0], limit):
        if not i*product_so_far <= limit:
            break
        count += get_count_of_hamming_numbers(primes[1:], limit, i*product_so_far)
    return count


def main():
    t0 = time.perf_counter()
    primes = primes_from_2_to(100)
    ct = get_count_of_hamming_numbers(sorted(primes, key=lambda x: -x), 10 ** 9)
    tf = time.perf_counter()
    print('Count:', ct)
    print('Time taken:', tf - t0)


if __name__ == '__main__':
    main()
